## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy.sql import func
from numpy import array

from cables.models import DBSession
from cables.models import TVZonesSensibles, TCommune, \
        TInventairePoteauxErdf, TEquipementsPoteauxErdf, \
        TInventaireTronconsErdf, TEquipementsTronconsErdf
from cables.views import year_extract_p, year_extract_t, years_p, years_t, \
        R_HIG, R_SEC, R_LOW, to_int, add_header_row, flatten

log = logging.getLogger(__name__)

@view_config(route_name='export_zonessensibles', renderer='csv')
def export_zonessensibles(request):
    global years_p, years_t
    DBSession.execute('SET search_path TO cables73, public')
    query = DBSession.query(TVZonesSensibles)
    if request.params.has_key('ids'):
        ids = map(int, request.params.get('ids').split(','))
        query = query.filter(TVZonesSensibles.id_zone_sensible.in_(ids))
    years_p = tuple(sorted(map(to_int, DBSession.query(year_extract_p).distinct().all())))
    years_t = tuple(sorted(map(to_int, DBSession.query(year_extract_t).distinct().all())))
    entries = map(zs_to_dict, query)
    add_header_row(entries, 'nom', years_p, years_t)
    return array(entries).transpose()

def zs_to_dict(item):
    poteaux = (
        item.nom_zone_sensible,
        item.nb_poteaux_inventories_risque_fort,
        item.nb_poteaux_inventories_risque_secondaire,
        (item.nb_poteaux_inventories_risque_fort or 0) + (item.nb_poteaux_inventories_risque_secondaire or 0),
        item.nb_poteaux_equipes_risque_fort,
        item.nb_poteaux_equipes_risque_secondaire,
        (item.nb_poteaux_equipes_risque_fort or 0) + (item.nb_poteaux_equipes_risque_secondaire or 0))
    qfilter = TInventairePoteauxErdf.id_zone_sensible==item.id_zone_sensible
    poteaux_year = tuple( get_nb_poteaux(item, year, qfilter) for year in years_p )
    troncons = (
        item.m_troncons_inventories_risque_fort,
        item.m_troncons_inventories_risque_secondaire,
        (item.m_troncons_inventories_risque_fort or 0) + (item.m_troncons_inventories_risque_secondaire or 0),
        item.m_troncons_equipes_risque_fort,
        item.m_troncons_equipes_risque_secondaire,
        (item.m_troncons_equipes_risque_fort or 0) + (item.m_troncons_equipes_risque_secondaire or 0))
    qfilter = TInventaireTronconsErdf.id_zone_sensible==item.id_zone_sensible
    troncons_year = tuple( get_len_troncons(item, year, qfilter) for year in years_t )
    return poteaux + poteaux_year + troncons + troncons_year

def get_nb_poteaux(item, year, qfilter):
    return DBSession.query(TInventairePoteauxErdf).\
            join(TEquipementsPoteauxErdf).\
            filter(qfilter).\
            filter(year_extract_p==year).\
            count()

def get_len_troncons(item, qfilter, year=None):
    q = DBSession.query(func.sum(TInventaireTronconsErdf.lg_equipee)).\
            join(TEquipementsTronconsErdf).\
            filter(qfilter)
    if year is not None:
        q = q.filter(year_extract_t==year)
    length = q.first()[0]
    return 0 if length is None else int(length)

@view_config(route_name='export_communes', renderer='csv')
def export_communes(request):
    entries = get_communes('cables73')
    entries = flatten(entries)
    add_header_row(entries, 'Commune', years_p, years_t)
    return array(entries).transpose()

def get_communes(schema):
    global years_p, years_t
    DBSession.execute('SET search_path TO %s, public' % schema)
    years_p = tuple(sorted(map(to_int, DBSession.query(year_extract_p).distinct().all())))
    years_t = tuple(sorted(map(to_int, DBSession.query(year_extract_t).distinct().all())))

    communes_poteaux = map(lambda x: x.insee, DBSession.query(TCommune.insee) \
        .join(TInventairePoteauxErdf) \
        .join(TEquipementsPoteauxErdf) \
        .distinct())
    communes_troncons = map(lambda x: x.insee, DBSession.query(TCommune.insee) \
        .join(TInventaireTronconsErdf) \
        .filter(TInventaireTronconsErdf.lg_equipee != None) \
        .distinct())
    ids = list(set(communes_poteaux + communes_troncons))

    query = DBSession.query(TCommune) \
        .outerjoin(TInventairePoteauxErdf) \
        .outerjoin(TEquipementsPoteauxErdf) \
        .outerjoin(TInventaireTronconsErdf) \
        .filter(TCommune.insee.in_(ids))
    entries = map(commune_to_dict, query)
    return entries

def poteaux_filter(value, equipements=False):
  if equipements:
      return lambda x: x.risque_poteau == value and len(x.equipements)>0
  return lambda x: x.risque_poteau == value

def len_troncons (troncons, rfilter, equipements=False):
    if equipements:
        qf = lambda x: x.risque_troncon == rfilter and len(x.equipements)>0
    else:
        qf = lambda x: x.risque_troncon == rfilter
    troncons = filter(lambda x: x.risque_troncon == rfilter, troncons)
    return int(sum(filter(
        lambda t: t if t is not None else 0,
        [ troncon.lg_equipee for troncon in troncons ])))

def commune_to_dict(item):
    hig = len(filter(poteaux_filter(R_HIG), item.poteaux))
    sec = len(filter(poteaux_filter(R_SEC), item.poteaux))
    hig_eq = len(filter(poteaux_filter(R_HIG, equipements=True), item.poteaux))
    sec_eq = len(filter(poteaux_filter(R_SEC, equipements=True), item.poteaux))
    pfilter = TInventairePoteauxErdf.insee == item.insee
    tfilter = TInventaireTronconsErdf.insee == item.insee

    poteaux = (item.nom_commune, hig, sec, hig + sec, hig_eq, sec_eq, hig_eq + sec_eq)
    poteaux_year = { year: get_nb_poteaux(item, year, pfilter) for year in years_p}

    t_hig = len_troncons(item.troncons, R_HIG)
    t_sec = len_troncons(item.troncons, R_SEC)
    t_hig_eq = len_troncons(item.troncons, R_HIG, equipements=True)
    t_sec_eq = len_troncons(item.troncons, R_SEC, equipements=True)

    troncons = ( t_hig, t_sec, t_hig + t_sec, t_hig_eq, t_sec_eq, t_hig_eq + t_sec_eq)
    troncons_year = {year: get_len_troncons(item, tfilter, year) for year in years_t }

    return {
            "poteaux": poteaux,
            "poteaux_year": poteaux_year,
            "troncons": troncons,
            "troncons_year": troncons_year }

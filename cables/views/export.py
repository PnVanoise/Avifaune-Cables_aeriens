## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy import extract
from sqlalchemy.sql import func
from numpy import array

from cables.models import DBSession
from cables.models import TVZonesSensibles, TCommune, \
        TInventairePoteauxErdf, TEquipementsPoteauxErdf, \
        TInventaireTronconsErdf, TEquipementsTronconsErdf

log = logging.getLogger(__name__)

year_extract_p = extract('year', TEquipementsPoteauxErdf.date_equipement)
year_extract_t = extract('year', TEquipementsTronconsErdf.date_equipement_troncon)
years_p = ()
years_t = ()

R_HIG = u'Risque élevé'
R_SEC = u'Risque secondaire'
R_LOW = u'Peu ou pas de risque'

to_int = lambda x: int(x[0])

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
    add_header_row(entries, 'nom')
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
    global years_p, years_t
    DBSession.execute('SET search_path TO cables73, public')
    years_p = tuple(sorted(map(to_int, DBSession.query(year_extract_p).distinct().all())))
    years_t = tuple(sorted(map(to_int, DBSession.query(year_extract_t).distinct().all())))
    query = DBSession.query(TCommune) \
        .join(TInventairePoteauxErdf) \
        .join(TEquipementsPoteauxErdf)
    entries = map(commune_to_dict, query)
    add_header_row(entries, 'Commune')
    return array(entries).transpose()

def poteaux_filter(value, equipements=False):
  if equipements:
      return lambda x: x.risque_poteau == value and len(x.equipements)>0
  return lambda x: x.risque_poteau == value

def commune_to_dict(item):
    hig = len(filter(poteaux_filter(R_HIG), item.poteaux))
    sec = len(filter(poteaux_filter(R_SEC), item.poteaux))
    hig_eq = len(filter(poteaux_filter(R_HIG, equipements=True), item.poteaux))
    sec_eq = len(filter(poteaux_filter(R_SEC, equipements=True), item.poteaux))
    qfilter = TInventairePoteauxErdf.insee == item.insee

    poteaux = (item.nom_commune,
        hig, sec, hig + sec,
        hig_eq, sec_eq, hig_eq + sec_eq)
    poteaux_year = tuple( get_nb_poteaux(item, year, qfilter) for year in years_p )
    troncons = (
       '',
       '',
       '',
       '',
       '',
       '')
    troncons_year = tuple( get_len_troncons(item, year, qfilter) for year in years_t )
    return poteaux + poteaux_year + troncons + troncons_year

def add_header_row(entries, name):
    labels_years_p = tuple(u'Nb poteaux équipés en %s' % year for year in years_p)
    labels_years_t = tuple(u'Longueur troncons équipés en %s' % year for year in years_t)
    entries.insert(0, (
        name,
        u'Nb poteaux risque fort',
        u'Nb poteaux risque secondaire',
        u'Nb poteaux risque',
        u'Nb poteaux équipés risque fort',
        u'Nb poteaux équipés risque secondaire',
        u'Nb poteaux équipés risque') +
        labels_years_p + (
        u'Longueur troncons risque élevé',
        u'Longueur troncons risque secondaire',
        u'Longueur troncons risque',
        u'Longueur troncons équipés risque élevé',
        u'Longueur troncons équipés risque secondaire',
        u'Longueur troncons équipés risque') +
        labels_years_t
        )

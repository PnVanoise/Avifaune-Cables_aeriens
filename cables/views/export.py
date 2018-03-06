## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy import extract
from sqlalchemy.sql import func
from numpy import array

from cables.models import DBSession
from cables.models import TVZonesSensibles, \
        TInventairePoteauxErdf, TEquipementsPoteauxErdf, \
        TInventaireTronconsErdf, TEquipementsTronconsErdf

log = logging.getLogger(__name__)

@view_config(route_name='export_zonessensibles', renderer='csv')
def export_zonessensibles(request):
    query = DBSession.query(TVZonesSensibles)
    if request.params.has_key('ids'):
        ids = map(int, request.params.get('ids').split(','))
        query = query.filter(TVZonesSensibles.id_zone_sensible.in_(ids))
    rows = query.all()
    entries = map(zs_to_dict, rows)
    entries.insert(0, (
        'id',
        'nom',
        'Nb poteaux risque fort',
        'Nb poteaux risque secondaire',
        'Nb poteaux risque',
        'Nb poteaux équipés risque fort',
        'Nb poteaux équipés risque secondaire',
        'Nb poteaux équipés risque',
        'Nb poteaux équipés en 2014',
        'Nb poteaux équipés en 2015',
        'Nb poteaux équipés en 2016',
        'Longueur troncons risque élevé',
        'Longueur troncons risque secondaire',
        'Longueur troncons risque',
        'Longueur troncons équipés risque élevé',
        'Longueur troncons équipés risque secondaire',
        'Longueur troncons équipés risque',
        'Longueur troncons équipés en 2014',
        'Longueur troncons équipés en 2015',
        'Longueur troncons équipés en 2016',
        ))
    return array(entries).transpose()

def zs_to_dict(item):
    return (
        item.id_zone_sensible,
        item.nom_zone_sensible,
        item.nb_poteaux_inventories_risque_fort,
        item.nb_poteaux_inventories_risque_secondaire,
        (item.nb_poteaux_inventories_risque_fort or 0) + (item.nb_poteaux_inventories_risque_secondaire or 0),
        item.nb_poteaux_equipes_risque_fort,
        item.nb_poteaux_equipes_risque_secondaire,
        (item.nb_poteaux_equipes_risque_fort or 0) + (item.nb_poteaux_equipes_risque_secondaire or 0),
        get_nb_poteaux(item, 2014),
        get_nb_poteaux(item, 2015),
        get_nb_poteaux(item, 2016),
        item.m_troncons_inventories_risque_fort,
        item.m_troncons_inventories_risque_secondaire,
        (item.m_troncons_inventories_risque_fort or 0) + (item.m_troncons_inventories_risque_secondaire or 0),
        item.m_troncons_equipes_risque_fort,
        item.m_troncons_equipes_risque_secondaire,
        (item.m_troncons_equipes_risque_fort or 0) + (item.m_troncons_equipes_risque_secondaire or 0),
        get_len_troncons(item, 2014),
        get_len_troncons(item, 2015),
        get_len_troncons(item, 2016),
        )

def get_nb_poteaux(item, year):
    year_extract = extract('year', TEquipementsPoteauxErdf.date_equipement)
    return DBSession.query(TInventairePoteauxErdf).\
            join(TEquipementsPoteauxErdf).\
            filter(TInventairePoteauxErdf.id_zone_sensible==item.id_zone_sensible).\
            filter(year_extract==year).\
            count()

def get_len_troncons(item, year):
    year_extract = extract('year', TEquipementsTronconsErdf.date_equipement_troncon)
    length = DBSession.query(func.sum(TInventaireTronconsErdf.lg_equipee)).\
            join(TEquipementsTronconsErdf).\
            filter(TInventaireTronconsErdf.id_zone_sensible==item.id_zone_sensible).\
            filter(year_extract==year).\
            first()[0]
    return 0 if length is None else float(length)

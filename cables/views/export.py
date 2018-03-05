## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy import extract
from numpy import array

from cables.models import DBSession
from cables.models import TVZonesSensibles
from cables.models import TInventairePoteauxErdf
from cables.models import TEquipementsPoteauxErdf


log = logging.getLogger(__name__)

@view_config(route_name='export', renderer='csv')
def export(request):
    query = DBSession.query(TVZonesSensibles)
    if request.params.has_key('ids'):
        ids = map(int, request.params.get('ids').split(','))
        query = query.filter(TVZonesSensibles.id_zone_sensible.in_(ids))
    rows = query.all()
    entries = map(to_dict, rows)
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
        ))
    return array(entries).transpose()

def to_dict(item):
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
        )

def get_nb_poteaux(item, year):
    year_extract = extract('year', TEquipementsPoteauxErdf.date_equipement)
    return DBSession.query(TInventairePoteauxErdf).\
            join(TEquipementsPoteauxErdf).\
            filter(TInventairePoteauxErdf.id_zone_sensible==item.id_zone_sensible).\
            filter(year_extract==year).\
            count()

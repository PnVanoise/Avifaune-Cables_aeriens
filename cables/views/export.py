## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.security import remember, forget
from pyramid.response import Response

from cables.models import DBSession
# from cables.models import TZonesSensible
from cables.models import TVZonesSensibles
from numpy import array


log = logging.getLogger(__name__)

@view_config(route_name='export', renderer='csv')
def export(request):
    rows = map(to_dict, DBSession.query(TVZonesSensibles).all())
    return array(rows).transpose()

def to_dict(item):
    return (
        item.id_zone_sensible,
        item.nom_zone_sensible,
        item.niveau_sensibilite,
        item.nb_poteaux_inventories,
        item.nb_poteaux_inventories_risque_fort,
        item.nb_poteaux_inventories_risque_secondaire,
        item.nb_poteaux_inventories_risque_faible,
        item.nb_poteaux_equipes,
        item.nb_poteaux_equipes_risque_fort,
        item.nb_poteaux_equipes_risque_secondaire,
        item.nb_poteaux_equipes_risque_faible,
        item.m_troncons_inventories,
        item.m_troncons_inventories_risque_fort,
        item.m_troncons_inventories_risque_secondaire,
        item.m_troncons_inventories_risque_faible,
        item.m_troncons_equipes,
        item.m_troncons_equipes_risque_fort,
        item.m_troncons_equipes_risque_secondaire,
        item.m_troncons_equipes_risque_faible,
        )

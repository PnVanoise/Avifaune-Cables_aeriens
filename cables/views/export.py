## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.security import remember, forget
from pyramid.response import Response

from cables.models import DBSession
from cables.models import TZonesSensible


log = logging.getLogger(__name__)

@view_config(route_name='export', renderer='csv')
def export(request):
    rows = DBSession.query(TZonesSensible).all()
    return map(to_dict, rows)

def to_dict(item):
    return ( item.id_zone_sensible, item.nom_zone_sensible, item.niveau_sensibilite )


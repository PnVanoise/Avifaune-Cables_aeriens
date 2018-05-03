## -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest

from sqlalchemy.sql import func
from numpy import array

from cables.models import DBSession
from cables.views import add_header_row, flatten
from cables.views.export import get_communes

log = logging.getLogger(__name__)

@view_config(route_name='export_departements', renderer='csv')
def export_departements(request):
    flattened = flatten(
            get_communes('cables73') + get_communes('cables74'),
            compute_years=True)
    entries = flattened.get('entries')
    add_header_row(
            entries,
            u'Département',
            flattened.get('p_years'),
            flattened.get('t_years'))
    return array(entries).transpose()

# -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config

from numpy import array

from cables.views import add_header_row, flatten
from cables.views.export import get_communes

log = logging.getLogger(__name__)


@view_config(route_name='export_departements', renderer='csv')
def export_departements(request):
    flattened = flatten(
            get_communes('73') + get_communes('74'),
            compute_years=True)
    entries = flattened.get('entries')
    add_header_row(
            entries,
            (u'Département', u'Commune'),
            flattened.get('p_years'),
            flattened.get('t_years'))
    # Full array
    transposed = array(entries).transpose()
    # Delete commune row
    return delete(transposed, 1, 0)

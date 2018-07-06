# -*- coding: utf-8 -*-
from logging import getLogger
from pyramid.view import view_config
from numpy import array, delete

from cables.views import add_header_row, flatten
from cables.views.export import get_communes

log = getLogger(__name__)


def sum_values(data, life):
    """ Sum row values for cols of same department
    """
    data = array(data).transpose()
    # delete commune row, cast as int, sum rows
    filtered = delete(data, 1, 0).astype(int).sum(axis=1)
    return filtered


@view_config(route_name='export_life', renderer='csv')
def export_life(request):
    life = True if request.params['life'] == 'true' else False
    flattened = flatten(
            get_communes(u'73', life=life) + get_communes(u'74', life=life),
            compute_years=True)
    entries = sum_values(flattened.get('entries'), life).tolist()
    entries[0] = 'Life' if life else 'Hors life'
    entries = [entries]
    add_header_row(
            entries,
            u'Life',
            flattened.get('p_years'),
            flattened.get('t_years'))

    return array(entries).transpose()

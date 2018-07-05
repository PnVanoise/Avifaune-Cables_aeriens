# -*- coding: utf-8 -*-
import logging
from pyramid.view import view_config
from numpy import array, delete, concatenate

from cables.views import add_header_row, flatten
from cables.views.export import get_communes

log = logging.getLogger(__name__)


def sum_dept_values(data, dept):
    """ Sum row values for cols of same department
    """
    data = array(data).transpose()
    # delete commune row, cast as int, sum rows
    filtered = delete(data[:, (data == dept)[0]], 1, 0).astype(int).sum(axis=1)
    # reset dept to its value
    filtered.itemset(0, dept)
    return filtered


@view_config(route_name='export_departements', renderer='csv')
def export_departements(request):
    grouped = 'group' in request.params
    flattened = flatten(
            get_communes(u'73') + get_communes(u'74'),
            compute_years=True)
    entries = flattened.get('entries')
    if grouped:
        entries73, entries74 = [
                sum_dept_values(entries, d) for d in [u'73', u'74']]
        entries = concatenate(([entries73], [entries74]), axis=0).tolist()
    add_header_row(
            entries,
            u'Département' if grouped else (u'Département', u'Commune'),
            flattened.get('p_years'),
            flattened.get('t_years'))

    return array(entries).transpose()

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
        R_HIG, R_SEC, R_LOW, to_int, add_header_row
from cables.views.export import get_communes

log = logging.getLogger(__name__)

@view_config(route_name='export_departements', renderer='csv')
def export_departements(request):
    entries = get_communes('cables73')
    add_header_row(entries, u'Département', years_p, years_t)
    return array(entries).transpose()

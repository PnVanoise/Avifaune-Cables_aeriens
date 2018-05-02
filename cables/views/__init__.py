## -*- coding: utf-8 -*-
import logging

from sqlalchemy import extract
from cables.models import TEquipementsPoteauxErdf, TEquipementsTronconsErdf

log = logging.getLogger(__name__)

year_extract_p = extract('year', TEquipementsPoteauxErdf.date_equipement)
year_extract_t = extract('year', TEquipementsTronconsErdf.date_equipement_troncon)
years_p = ()
years_t = ()

R_HIG = u'Risque élevé'
R_SEC = u'Risque secondaire'
R_LOW = u'Peu ou pas de risque'

to_int = lambda x: int(x[0]) if x[0] is not None else 0

def add_header_row(entries, name, years_p, years_t):
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

def flatten_years_item(item):
    return item['poteaux'] + tuple(map(lambda r: r[1], item['poteaux_year'])) + \
            item['troncons'] + tuple(map(lambda r: r[1], item['troncons_year']))

def flatten_years(entries):
    return map(flatten_years_item, entries)

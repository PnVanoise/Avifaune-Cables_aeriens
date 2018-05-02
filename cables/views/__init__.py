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

def flatten_property(item, attr, keys=None):
    if keys is None:
        keys = item[attr].keys()
    return tuple(item[attr].get(key, 0) for key in keys)

def flatten_item(item, p_years, t_years):
    return item['poteaux'] + flatten_property(item, 'poteaux_year', keys=p_years) + \
            item['troncons'] + flatten_property(item, 'troncons_year', keys=t_years)

def flatten(entries, compute_years=False):
    p_years = (2014, 2015, 2016) if compute_years else None
    t_years = (2012, 2013, 2014, 2015, 2016) if compute_years else None
    return map(lambda x: flatten_item(x, p_years, t_years), entries)

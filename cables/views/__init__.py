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

to_int = lambda x: int(x[0])

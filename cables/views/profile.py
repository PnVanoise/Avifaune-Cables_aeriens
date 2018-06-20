# -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

from cables import PROFILES
from cables.models import DBSession
from cables.models.utilisateurs import TRole, BibOrganisme

log = logging.getLogger(__name__)


@view_config(route_name='profile', renderer='json')
def profile(request):
    user = request.params.get('user')
    if user is None:
        raise HTTPBadRequest()
    profile = DBSession.query(TRole).join(BibOrganisme).filter(
            TRole.identifiant == user).first()
    if profile is None:
        raise HTTPNotFound()
    id_org = profile.bib_organisme.id_organisme
    return {"id_org": id_org,
            "org": PROFILES[str(id_org)] if str(id_org) in PROFILES else ''}

# -*- coding: utf-8 -*-
import logging

from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound, HTTPBadRequest

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
    org = profile.bib_organisme.id_organisme
    return {"org": org}

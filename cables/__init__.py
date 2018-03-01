#-*- coding: utf-8 -*-
import os

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.decorator import reify
from pyramid.request import Request
from pyramid.security import unauthenticated_userid
import sqlalchemy
import sqlahelper
import pyramid_tm

from pyramid_beaker import session_factory_from_settings

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    session_factory = session_factory_from_settings(settings)

    config = Configurator(settings=settings,
                          session_factory=session_factory)

    config.include('pyramid_mako')

    # initialize database
    engine = sqlalchemy.engine_from_config(settings, 'sqlalchemy.')
    sqlahelper.add_engine(engine)


    # add the "geojson" and "csv" renderer
    config.add_renderer(name='csv', factory='cables.renderers.CSVRenderer')

    # add routes to the entry view class
    config.add_route('home', '/')

    # we need to call scan() for the "home" and "countries"
    # routes
    config.scan()

    # add the static view (for static resources)
    config.add_static_view('static', 'cables:static')

    return config.make_wsgi_app()


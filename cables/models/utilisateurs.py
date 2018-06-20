# coding: utf-8
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, \
        String, Table, Text, text
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
metadata = Base.metadata


class BibDroit(Base):
    __tablename__ = 'bib_droits'
    __table_args__ = {u'schema': 'utilisateurs'}

    id_droit = Column(Integer, primary_key=True)
    nom_droit = Column(String(50))
    desc_droit = Column(Text)


class BibObservateur(Base):
    __tablename__ = 'bib_observateurs'
    __table_args__ = {u'schema': 'utilisateurs'}

    codeobs = Column(String(6), primary_key=True)
    nom = Column(String(100))
    prenom = Column(String(100))
    orphelin = Column(Integer)


class BibOrganisme(Base):
    __tablename__ = 'bib_organismes'
    __table_args__ = {u'schema': 'utilisateurs'}

    nom_organisme = Column(String(100), nullable=False)
    adresse_organisme = Column(String(128))
    cp_organisme = Column(String(5))
    ville_organisme = Column(String(100))
    tel_organisme = Column(String(14))
    fax_organisme = Column(String(14))
    email_organisme = Column(String(100))
    id_organisme = Column(Integer, primary_key=True, server_default=text("nextval('utilisateurs.bib_organismes_id_seq'::regclass)"))


class BibUnite(Base):
    __tablename__ = 'bib_unites'
    __table_args__ = {u'schema': 'utilisateurs'}

    nom_unite = Column(String(50), nullable=False)
    adresse_unite = Column(String(128))
    cp_unite = Column(String(5))
    ville_unite = Column(String(100))
    tel_unite = Column(String(14))
    fax_unite = Column(String(14))
    email_unite = Column(String(100))
    id_unite = Column(Integer, primary_key=True, server_default=text("nextval('utilisateurs.bib_unites_id_seq'::regclass)"))


class CorRoleDroitApplication(Base):
    __tablename__ = 'cor_role_droit_application'
    __table_args__ = {u'schema': 'utilisateurs'}

    id_role = Column(ForeignKey(u'utilisateurs.t_roles.id_role', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False)
    id_droit = Column(ForeignKey(u'utilisateurs.bib_droits.id_droit', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False)
    id_application = Column(ForeignKey(u'utilisateurs.t_applications.id_application', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False)

    t_application = relationship(u'TApplication')
    bib_droit = relationship(u'BibDroit')
    t_role = relationship(u'TRole')


t_cor_role_menu = Table(
    'cor_role_menu', metadata,
    Column('id_role', ForeignKey(u'utilisateurs.t_roles.id_role', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('id_menu', ForeignKey(u'utilisateurs.t_menus.id_menu', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    schema='utilisateurs'
)
class TCorRoleMenu(object):
    pass
mapper(TCorRoleMenu, t_cor_role_menu)


t_cor_roles = Table(
    'cor_roles', metadata,
    Column('id_role_groupe', ForeignKey(u'utilisateurs.t_roles.id_role', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    Column('id_role_utilisateur', ForeignKey(u'utilisateurs.t_roles.id_role', ondelete=u'CASCADE', onupdate=u'CASCADE'), primary_key=True, nullable=False),
    schema='utilisateurs'
)
class TCorRoles(object):
    pass
mapper(TCorRoles, t_cor_roles)


class TApplication(Base):
    __tablename__ = 't_applications'
    __table_args__ = {u'schema': 'utilisateurs'}

    id_application = Column(Integer, primary_key=True, server_default=text("nextval('utilisateurs.t_applications_id_application_seq'::regclass)"))
    nom_application = Column(String(50), nullable=False)
    desc_application = Column(Text)


class TMenu(Base):
    __tablename__ = 't_menus'
    __table_args__ = {u'schema': 'utilisateurs'}

    id_menu = Column(Integer, primary_key=True, server_default=text("nextval('utilisateurs.t_menus_id_menu_seq'::regclass)"))
    nom_menu = Column(String(50), nullable=False)
    desc_menu = Column(Text)
    id_application = Column(ForeignKey(u'utilisateurs.t_applications.id_application', ondelete=u'CASCADE', onupdate=u'CASCADE'))

    t_application = relationship(u'TApplication')
    # t_roles = relationship(u'TRole', secondary='TCorRoles')


class TRole(Base):
    __tablename__ = 't_roles'
    __table_args__ = {u'schema': 'utilisateurs'}

    groupe = Column(Boolean, nullable=False, server_default=text("false"))
    id_role = Column(Integer, primary_key=True, server_default=text("nextval('utilisateurs.t_roles_id_seq'::regclass)"))
    identifiant = Column(String(100))
    nom_role = Column(String(50))
    prenom_role = Column(String(50))
    desc_role = Column(Text)
    _pass = Column('pass', String(100))
    email = Column(String(250))
    id_organisme = Column(ForeignKey(u'utilisateurs.bib_organismes.id_organisme', onupdate=u'CASCADE'))
    organisme = Column(String(32))
    id_unite = Column(ForeignKey(u'utilisateurs.bib_unites.id_unite', onupdate=u'CASCADE'))
    remarques = Column(Text)
    pn = Column(Boolean)
    session_appli = Column(String(50))
    date_insert = Column(DateTime)
    date_update = Column(DateTime)

    bib_organisme = relationship(u'BibOrganisme')
    bib_unite = relationship(u'BibUnite')
    # parents = relationship(
    #     u'TRole',
    #     secondary='cor_roles',
    #     primaryjoin=u'TRole.id_role == TCorRoles.id_role_groupe',
    #     secondaryjoin=u'TRole.id_role == TCorRoles.id_role_utilisateur'
    # )


t_view_login = Table(
    'view_login', metadata,
    Column('id_role', Integer),
    Column('identifiant', String(100)),
    Column('pass', String(100)),
    Column('nom_complet', Text),
    Column('id_application', Integer),
    Column('maxdroit', Integer),
    schema='utilisateurs'
)

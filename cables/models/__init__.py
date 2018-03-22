#-*- coding: utf-8 -*-
import logging
import sqlahelper

from sqlalchemy import BigInteger, Boolean, CheckConstraint, Column, Date, DateTime, Float, ForeignKey, Index, Integer, String, Table, Text, text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship, mapper
from sqlalchemy.ext.declarative import declarative_base

log = logging.getLogger(__name__)

Base = sqlahelper.get_base()
metadata = Base.metadata
DBSession = sqlahelper.get_session()

class DicoAge(Base):
    __tablename__ = 'dico_age'

    id_age = Column(Integer, primary_key=True)
    lib_age = Column(String(20))


class DicoCauseMortalite(Base):
    __tablename__ = 'dico_cause_mortalite'

    id_cause_mortalite = Column(Integer, primary_key=True)
    lib_cause_mortalite = Column(String(20))


class DicoClassesRisque(Base):
    __tablename__ = 'dico_classes_risque'

    id_classe_risque = Column(Integer, primary_key=True, server_default=text("nextval('dico_classes_risque_id_classe_risque_seq'::regclass)"))
    lib_classe_risque = Column(String(30))


class DicoNbEquipement(Base):
    __tablename__ = 'dico_nb_equipements'

    id_nb_equipements = Column(Integer, primary_key=True)
    nb_equipements = Column(Integer)


class DicoSexe(Base):
    __tablename__ = 'dico_sexe'

    id_sexe = Column(Integer, primary_key=True)
    lib_sexe = Column(String(20))


class DicoSource(Base):
    __tablename__ = 'dico_source'

    id_source = Column(Integer, primary_key=True)
    lib_source = Column(String(20))


class DicoTypeEquipementPoteau(Base):
    __tablename__ = 'dico_type_equipement_poteau'

    id_type_equipement_poteau = Column(Integer, primary_key=True)
    nom_type_equipement_poteau = Column(String)


class DicoTypeEquipementTroncon(Base):
    __tablename__ = 'dico_type_equipement_troncon'

    id_type_equipement_troncon = Column(Integer, primary_key=True)
    nom_type_equipement_troncon = Column(String)


class DicoTypePoteauErdf(Base):
    __tablename__ = 'dico_type_poteau_erdf'

    id_type_poteau_erdf = Column(Integer, primary_key=True)
    lib_type_poteau_erdf = Column(String)


class ErdfAppareilCoupure(Base):
    __tablename__ = 'erdf_appareil_coupure'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_appareil_coupure_id_seq'::regclass)"))
    AUTOMATISM = Column(String(62))
    AUTOMATIS1 = Column(String(62))
    AUTOMATIS2 = Column(String(62))
    POTEAU_HTA = Column(String(32))
    STATUT = Column(String(12))
    TYPE_DE_CO = Column(String(32))
    T_L_COMMAN = Column(String(7))
    SYMBOLOGIE = Column(String(64))
    ANGLE = Column(Float(53))
    SYSANGLE = Column(Float(53))
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class ErdfConnexionAerienne(Base):
    __tablename__ = 'erdf_connexion_aerienne'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_connexion_aerienne_id_seq'::regclass)"))
    POTEAU_HTA = Column(String(32))
    STATUT = Column(String(12))
    TYPE_DE_CO = Column(String(40))
    SYMBOLOGIE = Column(String(64))
    ANGLE = Column(Float(53))
    SYSANGLE = Column(Float(53))
    ID_SIG = Column(Integer)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class ErdfParafoudre(Base):
    __tablename__ = 'erdf_parafoudre'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_parafoudre_id_seq'::regclass)"))
    POTEAU_HTA = Column(String(32))
    STATUT = Column(String(12))
    TYPE = Column(String(32))
    SYMBOLOGIE = Column(String(64))
    ANGLE = Column(Float(53))
    SYSANGLE = Column(Float(53))
    ID_SIG = Column(Integer)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class ErdfPosteElectrique(Base):
    __tablename__ = 'erdf_poste_electrique'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_poste_electrique_id_seq'::regclass)"))
    FONCTION_P = Column(String(40))
    NOM_DU_POS = Column(String(32))
    POTEAU_HTA = Column(String(32))
    STATUT = Column(String(12))
    TYPE_DE_PO = Column(String(51))
    SYMBOLOGIE = Column(String(64))
    ANGLE = Column(Float(53))
    SYSANGLE = Column(Float(53))
    ID_SIG = Column(Integer)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class ErdfRemonteeAerosout(Base):
    __tablename__ = 'erdf_remontee_aerosout'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_remontee_aerosout_id_seq'::regclass)"))
    APPAREIL_D = Column(String(32))
    CONNEXION_ = Column(String(32))
    HAUTEUR_PO = Column(Float(53))
    INDICATEUR = Column(String(32))
    PARAFOUDRE = Column(String(32))
    PROTECTION = Column(String(7))
    REMONT_E_A = Column(String(7))
    STATUT = Column(String(12))
    SYMBOLOGIE = Column(String(64))
    ANGLE = Column(Float(53))
    SYSANGLE = Column(Float(53))
    ID_SIG = Column(Integer)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class ErdfTronconAerien(Base):
    __tablename__ = 'erdf_troncon_aerien'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    STATUT = Column(String(12))
    TECHNOLOGI = Column(String(32))
    TECHNOLOG1 = Column(String(32))
    SYMBOLOGIE = Column(String(64))
    COMMENTAIR = Column(String(30))
    geom = Column(NullType, index=True)
    ID_SIG = Column(Integer)
    id = Column(Integer, primary_key=True, server_default=text("nextval('erdf_troncon_aerien_id_seq'::regclass)"))
    geom_json = Column(String)


class OgmCablesRemonteesMecanique(Base):
    __tablename__ = 'ogm_cables_remontees_mecaniques'
    __table_args__ = (
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    geom = Column(NullType, index=True)
    OBJECTID = Column(Integer)
    idcable = Column(Integer, primary_key=True)
    TypeInfra = Column(String(50))
    NomInfra = Column(String(50))
    IdDomaine = Column(Integer)
    DateMontag = Column(DateTime)
    DateDemont = Column(DateTime)
    DateModif = Column(DateTime)
    SHAPE_Leng = Column(Float(53))
    geom_json = Column(String)


class OgmDomainesSkiable(Base):
    __tablename__ = 'ogm_domaines_skiables'
    __table_args__ = (
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    geom = Column(NullType, index=True)
    OBJECTID = Column(Integer)
    iddomaine = Column(Integer, primary_key=True)
    NomRDomain = Column(String(255))
    IdExploita = Column(Integer)
    Activite = Column(String(255))
    MoOGM = Column(String(255))
    Dpt = Column(String(100))
    NomStation = Column(String(255))
    SHAPE_Leng = Column(Float(53))
    SHAPE_Area = Column(Float(53))
    MoOGM_Vis = Column(String(255))
    Annee_Plan = Column(Integer)
    Surface_DS = Column(Integer)
    geom_json = Column(String)


class OgmTronconsDangereux(Base):
    __tablename__ = 'ogm_troncons_dangereux'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    geom = Column(NullType, index=True)
    OBJECTID = Column(Integer)
    idtd = Column(Integer, primary_key=True)
    IdCable = Column(Integer)
    Espece = Column(String(100))
    Nombre = Column(Integer)
    Estimation = Column(String(100))
    Sexe = Column(String(20))
    Age = Column(String(20))
    idPyBas = Column(String(100))
    idPyHt = Column(String(100))
    NomObs = Column(String(100))
    LongReelle = Column(Integer)
    Date_ = Column(DateTime)
    SHAPE_Leng = Column(Float(53))
    geom_json = Column(String)


class OgmTronconsVisualise(Base):
    __tablename__ = 'ogm_troncons_visualises'
    __table_args__ = (
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    geom = Column(NullType, index=True)
    OBJECTID = Column(Integer)
    idtv = Column(Integer, primary_key=True)
    IdCable = Column(Integer)
    TypeVisu = Column(String(255))
    Financeur = Column(String(255))
    Operateur = Column(String(255))
    IdPyBas = Column(String(100))
    IdPyHt = Column(String(100))
    LongReelle = Column(Integer)
    Date_visu = Column(DateTime)
    SHAPE_Leng = Column(Float(53))
    geom_json = Column(String)


class OgmTronconsVisualisesDangereux(Base):
    __tablename__ = 'ogm_troncons_visualises_dangereux'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    geom = Column(NullType, index=True)
    OBJECTID = Column(Integer)
    Espece = Column(String(100))
    Nombre = Column(Integer)
    Estimation = Column(String(100))
    Sexe = Column(String(20))
    Age = Column(String(20))
    idPyBas = Column(String(100))
    idPyHt = Column(String(100))
    NomObs = Column(String(100))
    LongReelle = Column(Integer)
    Date_ = Column(DateTime)
    idtvd = Column(Integer, primary_key=True)
    IdTV = Column(Integer)
    Shape_Leng = Column(Float(53))
    raisons = Column(String(255))
    geom_json = Column(String)


class RteLigne(Base):
    __tablename__ = 'rte_lignes'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_rte_ligne = Column(Integer, primary_key=True, server_default=text("nextval('rte_lignes_id_rte_ligne_seq'::regclass)"))
    U_MAX = Column(String(20))
    CONFIG = Column(String)
    TERNE_EX = Column(Integer)
    ADR_LIT_1 = Column(String)
    ADR_LIT_2 = Column(String)
    ADR_LIT_3 = Column(String)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class RtePoste(Base):
    __tablename__ = 'rte_postes'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_rte_poste = Column(Integer, primary_key=True, server_default=text("nextval('rte_postes_id_rte_poste_seq'::regclass)"))
    U_MAX = Column(String(20))
    LIBELLE = Column(String(64))
    LIB_SUIT = Column(String(64))
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class RtePoteaux(Base):
    __tablename__ = 'rte_poteaux'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_rte_poteaux = Column(Integer, primary_key=True, server_default=text("nextval('rte_poteaux_id_rte_poteaux_seq'::regclass)"))
    U_MAX = Column(String(20))
    NB_TERNE = Column(Integer)
    geom = Column(NullType, index=True)
    geom_json = Column(String)


class TAxesMigratoire(Base):
    __tablename__ = 't_axes_migratoires'
    __table_args__ = (
        CheckConstraint(u"((public.geometrytype(geom) = 'POLYGON'::text) OR (public.geometrytype(geom) = 'MULTIPOLYGON'::text)) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_axe_migratoire = Column(Integer, primary_key=True, server_default=text("nextval('t_axes_migratoires_id_axe_migratoire_seq'::regclass)"))
    nom_axe_migratoire = Column(String(100))
    migration = Column(Integer)
    source = Column(String(100))
    description = Column(String)
    geom = Column(NullType, nullable=False, index=True)
    geom_json = Column(String)


class TCasMortalite(Base):
    __tablename__ = 't_cas_mortalite'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_cas_mortalite = Column(Integer, primary_key=True, server_default=text("nextval('t_cas_mortalite_id_cas_mortalite_seq'::regclass)"))
    id_espece = Column(ForeignKey(u't_especes.id_espece'), nullable=False)
    source = Column(String(100))
    id_cause_mortalite = Column(ForeignKey(u'dico_cause_mortalite.id_cause_mortalite'), nullable=False)
    nb_cas = Column(Integer)
    sexe = Column(String(30))
    age = Column(String(30))
    date = Column(Date)
    geom = Column(NullType, index=True)
    geom_json = Column(String)

    dico_cause_mortalite = relationship(u'DicoCauseMortalite')
    t_espece = relationship(u'TEspece')


class TCommune(Base):
    __tablename__ = 't_communes'
    __table_args__ = (
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    insee = Column(Integer, primary_key=True)
    nom_commune = Column(String(100))
    geom = Column(NullType, nullable=False, index=True)
    geom_json = Column(String)


class TEquipementsPoteauxErdf(Base):
    __tablename__ = 't_equipements_poteaux_erdf'

    id_equipement_poteau_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_equipements_poteaux_erdf_id_equipement_poteau_erdf_seq'::regclass)"))
    id_inventaire_poteau_erdf = Column(ForeignKey(u't_inventaire_poteaux_erdf.id_inventaire_poteau_erdf', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    id_type_equipement_poteau = Column(ForeignKey(u'dico_type_equipement_poteau.id_type_equipement_poteau'))
    date_equipement = Column(Date)
    login_saisie = Column(String(25))
    mis_en_place = Column(Boolean, server_default=text("false"))
    id_nb_equipements = Column(ForeignKey(u'dico_nb_equipements.id_nb_equipements'))

    t_inventaire_poteaux_erdf = relationship(u'TInventairePoteauxErdf')
    dico_nb_equipement = relationship(u'DicoNbEquipement')
    dico_type_equipement_poteau = relationship(u'DicoTypeEquipementPoteau')


class TEquipementsTronconsErdf(Base):
    __tablename__ = 't_equipements_troncons_erdf'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_equipement_troncon_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_equipements_troncons_erdf_id_equipement_troncon_erdf_seq'::regclass)"))
    id_inventaire_troncon_erdf = Column(ForeignKey(u't_inventaire_troncons_erdf.id_inventaire_troncon_erdf', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    id_type_equipement_troncon = Column(ForeignKey(u'dico_type_equipement_troncon.id_type_equipement_troncon'))
    date_equipement_troncon = Column(Date)
    geom = Column(NullType, index=True)
    login_saisie = Column(String(25))
    geom_json = Column(String)

    t_inventaire_troncons_erdf = relationship(u'TInventaireTronconsErdf')
    dico_type_equipement_troncon = relationship(u'DicoTypeEquipementTroncon')


class TEspece(Base):
    __tablename__ = 't_especes'

    id_espece = Column(Integer, primary_key=True, server_default=text("nextval('t_especes_id_espece_seq'::regclass)"))
    nom_espece = Column(String(100), nullable=False)
    taille_zone_tampon = Column(Integer)
    code_couleur = Column(String(20))

t_v_zones_sensibles = Table(
    'v_zones_sensibles', metadata,
    Column('id_zone_sensible', Integer, primary_key=True),
    Column('nom_zone_sensible', String),
    Column('niveau_sensibilite', Integer),
    Column('nb_poteaux_inventories', BigInteger),
    Column('nb_poteaux_inventories_risque_fort', BigInteger),
    Column('nb_poteaux_inventories_risque_secondaire', BigInteger),
    Column('nb_poteaux_inventories_risque_faible', BigInteger),
    Column('nb_poteaux_equipes', BigInteger),
    Column('nb_poteaux_equipes_risque_fort', BigInteger),
    Column('nb_poteaux_equipes_risque_secondaire', BigInteger),
    Column('nb_poteaux_equipes_risque_faible', BigInteger),
    Column('m_troncons_inventories', Float(53)),
    Column('m_troncons_inventories_risque_fort', Float(53)),
    Column('m_troncons_inventories_risque_secondaire', Float(53)),
    Column('m_troncons_inventories_risque_faible', Float(53)),
    Column('m_troncons_equipes', Float(53)),
    Column('m_troncons_equipes_risque_fort', Float(53)),
    Column('m_troncons_equipes_risque_secondaire', Float(53)),
    Column('m_troncons_equipes_risque_faible', Float(53)),
    Column('geom', Text)
)
class TVZonesSensibles(object):
    pass
mapper(TVZonesSensibles, t_v_zones_sensibles)

class TInventairePoteauxErdf(Base):
    __tablename__ = 't_inventaire_poteaux_erdf'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326'),
        Index('t_inventaire_poteaux_erdf_index_id', 'id_type_poteau_erdf', 'id_type_poteau_erdf_secondaire', 'id_zone_sensible', 'id_attractivite', 'id_dangerosite')
    )

    id_inventaire_poteau_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_inventaire_poteaux_erdf_id_inventaire_poteau_erdf_seq'::regclass)"))
    date_inventaire = Column(Date)
    id_type_poteau_erdf = Column(ForeignKey(u'dico_type_poteau_erdf.id_type_poteau_erdf'))
    id_type_poteau_erdf_secondaire = Column(ForeignKey(u'dico_type_poteau_erdf.id_type_poteau_erdf'))
    remarques = Column(String)
    id_zone_sensible = Column(ForeignKey(u't_zones_sensibles.id_zone_sensible'))
    etat_poteau = Column(String)
    id_attractivite = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    id_dangerosite = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    neutralisation_prevue_isolation = Column(Boolean)
    neutralisation_prevue_dissuasion = Column(Boolean)
    neutralisation_prevue_attraction = Column(Boolean)
    deja_neutralise = Column(Boolean)
    geom = Column(NullType, index=True)
    geom_json = Column(String)
    risque_poteau = Column(String(20))
    commune = Column(String(100))
    nb_equipements = Column(Integer)
    nb_photos = Column(Integer)
    insee = Column(ForeignKey(u't_communes.insee'))

    dico_classes_risque = relationship(u'DicoClassesRisque', primaryjoin='TInventairePoteauxErdf.id_attractivite == DicoClassesRisque.id_classe_risque')
    dico_classes_risque1 = relationship(u'DicoClassesRisque', primaryjoin='TInventairePoteauxErdf.id_dangerosite == DicoClassesRisque.id_classe_risque')
    dico_type_poteau_erdf = relationship(u'DicoTypePoteauErdf', primaryjoin='TInventairePoteauxErdf.id_type_poteau_erdf == DicoTypePoteauErdf.id_type_poteau_erdf')
    dico_type_poteau_erdf1 = relationship(u'DicoTypePoteauErdf', primaryjoin='TInventairePoteauxErdf.id_type_poteau_erdf_secondaire == DicoTypePoteauErdf.id_type_poteau_erdf')
    t_zones_sensible = relationship(u'TZonesSensible', backref='poteaux')
    t_commune = relationship(u'TCommune')


class TInventaireTronconsErdf(Base):
    __tablename__ = 't_inventaire_troncons_erdf'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'LINESTRING'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326'),
        Index('t_inventaire_troncons_erdf_index_id', 'id_zone_sensible', 'id_risque_deplacement', 'id_risque_integration_topo', 'id_risque_integration_vegetation', 'id_risque_integration_bati')
    )

    id_inventaire_troncon_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_inventaire_troncons_erdf_id_inventaire_troncon_erdf_seq'::regclass)"))
    date_inventaire = Column(Date)
    id_zone_sensible = Column(ForeignKey(u't_zones_sensibles.id_zone_sensible'))
    geom = Column(NullType, index=True)
    remarques = Column(String)
    id_risque_deplacement = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    id_risque_integration_topo = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    id_risque_integration_vegetation = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    id_risque_integration_bati = Column(ForeignKey(u'dico_classes_risque.id_classe_risque'))
    deja_neutralise = Column(Boolean)
    geom_json = Column(String)
    risque_troncon = Column(String(20))
    commune = Column(String(100))
    nb_photos = Column(Integer)
    lg_equipee = Column(Float(53))
    longueur = Column(Float(53))

    dico_classes_risque = relationship(u'DicoClassesRisque', primaryjoin='TInventaireTronconsErdf.id_risque_deplacement == DicoClassesRisque.id_classe_risque')
    dico_classes_risque1 = relationship(u'DicoClassesRisque', primaryjoin='TInventaireTronconsErdf.id_risque_integration_bati == DicoClassesRisque.id_classe_risque')
    dico_classes_risque2 = relationship(u'DicoClassesRisque', primaryjoin='TInventaireTronconsErdf.id_risque_integration_topo == DicoClassesRisque.id_classe_risque')
    dico_classes_risque3 = relationship(u'DicoClassesRisque', primaryjoin='TInventaireTronconsErdf.id_risque_integration_vegetation == DicoClassesRisque.id_classe_risque')
    t_zones_sensible = relationship(u'TZonesSensible')


class TObservation(Base):
    __tablename__ = 't_observations'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2')
    )

    id_observation = Column(Integer, primary_key=True, server_default=text("nextval('t_observations_id_observation_seq'::regclass)"))
    id_espece = Column(ForeignKey(u't_especes.id_espece', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    lieu = Column(String(100))
    commentaires = Column(String)
    precision_loc = Column(String(50))
    source = Column(String(50))
    geom = Column(NullType, index=True)
    geom_json = Column(String)
    nombre = Column(Integer)
    date = Column(Date)

    t_espece = relationship(u'TEspece')


class TPhotosPoteauxErdf(Base):
    __tablename__ = 't_photos_poteaux_erdf'

    id_photo_poteau_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_photos_poteaux_erdf_id_photo_poteau_erdf_seq'::regclass)"))
    id_inventaire_poteau_erdf = Column(ForeignKey(u't_inventaire_poteaux_erdf.id_inventaire_poteau_erdf', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    chemin_photo = Column(String)
    commentaire = Column(String)
    neutralise = Column(Boolean)
    auteur = Column(String)

    t_inventaire_poteaux_erdf = relationship(u'TInventairePoteauxErdf')


class TPhotosTronconsErdf(Base):
    __tablename__ = 't_photos_troncons_erdf'

    id_photo_troncon_erdf = Column(Integer, primary_key=True, server_default=text("nextval('t_photos_troncons_erdf_id_photo_troncon_erdf_seq'::regclass)"))
    id_inventaire_troncon_erdf = Column(ForeignKey(u't_inventaire_troncons_erdf.id_inventaire_troncon_erdf', ondelete=u'CASCADE', onupdate=u'CASCADE'))
    chemin_photo = Column(String)
    commentaire = Column(String)
    neutralise = Column(Boolean)
    auteur = Column(String)

    t_inventaire_troncons_erdf = relationship(u'TInventaireTronconsErdf')


class TSitesNidification(Base):
    __tablename__ = 't_sites_nidification'
    __table_args__ = (
        CheckConstraint(u"(public.geometrytype(geom) = 'POINT'::text) OR (geom IS NULL)"),
        CheckConstraint(u'public.st_ndims(geom) = 2'),
        CheckConstraint(u'public.st_srid(geom) = 4326')
    )

    id_site_nidification = Column(Integer, primary_key=True, server_default=text("nextval('t_sites_nidification_id_site_nidification_seq'::regclass)"))
    id_espece = Column(ForeignKey(u't_especes.id_espece', ondelete=u'CASCADE', onupdate=u'CASCADE'), nullable=False)
    lieu = Column(String(100))
    nidification_10_ans = Column(Boolean)
    commentaires = Column(String)
    precision_loc = Column(String(50))
    source = Column(String(50))
    geom = Column(NullType, index=True)
    geom_json = Column(String)

    t_espece = relationship(u'TEspece')


class TZonesSensible(Base):
    __tablename__ = 't_zones_sensibles'

    id_zone_sensible = Column(Integer, primary_key=True, server_default=text("nextval('t_zone_sensible_id_zone_sensible_seq'::regclass)"))
    nom_zone_sensible = Column(String)
    niveau_sensibilite = Column(Integer)


t_v_equipements_poteaux = Table(
    'v_equipements_poteaux', metadata,
    Column('id', Integer, primary_key=True),
    Column('id_inventaire_poteau_erdf', Integer),
    Column('nom_type_equipement_poteau', String),
    Column('id_nb_equipements', Integer),
    Column('mis_en_place', Boolean),
    Column('date_equipement', Date),
    Column('geom_json', String)
)
class TVEquipementsPoteaux(object):
    pass
mapper(TVEquipementsPoteaux, t_v_equipements_poteaux)


t_v_sites_nidification_zone_tampon = Table(
    'v_sites_nidification_zone_tampon', metadata,
    Column('id_espece', Integer),
    Column('nom_espece', String(100)),
    Column('geom', NullType),
    Column('geom_json', Text)
)


t_v_zones_sensibles_poteaux = Table(
    'v_zones_sensibles_poteaux', metadata,
    Column('id_zone_sensible', Integer),
    Column('nb_poteaux_inventories', BigInteger),
    Column('nb_poteaux_inventories_risque_fort', BigInteger),
    Column('nb_poteaux_inventories_risque_secondaire', BigInteger),
    Column('nb_poteaux_inventories_risque_faible', BigInteger),
    Column('nb_poteaux_equipes', BigInteger),
    Column('nb_poteaux_equipes_risque_fort', BigInteger),
    Column('nb_poteaux_equipes_risque_secondaire', BigInteger),
    Column('nb_poteaux_equipes_risque_faible', BigInteger),
    Column('geom', NullType)
)


t_v_zones_sensibles_troncons = Table(
    'v_zones_sensibles_troncons', metadata,
    Column('id_zone_sensible', Integer),
    Column('m_troncons_inventories', Float(53)),
    Column('m_troncons_inventories_risque_fort', Float(53)),
    Column('m_troncons_inventories_risque_secondaire', Float(53)),
    Column('m_troncons_inventories_risque_faible', Float(53)),
    Column('m_troncons_equipes', Float(53)),
    Column('m_troncons_equipes_risque_fort', Float(53)),
    Column('m_troncons_equipes_risque_secondaire', Float(53)),
    Column('m_troncons_equipes_risque_faible', Float(53)),
    Column('geom', NullType)
)

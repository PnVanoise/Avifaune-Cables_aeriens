# Avifaune/Câbles aériens

Développement d'une nouvelle version de l'application.

### Installation

```console
$ python bootstrap.py
$ buildout/bin/buildout
```

### Configuration

 Renseigner le(s) fichier(s) development.ini (production.ini) avec les paramètres de connexion à la base:
 - clef: `sqlalchemy.url`
 - format: `postgresql://user:pass@host:port/base`


### Déploiement

#### Avec paster (développement)

```console
$ buildout/bin/pserve development.ini
```

#### Avec apache (production)

 - Inclure le fichier de configuration apache: `apache/wsgi.conf`

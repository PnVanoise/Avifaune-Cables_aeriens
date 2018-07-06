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

 - Inclure le fichier de configuration apache: `apache/wsgi.conf`. Ce fichier est généré via le `buildout`, les éventuelles modifications seront donc à porter sur le fichier `apache/wsgi.conf.in` afin de ne pas être écrasées par un `buildout` ultérieur.

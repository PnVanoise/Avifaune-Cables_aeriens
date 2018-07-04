# Avifaune/Câbles aériens

Développement d'une nouvelle version de l'application.

## Installation

```console
$ python bootstrap.py
$ buildout/bin/buildout
```

## Déploiement

### Avec paster (développement)

```console
$ buildout/bin/pserve development.ini
```

### Avec apache (production)

 - Inclure le fichier de configuration apache: `apache/wsgi.conf`

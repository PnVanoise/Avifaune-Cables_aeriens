import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.md')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid_mako',
    'pyramid_ipython',
    'pyramid',
    'psycopg2',
    'SQLAlchemy',
    'SQLAHelper',
    'pyramid_tm',
    'PasteScript',
    'pyramid_debugtoolbar',
    'ordereddict',
    'PyYAML',
    'pyramid_beaker',
    'GeoAlchemy2',
    'backports.shutil_get_terminal_size',
    'pexpect',
    'pathlib2',
    'six',
    'enum',
    'pgcli',
    'sqlacodegen',
    'numpy',
    'ipdb',
    'traitlets',
    'ipython',
    'enum',
]

test_requires = requires.extend(['WebTest',
                                 'pyquery',
                                 'mock',
                                 'nose>=1.2.1',
                                 'nosexcover',
                                 'nose-progressive',
                                 'coverage',
                                 'nose-testconfig',
                                 'BeautifulSoup'])

setup(name='Cables',
      version='0.0',
      description='Cables',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pyramid pylons',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=test_requires,
      test_suite="cables",
      entry_points="""\
      [paste.app_factory]
      main = cables:main
      """,
      )

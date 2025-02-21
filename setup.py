import setuptools
from babel.messages.frontend import compile_catalog

c = compile_catalog()
c.directory = 'transmission_rutracker_seed/locale'
c.domain = ['messages']
c.run()

setuptools.setup()

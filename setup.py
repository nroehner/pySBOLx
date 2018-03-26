from setuptools import setup

install_requires=['rdflib', 'pysbol']

setup(name='pySBOLx',
      version='0.1',
      description='pysbol extended to support experimental data representation.',
      url='https://github.com/SD2E/data-representation/sbol/pySBOLx',
      author='Nicholas Roehner',
      author_email='nicholasroehner@gmail.com',
      packages=['pySBOLx'],
      install_requires=install_requires,
      zip_safe=False)
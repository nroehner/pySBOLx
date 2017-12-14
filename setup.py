from setuptools import setup

setup(name='pySBOLx',
      version='0.1',
      description='pysbol extended to support experimental data representation (built for 64-bit Windows and Python 3).',
      url='https://github.com/SD2E/data-representation/sbol/pySBOLx_Win_64_3/pySBOLx',
      author='Nicholas Roehner',
      author_email='nicholasroehner@gmail.com',
      packages=['pySBOLx'],
      install_requires=[
          'rdflib',
          'sbol'
      ],
      dependency_links=['git+https://git@github.com/nroehner/pySBOL_Win_64_3.git#egg=sbol'],
      zip_safe=False)
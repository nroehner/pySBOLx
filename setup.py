from setuptools import setup

install_requires=['rdflib']

if sys.platform in {'win32'}:
  install_requires.append('sbol')
else:
  install_requires.append('pysbol')

setup(name='pySBOLx',
      version='0.1',
      description='pysbol extended to support experimental data representation.',
      url='https://github.com/SD2E/data-representation/sbol/pySBOLx',
      author='Nicholas Roehner',
      author_email='nicholasroehner@gmail.com',
      packages=['pySBOLx'],
      install_requires=install_requires,
      dependency_links=[
        'git+https://git@github.com/nroehner/pySBOL_Win_64_3.git#egg=sbol'
      ],
      zip_safe=False)
from setuptools import setup

setup(
      name             = 'refex',
      version          = '0.0.1',
      description      = 'Database cross-referencing tool.',
      long_description = open('README.md').read(),
      license          = 'MIT',
      url              = 'http://github.com/tmp-usr/biodb/',
      author           = 'Kemal Sanli',
      author_email     = 'kemalsanli1@gmail.com',
      classifiers      = ['Topic :: Scientific/Engineering :: Bio-Informatics'],
      packages         = ['refex', 
                          'refex/mapping',
                          'refex/gsea',
                          'refex/gsea/gene_sets'
                          'refex/sqling',
                          ],
     
      include_package_data = True,
      package_data = {'biodb': [
                          'refex/mapping/refex.db',
          ] } ,      
      install_requires = ['storm'],
)

from setuptools import setup
readme = open('README.rst').read()

setup(name='marbaloo_sqlalchemy',
      version='0.1.0',
      description='SQLAlchemy support for cherrypy.',
      long_description=readme,
      url='http://github.com/marbaloo/marbaloo_sqlalchemy',
      author='Mahdi Ghane.g',
      license='MIT',
      keywords='sqlalchemy cherrypy marbaloo marbaloo_sqlalchemy',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Framework :: CherryPy',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX :: Linux',
          'Operating System :: Unix',
          'Programming Language :: Python :: 3 :: Only',
          'Topic :: Software Development :: Libraries'
      ],
      install_requires=[
          'cherrypy>=8.1.2',
          'sqlalchemy>=1.1.0'
      ],
      packages=['marbaloo_sqlalchemy'],
      )

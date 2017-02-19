Marbaloo SQLAlchemy
===================

`sqlalchemy <http://www.sqlalchemy.org//>`_ support for cherrypy.

Installation
------------
::

    pip install marbaloo_sqlalchemy

Usage
-----

::

    # app.py
    import marbaloo_sqlalchemy
    import cherrypy
    import os
    from your_models import messages_model
    marbaloo_sqlalchemy.Plugin(cherrypy.engine).subscribe()
    cherrypy.tools.db = marbaloo_sqlalchemy.Tool()


    class Root(object):

        @cherrypy.expose
        def index(self):
            db_session1 = cherrypy.request.db['db1']
            db_session2 = cherrypy.request.db['db2']

            query = messages_model.insert().values(message='TESTMessage')
            db_session1.get_bind().execute(query)
            db_session1.commit()

            query = messages_model.insert().values(message='TESTMessage')
            db_session2.get_bind().execute(query)
            db_session2.commit()

    config = {
        'global': {
            'marbaloo_sqlalchemy_db': {
                'db1': {
                    'engine': {
                        'name_or_url': 'sqlite:///test1.db',
                        'echo': True,
                    },
                    'session': {
                        'expire_on_commit': True,
                        'autoflush': True,
                        'autocommit': False
                    }
                },
                'db2': {
                    'engine': {
                        'name_or_url': 'sqlite:///test2.db',
                        'echo': True,
                    },
                    'session': {
                        'expire_on_commit': True,
                        'autoflush': True,
                        'autocommit': False
                    }
                },
            }
        },
        '/': {
            'tools.db.on': True
        }
    }
    cherrypy.quickstart(Root(), '/', config)

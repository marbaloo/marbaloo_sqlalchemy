import cherrypy
import os
from cherrypy.test import helper


class CPTest(helper.CPWebCase):

    def setup_server():
        import marbaloo_sqlalchemy

        from sqlalchemy import MetaData, Column, Table, exc
        from sqlalchemy.types import UnicodeText, Integer
        metadata2 = MetaData()
        messages_model = Table(
            'messages', metadata2,
            Column('id', Integer, primary_key=True, autoincrement=True),
            Column('message', UnicodeText(), nullable=False)
        )
        marbaloo_sqlalchemy.Plugin(cherrypy.engine).subscribe()
        cherrypy.tools.db = marbaloo_sqlalchemy.Tool()

        class Root(object):
            @cherrypy.expose
            def index(self):
                db_session1 = cherrypy.request.db['db1']
                db_session2 = cherrypy.request.db['db2']
                # metadata2.create_all(bind=db_session1.get_bind())
                # metadata2.create_all(bind=db_session2.get_bind())
                # metadata2.reflect(bind=db_session1.get_bind())
                # metadata2.reflect(bind=db_session2.get_bind())

                try:
                    query = messages_model.insert().values(message='hello world')
                    db_session1.get_bind().execute(query)
                    db_session1.commit()
                    query = messages_model.insert().values(message='hello world')
                    db_session2.get_bind().execute(query)
                    db_session2.commit()
                except exc.SQLAlchemyError:
                    return 'fail'
                return 'success'

        root_path = os.path.dirname(__file__)
        db_path1 = os.path.join(root_path, 'db1.db')
        db_path2 = os.path.join(root_path, 'db2.db')
        cherrypy.config['marbaloo_sqlalchemy_db'] = {
            'db1': {
                'engine': {
                    'name_or_url': 'sqlite:///%s' % db_path1,
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
                    'name_or_url': 'sqlite:///%s' % db_path2,
                    'echo': True,
                },
                'session': {
                    'expire_on_commit': True,
                    'autoflush': True,
                    'autocommit': False
                }
            },
        }

        cherrypy.tree.mount(Root(), '/', {
                                '/': {
                                    'tools.db.on': True
                                }
                            })
    setup_server = staticmethod(setup_server)

    def test_simple(self):
        self.getPage("/")
        self.assertStatus('200 OK')
        self.assertHeader('Content-Type', 'text/html;charset=utf-8')
        self.assertBody('success')

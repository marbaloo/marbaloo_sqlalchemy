import cherrypy
from cherrypy.process import plugins
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['Plugin', 'Tool']


class Plugin(plugins.SimplePlugin):
    def __init__(self, bus):
        plugins.SimplePlugin.__init__(self, bus)
        self.sessions = {}

    def start(self):
        if cherrypy.config.get('marbaloo_sqlalchemy_db') is not None:
            for db_alias, db_spec in cherrypy.config.get('marbaloo_sqlalchemy_db').items():
                self.bus.log('Starting up DB[%s] access' % db_alias)
                sa_engine = create_engine(**db_spec['engine'])
                db_spec['session']['bind'] = sa_engine
                self.sessions[db_alias] = scoped_session(sessionmaker(**db_spec['session']))
            self.bus.subscribe('get-db-sessions', self.get_sessions)
        else:
            print('sqlalchemy databases is not set.')
            raise Exception

    def stop(self):
        self.bus.unsubscribe('get-db-sessions', self.get_sessions)
        for db_alias, db_spec in cherrypy.config.get('marbaloo_sqlalchemy_db').items():
            self.bus.log('Stopping down DB[%s] access' % db_alias)
            self.sessions[db_alias].get_bind().dispose()
            self.sessions[db_alias].close()
            self.sessions[db_alias] = None

    def get_sessions(self):
        return self.sessions


class Tool(cherrypy.Tool):
    def __init__(self):
        cherrypy.Tool.__init__(self, 'on_start_resource',
                               self.bind_session,
                               priority=2)

    @staticmethod
    def bind_session():
        cherrypy.request.db = {}
        for db_alias, session in cherrypy.engine.publish('get-db-sessions').pop().items():
            cherrypy.request.db[db_alias] = session

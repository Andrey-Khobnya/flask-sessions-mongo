# Copyright (c) 2013, Andrey Khobnya
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice,
#   this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import datetime
import pickle
import base64
import os
from M2Crypto import m2
from flask.sessions import SessionInterface, SessionMixin

m2.rand_seed(os.urandom(16))

def sessions_mongo(app):
    """Initialize the `app` for use with :class:`~MongoSessionInterface`
    
    The app is configured according to the configuration variables
    ``SESSION_MONGO_PREIX`` (prefix of :class:`~PyMongo` instance. Defaults 
    to "MONGO"), ``SESSION_MONGO_COLLECTION`` (name of Mongo collection 
    for sessions. Defaults to "sessions"). To set up session expiration 
    time use db.sessions.ensureIndex( { 'accessTime': 1 }, { 
    'expireAfterSeconds': 3600 } in your Mongo shell.
    
    :param flask.Flask app: the application to configure for use with
        :class:`~MongoSessionInterface`
    """
    if app is None:
        return
    app.config.setdefault('SESSION_MONGO_PREIX', 'MONGO')
    app.config.setdefault('SESSION_MONGO_COLLECTION', 'sessions')
    mongo_sessions = MongoSessionInterface(
        app.extensions['pymongo'][app.config['SESSION_MONGO_PREIX']][1],
        app.config['SESSION_MONGO_COLLECTION'])
    app.session_interface = mongo_sessions  
    

class MongoSession(dict, SessionMixin):

    def __init__(self, initial=dict(), mongo_id=None, sid=None, new=False):
        dict.__init__(self, initial)
        self.mongo_id = mongo_id
        self.sid = sid
        self.new = new


class MongoSessionInterface(SessionInterface):
    serializer = pickle

    def __init__(self, db, collection_name):
        self.db = db
        self.collection_name = collection_name

    def generate_sid(self, size=16):
        return base64.b64encode(m2.rand_bytes(size))

    def open_session(self, app, request):
        sid = request.cookies.get(app.session_cookie_name)
        if not sid:
            sid = self.generate_sid()
            return MongoSession(sid=sid, new=True)
        data = self.db[self.collection_name].find_one({'sid': sid})
        if data is not None:
            return MongoSession(
                self.serializer.loads(data['data']),
                mongo_id = data['_id'],
                sid=sid)
        return MongoSession(sid=sid, new=True)

    def save_session(self, app, session, response):
        session_record = {
            'data':  self.serializer.dumps(dict(session)),
            'sid': session.sid,
            'accessTime': datetime.datetime.utcnow()}
        if session.mongo_id is not None:
            session_record['_id'] = session.mongo_id
        self.db[self.collection_name].save(session_record)
        response.set_cookie(app.session_cookie_name,
            session.sid,
            expires=self.get_expiration_time(app, session),
            httponly=True,
            domain=self.get_cookie_domain(app))
        
1) Set a [TTL](http://docs.mongodb.org/manual/tutorial/expire-data/) on your sessions collection using command like the following example at the mongo shell:

```javascript
db.sessions.ensureIndex( { "accessTime": 1 }, { "expireAfterSeconds": 1800 } )
```

2) Config and enable *flask-sessions-mongo* in your application:

```python
# ...
from flask_pymongo import PyMongo
from flask_sessions_mongo import sessions_mongo

app = Flask(__name__)

# config flask-pymongo
app.config['MONGO_DBNAME'] = 'exampledb'
mongo = PyMongo(app)

# config flask-sessions-mongo
# prefix of PyMongo instance. Defaults to "MONGO"
app.config['SESSION_MONGO_PREIX'] = 'MONGO'
# name of sessions collection. Defaults to "sessions"
app.config['SESSION_MONGO_COLLECTION'] = 'sessions'
    
# enable flask-sessions-mongo
sessions_mongo(app)

#...
```
    
3) Enjoy! If you need scaling, you can use *sid* as sharding key.

from models import using_mongo

mng = using_mongo()
uri = 'mongodb://localhost:27017'


if __name__ == '__main__':
    mng.mongo_connect(uri)
    mng.add_user(98)
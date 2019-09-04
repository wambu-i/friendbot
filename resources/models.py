from pymongo import MongoClient
import os
import logging

formatter = '[%(asctime)-15s] %(levelname)s [%(filename)s.%(funcName)s#L%(lineno)d] - %(message)s'

logging.basicConfig(level = logging.DEBUG, format = formatter)

logger = logging.getLogger("database")


class using_mongo:
    def __init__(self):
        self.db = ''

    def mongo_connect(self, uri):
        try:
            client = MongoClient(uri)
            self.db = client['aarifu']
            user = os.environ.get('USER', None)
            pwd = os.environ.get('PWD', None)
            logger.info("Connection to database successful!")
            return self.db
        
        except Exception as e:
            logger.warning('Could not connect to database')
            logger.error(e, exec_info = True)

    def add_user(self, id):
        subscribe = False
        collection = self.db['interactions']
        user =  collection.find_one({'s_id': id})
        if user is not None:
            logger.info('User already subscribed!')
            subscribe = True
        else:
            collection.insert({'s_id': id})
            subscribe = False
        return subscribe
    
    def add_user_role(self, id, role):
        added = False
        collection = self.db['interactions']
        user = collection.find_one({'s_id': id})
        if user is not None:
            collection.update_one({'s_id': id}, {'$set': {'role': role}})
            logger.info("User successfully defined in database.")
            added = True
        else:
            collection.insert_one({'s_id': id, 'role': role})
            added = True
        return added
            
            

    def check_subscribed(self, id):
        subscribe = False
        collection = self.db['interactions']
        user =  collection.find_one({'s_id': id})
        if user is not None:
            logger.info('User already subscribed!')
            subscribe = True
        else:
            collection.insert({'s_id': id})
            subscribe = False
        return subscribe


    def unsubscribe(self, id):
        unsubscribe = False
        collection = self.db['interactions']
        user =  collection.find_one({'s_id': id})
        if user is not None:
            collection.delete_one({'s_id' : id})
            logger.info("User successfully unsubscribed!")
            unsubscribe = True
        else:
            unsubscribe = False
        return unsubscribe

    def add_response(self, id, url):
        collection = self.db['interactions']
        user = collection.find_one({'u_id': id})
        if user is not None:
            posts = user['postID']
            if postID not in posts:
                collection.update_one({'u_id': id}, {'$push': {'postID': postID}})
            else:
                print('Already added')
        else:
            collection.insert({'u_id' : id, 'postID': [postID]})

"""     def saveChallenge(self, id, postID):
        collection = self.db['saved']
        user = collection.find_one({'u_id': id})
        if user is not None:
            posts = user['postID']
            if postID not in posts:
                collection.update_one({'u_id': id}, {'$push': {'postID': postID}})
            else:
                print('Already saved')
        else:
            collection.insert({'u_id' : id, 'postID': [postID]})


    def subscribedUsers(self):
        collection = self.db['subbed']
        users = collection.find({})
        subs = []
        if users is not None:
            for user in users:
                subs.append(user)
            return subs
        else: 
            return subs

    def sentPosts(self, id):
        collection = self.db['posts']
        user = collection.find_one({'u_id': id})
        if user is not None:
            posts = user['postID']
            return posts
        else:
            posts = []
            return posts

    def savedPosts(self, id):
        collection = self.db['saved']
        user = collection.find_one({'u_id' : id})
        if user is not None:
            posts = user['postID']
            return posts
        else:
            posts = []
            return posts

    def solve(self, id, postID):
        collection = self.db['solved']
        user = collection.find_one({'u_id': id})
        if user is not None:
            posts = user['postID']
            if postID not in posts:
                collection.update_one({'u_id': id}, {'$push': {'postID': postID}})
            else:
                print('Already solved')
        else:
            collection.insert_one({'u_id' : id, 'postID': [postID]})


    def solvedPosts(self, id):
        collection = self.db['solved']
        user = collection.find_one({'u_id' : id})
        if user is not None:
            posts = user['postID']
            return posts
        else:
            posts = []
            return posts

    def save_solutions(self, id, post, content):
        collection = self.db['solutions']
        user = collection.find_one({'u_id' : id})
        if user is not None:
            collection.update_one({'u_id' : id}, {'$set' : {post: content}})
        else:
            collection.insert_one({'u_id' : id, post: content})

    def get_solution(self, id, post):
        collection = self.db['solutions']
        user = collection.find_one({'u_id' : id})
        if user is not None:
            content = user[post]
            return content
        else:
            content = ''
            return content """
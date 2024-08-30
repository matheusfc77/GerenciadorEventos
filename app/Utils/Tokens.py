import pymongo
import pandas as pd

class Tokens:

    def __init__(self):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["test_mongo"]
        mycol = mydb["tokens"]
        mydoc = mycol.find()

        lt_tokens = [(tk['token'], tk['level_acess']) for tk in mydoc]
        self.df_tokens = pd.DataFrame(lt_tokens, columns=['tokens', 'level_acess'])


    def token_is_exist(self, token):
        return self.df_tokens[self.df_tokens['tokens'] == token].shape[0] > 0
    

    def token_is_admin(self, token):
        return (
            self.token_is_exist(token) and 
            self.df_tokens[(self.df_tokens['tokens'] == token) & (self.df_tokens['level_acess'] == 'admin')].shape[0] > 0
        )
from sqlalchemy.orm import Query
'''
https://stackoverflow.com/questions/15936111/sqlalchemy-can-you-add-custom-methods-to-the-query-object
'''
class CustomQuery(Query):
    def filter_if(self: Query, condition: bool, *criterion):
        if condition:
            return self.filter(*criterion)
        else:
            return self
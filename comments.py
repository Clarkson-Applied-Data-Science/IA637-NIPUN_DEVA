from QueryManager import QueryManager
from baseObject import baseObject
from datetime import datetime

class comments(baseObject):
    def __init__(self):
        self.setup()
        self.errors = [] 
        self.queryManager=QueryManager()

    def validate(self,n=0):
        self.errors = []      
        if not self.data[n].get('content'):
            self.errors.append("content cannot be blank.")
        
        # Updated On
        self.data[n]['updated_on'] = datetime.now().strftime("%Y-%m-%d")

        # Task ID
        if not self.data[n].get('task_id'):
            self.errors.append("Task ID cannot be blank.")


        # user ID
        if not self.data[n].get('user_id'):
            self.errors.append("User ID cannot be blank.")

        return len(self.errors)==0

    def get_comment_user_details(self,task_id):
        query=self.queryManager.get_query('get_comment_user_details')
        self.cur.execute(query,(task_id,))
        return self.cur.fetchall()
        
                    
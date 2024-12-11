from baseObject import baseObject
from QueryManager import QueryManager


class userTask(baseObject):
    def __init__(self):
        self.setup()
        self.errors = []

    def validate(self, n=0):
        print("validation in user tasks")
        self.errors = []
        # Task ID
        if not self.data[n].get('task_id'):
            self.errors.append("Task ID cannot be blank.")

        # User ID
        if not self.data[n].get('user_id'):
            self.errors.append("User ID cannot be blank.")

        return len(self.errors) == 0


    def get_user_and_task_details(self):
        queryManager=QueryManager()
        return queryManager.get_query('get_user_and_task_details')

    def delete_user_and_task_details(self):
        queryManager = QueryManager()
        return queryManager.get_query('delete_user_and_task_details')


from datetime import datetime
from baseObject import baseObject
from QueryManager import QueryManager


class task(baseObject):
    def __init__(self):  
        self.setup()      
        self.errors = [] 
        self.allowed_statuses = ["Not Started", "In Progress", "Completed"]
        self.allowed_priorities = ["Low", "Medium", "High"]
        self.queryManager=QueryManager()

    def validate(self,n=0):
        print("validation started")
        self.errors = []      
        print(self.data[n])
        if not self.data[n].get('task_name'):           
            self.errors.append("Task name cannot be blank.")     
       
        if not self.data[n].get('description'):
            self.errors.append("Description cannot be blank.")
      
        if not self.data[n].get('status') in self.allowed_statuses:
            self.errors.append(f"Status must be one of {self.allowed_statuses}.")

        # Created On
        if not self.data[n].get('created_on'):
            self.errors.append("Created On date cannot be blank.")

        elif not self.is_valid_date(self.data[n]['created_on']):
            self.errors.append("Created On date is invalid.")

        # Due Date
        if not self.data[n].get('due_date'):
            self.errors.append("Due Date cannot be blank.")
        elif not self.is_valid_date(self.data[n]['due_date']):
            self.errors.append("Due Date is invalid.")
        elif self.data[n]['created_on'] and self.data[n]['due_date']:
            if self.data[n]['due_date'] < self.data[n]['created_on']:
                self.errors.append("Due Date cannot be earlier than Created On date")
                raise ValueError("Due Date cannot be earlier than Created On date")

        # Updated On
        self.data[n]['updated_on'] = datetime.now().strftime("%Y-%m-%d")

        # Priority
        if not self.data[n].get('priority') in self.allowed_priorities:
            print('priority check')
            self.errors.append(f"Priority must be one of {self.allowed_priorities}.")

        # # Total Hours
        # if not self.data[n].get('total_hours') or self.data[n]['total_hours'] <= 0:
        #     self.errors.append("Total Hours must be greater than 0")
        #     raise ValueError("Total Hours must be greater than 0")


        # # Logged Hours
        # if not self.data[n].get('logged_hours') or self.data[n]['logged_hours'] < 0:
        #     self.errors.append("Logged Hours cannot be negative")
        #     raise ValueError("Logged Hours cannot be negative")     
        # print("flag status",len(self.errors) == 0)
        return len(self.errors) == 0


    def is_valid_date(self, date_str):
        if isinstance(date_str, datetime):
            return True
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def get_task_details(self):
        queryManager=QueryManager()
        return queryManager.get_query('get_task_details')
    
    def get_task_comments_user_details(self,task_id):
        query=self.queryManager.get_query('get_task_comments_user_details')
        result=self.cur.execute(query,(task_id,))
        return result



    def get_task_analysis(self):
        query=self.queryManager.get_query('get_task_analysis')
        self.cur.execute(query)
        return self.cur.fetchall()



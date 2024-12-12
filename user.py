import hashlib, re
from baseObject import baseObject
from datetime import datetime
from QueryManager import QueryManager


class user(baseObject):
    def __init__(self):
        self.setup()
        self.roles = [{'value': 'admin', 'text': 'admin'}, {'value': 'employee', 'text': 'employee'},
                      {'value': 'manager', 'text': 'manager'}]
        self.active = ['Yes', 'No']

    def hashPassword(self, pw):
        pw = pw + 'xyz'
        return hashlib.md5(pw.encode('utf-8')).hexdigest()

    def verify_new(self, flag=False, n=0):
        self.errors = []

        if not flag:
            u = user()
            u.getByField('name', self.data[n]['name'])
            if len(u.data) > 0:
                self.errors.append('Name already in use.')

        if self.data[n]['name'] == '':
            self.errors.append('Name cannot be blank.')

        if self.data[n]['password'] != self.data[n]['password2']:
            self.errors.append('Retyped password must match.')
 

        if len(self.data[n]['password']) < 3:
            self.errors.append('Password needs to be more than 3 chars.')
           
        else:
            self.data[n]['password'] = self.hashPassword(self.data[n]['password'])

        rl = []
        for role in self.roles:
            rl.append(role['value'])
        if self.data[n]['role'] not in rl:
            self.errors.append(f'Role must be one of {rl}')

        if self.data[n]['doj'] is None:
            self.errors.append('Date of joining cannot be blank')
        else:
            doj = self.data[n]['doj']
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", doj):
                self.errors.append('Invalid date format. Please enter in YYYY-MM-DD format.')

        if self.data[n]['Active'] is None:
            self.errors.append('Employee status cannot be empty')
        if self.data[n]['Active'] not in self.active:
            self.errors.append('Employee status needs to be be empty')

        return len(self.errors) == 0

    def verify_update(self, n=0):
        self.errors = []

        if self.data[n]['name'] == '':
            self.errors.append('Name cannot be blank.')
        else:
            u = user()
            u.getByField('name', self.data[n]['name'])
            if len(u.data) > 0 and u.data[0][u.pk] != self.data[n][self.pk]:
                self.errors.append('Name already in use.')

        if len(self.data[n]['password']) < 3:
            self.errors.append('Password needs to be more than 3 chars.')
        else:
            self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
        rl = []
        for role in self.roles:
            rl.append(role['value'])
        if self.data[n]['role'] not in rl:
            self.errors.append(f'Role must be one of {rl}')
        if 'password2' in self.data[n].keys():  # user intends to change pw
            self.data[n]['password2'] = self.hashPassword(self.data[n]['password2'])
            if self.data[n]['password'] != self.data[n]['password2']:
                self.errors.append('Retyped password must match.')
            if len(self.data[n]['password']) < 3:
                self.errors.append('Password must be > 2 chars.')
            else:
                self.data[n]['password'] = self.hashPassword(self.data[n]['password'])
        else:
            del self.data[n]['password']

        if self.data[n]['doj'] is None:
            self.errors.append('Date of joining cannot be blank')
        else:
            doj = self.data[n]['doj']
            if not re.match(r"^\d{4}-\d{2}-\d{2}$", doj):
                self.errors.append('Invalid date format. Please enter in YYYY-MM-DD format.')

        if self.data[n]['Active'] is None:
            self.errors.append('Employee status cannot be empty')
        if self.data[n]['Active'] not in self.active:
            self.errors.append('Employee status needs to be be empty')

        ##Include this in verify:
        return len(self.errors) == 0

    def tryLogin(self, name, password):
        self.errors = []
        pwd = self.hashPassword(password)

        sql = f"Select * from `{self.tn}` where `name` = %s AND `password` = %s;"

        self.cur.execute(sql, (name, pwd))
        self.data = []

        for row in self.cur:
            self.data.append(row)

        if len(self.data) == 1:
            return True, self.data[0]['role'], self.data[0]['user_id']
     

    def get_task_per_user_details(self):
        queryManager = QueryManager()
        return queryManager.get_query('get_task_per_user_details')

    def get_tasks_on_user_details(self):
        queryManager = QueryManager()
        return queryManager.get_query('get_tasks_on_user_details')

    def delete_user(self, user_id):
        queryManager = QueryManager()
        query = queryManager.get_query('update_user_status')
        try:
            self.cur.execute(query, (user_id,))
            print(f'User deleted with user id-> {user_id}')
        except Exception as e:
            print(f"deletion failed due to: {e}")

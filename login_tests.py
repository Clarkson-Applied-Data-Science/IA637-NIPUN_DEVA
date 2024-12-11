from user import user
from baseObject import baseObject
from datetime import datetime

# 1
u = user()
# u.truncate()
u.set({'name':'admin_1','password':'101','password2':'101','role':'admin', 'doj' : '2024-10-10'})
if u.verify_new():
    u.insert()
else:
    print(u.errors[0])

u = user()
if u.tryLogin("admin_1","101"):
    print("Login successful.")
else:
    print("Login failed! \nUsername and password you entered does not exist, please check and try again!")

#2
u = user()
# u.truncate()
u.set({'name':'manager_1','password':'101','password2':'101','role':'manager', 'doj' : '2024-11-11'})
if u.verify_new():
    u.insert()
else:
    print(u.errors[0])

u = user()
if u.tryLogin("manager_1","101"):
    print("Login successful.")
else:
    print(u.errors[0])

#3
u = user()
# u.truncate()
u.set({'name':'employee_1','password':'101','password2':'101','role':'employee', 'doj' : '2024-11-13'})
if u.verify_new():
    u.insert()
else:
    print(u.errors[0])

u = user()
if u.tryLogin("employee_1","101"):
    print("Login successful.")
else:
    print(u.errors[0])


#4
u = user()
# u.truncate()
u.set({'name':'employee_2','password':'101','password2':'101','role':'employee', 'doj' : '2024-11-14'})
if u.verify_new():
    u.insert()
else:
    print(u.errors[0])

u = user()
if u.tryLogin("employee_2","101"):
    print("Login successful.")
else:
    print(u.errors[0])

#5
u = user()
# u.truncate()
u.set({'name':'employee_2_updated','password':'101','password2':'101','role':'employee', 'doj' : '2024-11-111'})
if u.verify_update():
    u.update()
else:
    print(u.errors[0])

u = user()
if u.tryLogin("employee_2","101"):
    print("Login successful.")
else:
    print(u.errors[0])

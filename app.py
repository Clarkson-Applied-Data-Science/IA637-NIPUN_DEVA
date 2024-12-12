from flask import Flask, flash, render_template, Response, request, redirect, url_for, session
import datetime
import logging
# import configparser
from user import user
from task import task
from usertask import userTask
from comments import comments

# Configure logging
logging.basicConfig(filename='flask_app.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__, static_url_path='')
app.secret_key = '1234'


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        u = user()

        try:
            status, role, uid = u.tryLogin(username, password)

            if status:

                # print(u.data)
                if role == 'admin':
                    return redirect(url_for('admin_view'))
                if role == 'manager':
                    return redirect(url_for('manager_view', user_id=uid))
                else:
                    # print('iin else ')  
                    return redirect(url_for('dashboard', user_id=uid))

        except Exception as e:
            print(f"Error during login: {e}")
            flash('Invalid username or password. Please try again.', 'danger')
            flash('Don\'t have an account? Contact Admin', 'info')

    return render_template('login.html')


### Admin Stuff
@app.route('/register', methods=['GET', 'POST'])
def register():
    userObj = user()

    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            username = request.form.get('username')
            password = request.form.get('password')
            password2 = request.form.get('password2')
            role = request.form.get('role')
            doj = request.form.get('doj')
            print(type(doj))
            method = request.args.get('method')
            active = request.form.get('Active')

            user_data = {
                'name': username,
                'password': password,
                'password2': password2,
                'role': role,
                'doj': doj,
                'Active': 'Yes' or active
            }

            if user_id:
                userObj.getById(user_id)

                if not userObj.data:
                    raise ValueError("User not found")

                user_data[userObj.pk] = user_id
                userObj.data = []

                # if method == 'PUT':
                userObj.set(user_data)
                userObj.verify_update()
                userObj.update()
                flash(f'Account updated for {username}!', 'info')
            else:  # new insert op
                user_data['role'] = role or 'employee'
                user_data['doj'] = doj or datetime.datetime.now().date()
                userObj.set(user_data)
                userObj.verify_new()
                userObj.insert()
                flash(f'Account created for {username}. Try logging in!', 'info')

            return redirect(url_for('login'))

        except Exception as e:
            flash(userObj.errors, 'danger')

    elif request.method == 'GET':  # current values for rendering
        method = request.args.get('method')
        if method == 'PUT':
            user_id = request.args.get('user_id')
            if user_id:
                userObj.getById(user_id)
            user_data = userObj.data if userObj and hasattr(userObj, 'data') else [{}]
            return render_template('register.html', user_data=user_data)
        else:  # Default view
            return render_template('register.html', user_data=[{}])


@app.route('/admin_view', methods=['GET', 'POST'])
def admin_view():
    u = user()
    u.getAll()
    employees = u.data
    fields = u.fields
    return render_template('admin_view.html', employees=employees, fieldsList=fields)


@app.route('/admin_view/delete', methods=['POST'])
def admin_delete():
    try:
        user_id = request.form.get('user_id')
        userObj = user()
        userObj.delete_user(user_id)
        return redirect('/admin_view')
    except Exception as e:
        print("Delete method failed due to", e)


## Manager Stuff

@app.route('/manager_view', methods=['GET', 'POST'])
def manager_view():
    taskObj = task()
    taskObj.getAll()
    tasksList = taskObj.data
    fieldsList = taskObj.fields
    user_id = request.args.get('user_id')
    return render_template('manager_view.html', user_id=user_id, tasksList=tasksList, fieldsList=fieldsList)


@app.route('/manager_view/delete', methods=['POST'])
def delete_task():
    try:
        task_id = request.form.get('task_id')

        ut = userTask()
        ut.deleteByField('task_id', task_id)

        taskObj = task()
        taskObj.deleteByField('task_id', task_id)
        return redirect('/manager_view')

    except Exception as e:
        print("Delete method failed due to", e)


@app.route('/create_task', methods=['GET', 'POST'])
def tasks():
    taskObj = task()
    usertaskObj = userTask()

    if request.method == "POST":
        try:
            task_id = request.form.get('task_id')
            task_name = request.form.get('task_name')
            description = request.form.get('description')
            priority = request.form.get('priority')
            status = request.form.get('status')
            created_on = request.form.get('created_on')
            due_date = request.form.get('due_date')
            update_on = datetime.datetime.now().date()
            # user_id = request.form.get('assignee')
            total_hours = int(request.form.get('total_hours', 0))
            logged_hours = int(request.form.get('logged_hours', 0))
            selected_choices = request.form.getlist('choices')
            selected_choices = list(map(int, selected_choices))

            print("chosen employees are:", selected_choices)

            task_data = {'task_name': task_name,
                         'description': description,
                         'status': status,
                         'due_date': due_date,
                         'updated_on': update_on,
                         'priority': priority,
                         'created_on': created_on,
                         'total_hours': total_hours,
                         'logged_hours': logged_hours
                         }

            if task_id:  # to edit existing task
                taskObj.getById(task_id)

                if not taskObj.data:
                    raise ValueError("Task not found")
                # taskObj=task()
                print("existing data to be edited is:", taskObj.data)
                task_data[taskObj.pk] = task_id
                taskObj.data = []
                taskObj.set(task_data)

                if taskObj.validate():
                    taskObj.update()

                    # usertable updation
                    get_user_and_task_details_query = usertaskObj.get_user_and_task_details()
                    usertaskObj.cur.execute(get_user_and_task_details_query, (task_id,))
                    ut_result = usertaskObj.cur.fetchall()
                    current_user_ids = [res['user_id'] for res in ut_result]

                    # filtering the user as per need
                    users_to_add = set(selected_choices) - set(current_user_ids)
                    users_to_remove = set(current_user_ids) - set(selected_choices)

                    # adding new user if any
                    for idx, user_id in enumerate(users_to_add):
                        usertaskObj.set({'task_id': task_id, 'user_id': user_id})
                        if usertaskObj.validate():
                            usertaskObj.insert(idx)
                            print(f"User {user_id} added to task {task_id}")
                        else:
                            print(usertaskObj.errors)

                    # removeing unchecked users
                    for user_id in users_to_remove:
                        query = usertaskObj.delete_user_and_task_details()
                        usertaskObj.cur.execute(query, (user_id, task_id))
                        print(f"User {user_id} removed from task {task_id}")

                    print("Update operation success")

                    return redirect(url_for('manager_view'))
                else:
                    print(taskObj.errors[0])

            else:  # insert operation
                # populating task table
                task_data['logged_hours'] = 0
                task_data['total_hours'] = 0

                taskObj.set(task_data)

                if taskObj.validate():
                    taskObj.insert()
                    print("insert operation success")
                else:
                    print(taskObj.errors[0])

            task_id = taskObj.data[-1][taskObj.pk]
            print('new pk is', task_id)

            # populate user_task table
            ut = userTask()
            for idx, choice in enumerate(selected_choices):
                print("choice is:", choice)
                ut.set({'user_id': choice, 'task_id': task_id})

                if ut.validate():
                    ut.insert(idx)
                    print("insert operation success")
                else:
                    print(taskObj.errors[0])

            return redirect(url_for('manager_view'))


        except Exception as e:
            # flash(str(e), 'danger')   
            print("Error occured", e)

    elif request.method == 'GET':
        u = user()
        u.getAll()
        task_data = [{}]
        statuses = ['Not Started', 'In Progress', 'Completed']
        priorities = ['Low', 'Medium', 'High']
        assigned_users = []
        method = request.args.get('method')
        if method == 'PUT':
            task_id = request.args.get('task_id')
            if task_id:
                get_task_details_query = taskObj.get_task_details()
                taskObj.cur.execute(get_task_details_query, (task_id,))
                results = taskObj.cur.fetchall()
                if results:
                    task_data = [results[0]]
                    assigned_users = [row['user_id'] for row in results]
                    # print(task_data)

                    print("Edit mode is working")
                else:
                    print("Task not Found")

            return render_template('taskForm.html', employeesList=u.data, assigned_users=assigned_users,
                                   statuses=statuses,
                                   priority=priorities, task_data=task_data)

        else:  # deafult view
            return render_template('taskForm.html', employeesList=u.data, statuses=statuses, priority=priorities,
                                   task_data=task_data)


## Employee Stuff

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    task_details, headers = [], []
    user_id = request.args.get('user_id')
    userObj = user()

    try:
        get_tasks_on_user_details_query = userObj.get_tasks_on_user_details()
        userObj.cur.execute(get_tasks_on_user_details_query, (user_id,))
        results = userObj.cur.fetchall()
        print(results)
        headers = ['Task_id', 'Task Name']
        task_details = [{'task_id': row['task_id'], 'task_name': row['task_name'], 'user_id': row['user_id'],
                         'emp_name': row['name']} for row in results]

    except Exception as e:
        print("Failed due to", e)

    return render_template('dashboard.html', task_details=task_details, headers=headers, user_id=user_id)


@app.route('/task/view/helper', methods=['GET', 'POST'])
def task_view_helper():
    task_id = request.args.get('task_id')
    user_id = request.args.get('user_id')
    return redirect(url_for('task_view', user_id=user_id, task_id=task_id))


#
@app.route('/task/view', methods=['GET', 'POST'])
def task_view():
    task_id = request.args.get('task_id')
    user_id = request.args.get('user_id')
    # comment_id=request.form.get('comment_id')

    taskObj = task()
    comObj = comments()

    task_details = []
    comments_details = []
    headers = ['Employee Name', 'Commented On', 'Comment']

    if request.method == 'GET':
        try:

            taskObj.getById(task_id)
            comments_details = comObj.get_comment_user_details(task_id)
            # print(comments_details)

            return render_template('task_view.html', task_details=taskObj.data, headers=headers,
                                   comments_details=comments_details, user_id=user_id)

        except Exception as e:
            print("Failed due to", e)

    elif request.method == 'POST':

        pass
    else:
        render_template('task_view.html', task_details=taskObj.data, comments_details=comObj.data)


# comment section
@app.route('/comment', methods=['GET', 'POST'])
def comment():
    comment_id = request.form.get('comment_id')
    user_id = request.form.get('user_id')
    task_id = request.form.get('task_id')

    commObj = comments()
    userObj = user()
    taskObj = task()

    if request.method == 'POST':
        # update_on = datetime.datetime.now().date()
        content = request.form.get('content')
        logged_hours = request.form.get('log_hrs')

        try:
            if user_id and task_id:
                userObj.getById(user_id)
                # employee_name = userObj.data[0]['name']
                # print('Employee adding comment is:', employee_name)
                taskObj.getById(task_id)
                task_details = taskObj.data
                current_logged_hours = task_details[0].get('logged_hours', 0)
                updated_hours = current_logged_hours + float(logged_hours)
                taskObj.data[0]['logged_hours'] = updated_hours
                taskObj.data[0]['updated_on'] = datetime.datetime.now()

                commObj.set({'content': content, 'user_id': user_id, 'task_id': task_id})

                if commObj.validate():
                    commObj.insert()
                    print(f"comment added succesfull for task {task_id} by user: {user_id}")

                if taskObj.validate():
                    taskObj.update()

                return redirect(url_for('task_view', user_id=user_id, task_id=task_id))


        except Exception as e:
            print(commObj.errors[0])

  
    else:
        return render_template('commentForm.html', user_id=user_id, task_id=task_id)


@app.route('/comment/add', methods=['POST'])
def addComment():
    user_id = request.form.get('user_id')
    task_id = request.form.get('task_id')
    return render_template('commentForm.html', user_id=user_id, task_id=task_id)


@app.route('/task/analysis', methods=['GET'])
def getAnalysis():
    taskObj = task()
    results = taskObj.get_task_analysis()
    statuses = [row['status'] for row in results]
    logged_hours = [row['total_logged_hours'] for row in results]
    assigned_hours = [row['total_assigned_hours'] for row in results]
    task_counts = [row['task_count'] for row in results]
    print(assigned_hours)
    print(task_counts)
    return render_template('task_analysis.html', statuses=statuses, logged_hours=logged_hours,
                           assigned_hours=assigned_hours, task_counts=task_counts)


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True)

## Project Management Tool 

#### Group Members
1. Nipun M Davasam
2. Devaduth Vempati


## Description
This app is a simplified project management tool. It allows users to create, track, and manage tasks across various stages of a project. The app includes features for task creation, categorization, assignment, and status tracking, enabling teams to collaborate and stay organized. 

## Primary use cases
- Creating and assigning tasks to team members.
- Tracking project progress and identifying bottlenecks.
- Collaborating on tasks and providing feedback.

#### User Roles
1. Admin
2. Manager
3. Employee

#### Main purpose of each user role
1. Admin - User Management:
  - Create new user accounts for employees
  - Assign roles to users
  - Deactivate or delete user accounts as needed

  

2. Manager - Project Management:
  - Create and manage projects.
  - Assign tasks to team members
  - Set deadlines and track progress
  - Monitor team performance and productivity
  - Provide feedback  to team members

3. Employee - Task Management:
  - View assigned tasks
  - Update task status and progress
  - Collaborate with team members on tasks
  - Log time spent on tasks
  - Use the platform to communicate with team members and managers

  ##### Note: Admin cannot modify user's password anytime after registration 
  
Credentials per user role (table)
1. Admin
   - username: admin_1
   - password: 101
2. Manager
   - username: manager_1
   - password: 101
3. Employee
   - username: employee_1
   - password: 101
## Select all users from the 'users' table



### sql for analytical view 
  - This query is used to generate a task analysis report with two charts. One chart shows logged hours and assigned hours by task status as a bar chart. The other chart shows the distribution of tasks by status as a pie chart.
    
```
SELECT status, SUM(logged_hours) AS total_logged_hours, SUM(total_hours) AS total_assigned_hours, COUNT(*) AS task_count FROM Task GROUP BY status;

```


## RELATIONAL Diagram
![RELATIONAL](https://github.com/user-attachments/assets/a00c32ae-df36-47a3-954c-52f9da9b5f0b)

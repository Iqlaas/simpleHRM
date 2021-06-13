import uuid
import datetime

from fastapi import FastAPI
from models import *

app = FastAPI()
db = Database(
    user='root',
    password='test-kamal',
    host='34.69.151.13',
    database='test-kamal-mysql'
)

@app.get("/")
async def hello():
    return {"hello": "world"}

@app.post("/register")
async def register(register: Register):
    
    email = register.email
    sql = f"select * from register where email='{email}'"

    out = db.query(sql)
    data = out['data']
    status = out['status']

    if data:
        response = {
            "response": f"Please try with another email as there is a duplicate {email}"
        }
        return response

    register.id = uuid.uuid4().hex[0:5]
    is_register = db.insert(register, 'register')

    user = register.username

    if is_register:
        response = {
            "response": f"User {user} is successfully registered"
        }
    
    return response

@app.post("/login")
async def login(login: Register):
    user = login.username
    email = login.email
    password = login.password

    sql = f"select * from register where email='{email}' and password='{password}' limit 1"
    out = db.query(sql)
    
    data = out['data']
    status = out['status']

    # print(is_user_exist)

    if data:
        response = {
            "response": f"Successfully login for {user}"
        }

        dt = datetime.datetime.utcnow()
        dt = dt.replace(microsecond=0)
        # dt = datetime.date.today()

        access = Access(
            id=login.id,
            username=login.username,
            sitename='login',
            accesstime=dt
        )

        _ = db.insert(access, 'access')
        
        return response

    else:
        response = {
            "response": f"Wrong either email or password"
        }
        return response

@app.post("/logout")
async def logout(logout: Register):
    user = logout.username
    email = logout.email


    dt = datetime.datetime.utcnow()
    dt = dt.replace(microsecond=0)
    # dt = datetime.date.today()

    access = Access(
        id=logout.id,
        username=logout.username,
        sitename='logout',
        accesstime=dt
    )

    _ = db.insert(access, 'access')

    response = {
        "response": f"Successfully logout for {user}"
    }
    
    return response

@app.post("/job")
async def job(job: Job):
    job.id = uuid.uuid4().hex[0:5]

    is_create_job = db.insert(job, 'job')

    if is_create_job:
        response = {
            "response": f"Job {job.title} is successfully created"
        }

    return response

@app.get("/job")
async def job():

    sql = "SELECT * FROM job"

    out = db.query(sql)
    # print(f"out :{out}")
    
    data = out['data']
    status = out['status']

    if not data:
        return {'no': 'items'}
    else:
        return data



@app.delete("/job/{id}")
async def job(job: Job):
    id = job.id

    sql = f"DELETE FROM job WHERE id='{id}'"
    
    db.query(sql)

    response = {
        "response": f"Successfully deleted for job {job.title}"
    }

    return response

@app.put("/job/{id}")
async def job(job: Job):
    id = job.id
    job_dict = job.dict()

    if 'id' in job_dict:
        del job_dict['id']

    set_array = []

    for key, value in job_dict.items():
        print(key, value)

        set_item = f"{key}='{value}'"
        set_array.append(set_item)
    
    set_string = ', '.join(set_array)

    sql = f"UPDATE job SET {set_string} WHERE id='{id}'"

    db.query(sql)

    response = {
        "response": f"Job {id} has been successfully updated"
    }

    return response

######################################################
########## EMPLOYEE ##################################
######################################################

@app.post("/employee")
async def employee(employee: Employee):
    employee.id = uuid.uuid4().hex[0:5]

    is_create_employee = db.insert(employee, 'employee')

    if is_create_employee:
        response = {
            "response": f"Employee {employee.name} is successfully created"
        }

    return response

@app.get("/employee")
async def employee():

    sql = "SELECT * FROM employee"

    out = db.query(sql)
    # print(f"out :{out}")
    
    data = out['data']
    status = out['status']

    if not data:
        return {'no': 'items'}
    else:
        return data

@app.delete("/employee/{id}")
async def employee(employee: Employee):
    id = employee.id

    sql = f"DELETE FROM employee WHERE id='{id}'"
    
    db.query(sql)

    response = {
        "response": f"Successfully deleted for employee {employee.name}"
    }

    return response

@app.put("/employee/{id}")
async def job(employee: Employee):
    id = employee.id
    employee_dict = employee.dict()

    if 'id' in employee_dict:
        del employee_dict['id']

    set_array = []

    for key, value in employee_dict.items():
        print(key, value)

        set_item = f"{key}='{value}'"
        set_array.append(set_item)
    
    set_string = ', '.join(set_array)

    sql = f"UPDATE employee SET {set_string} WHERE id='{id}'"

    db.query(sql)

    response = {
        "response": f"Employee {employee.name} has been successfully updated"
    }

    return response

######################################################
########## ACCESS ####################################
######################################################

@app.get("/access")
async def access():
    sql = "SELECT count(id) as number_of_access, sitename, username FROM access group by sitename, username"
    out = db.query(sql)
    
    data = out['data']

    return data

@app.post("/access")
async def access(user: UserAccess):

    dt = datetime.datetime.utcnow()
    dt = dt.replace(microsecond=0)
    # dt = datetime.date.today()

    access = Access(
        id=user.id,
        username=user.username,
        sitename=user.sitename,
        accesstime=dt
    )

    _ = db.insert(access, 'access')

    response = {
        "response": f"User {user.username} access {user.sitename}"
    }

    return response

######################################################
########## REPORTING ####################################
######################################################

@app.post("/sheet-jobs")
async def sheetjobs():
    sql = 'SELECT * FROM jobs'
    out = db.query(sql)
    data = out['data']

    return data

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = jobs_sheet_id
    range_name = 'A1:AA100'
    
    def main():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)
        values = [
        [
            data
        ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

@app.post("/sheet-employees")
async def employeejobs():
    sql = 'SELECT * FROM employee'
    out = db.query(sql)
    data = out['data']

    return data

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = jobs_sheet_id
    range_name = 'A1:AA100'
    
    def main():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)
        values = [
        [
            data
        ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

@app.post("/sheet-access")
async def sheetaccess():
    sql = 'SELECT * FROM access'
    out = db.query(sql)
    data = out['data']

    return data

    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    spreadsheet_id = jobs_sheet_id
    range_name = 'A1:AA100'
    
    def main():
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('sheets', 'v4', credentials=creds)
        values = [
        [
            data
        ],
        ]
        body = {
            'values': values
        }
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id, range=range_name,
            valueInputOption=value_input_option, body=body).execute()
        print('{0} cells updated.'.format(result.get('updatedCells')))

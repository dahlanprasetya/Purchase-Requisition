from flask import Flask,request,json,session, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal,fields
import datetime
from flask_cors import CORS, cross_origin
import os
import jwt
import requests
from requests.utils import quote


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'postgresql://postgres:Sembilantujuh97@localhost:5432/pr_makers'
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
jwtSecretKey = "goodcompany"

    
class Position(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name =  db.Column(db.String())

class Material(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())

class Employee(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    password = db.Column(db.String())
    position = db.Column(db.Integer,db.ForeignKey('position.id'))
    photoprofile = db.Column(db.String())
    payroll_number = db.Column(db.Integer())
    token = db.Column(db.String())

class Request(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    person_id = db.Column(db.Integer,db.ForeignKey('employee.id'))
    plant = db.Column(db.String())
    budget_type = db.Column(db.String())
    currency = db.Column(db.String())
    expected_date = db.Column(db.DateTime())
    location = db.Column(db.String())
    budget_source = db.Column(db.String())
    justification = db.Column(db.String())
    acc_scm = db.Column(db.Integer())
    acc_manager = db.Column(db.Integer())
    acc_owner = db.Column(db.Integer())
    material = db.Column(db.Integer, db.ForeignKey('material.id'))
    description = db.Column(db.String())
    quatity = db.Column(db.Integer())
    unit_measurement = db.Column(db.String())
    material_picture = db.Column(db.String())
    record_id = db.Column(db.String())
    process_id = db.Column(db.String())

# class Comment(db.Model):
#     id = db.Column(db.Integer,primary_key=True)
#     comment_content = db.Column(db.String())
#     id_user = db.Column(db.Integer, db.ForeignKey('employee.id'))
#     record_id = db.Column(db.String())

@app.route('/')
def get():
    return "test",201

@app.route('/login',methods=['POST'])
def login():
    request_data = request.get_json()
    req_email = request_data.get('email'),
    req_password = request_data.get('password')
    dataUser = Employee.query.filter_by(email=req_email, password=req_password).first()
    if dataUser :
        payload = {
            "id": dataUser.id,
            "secretcode": "kumiskucing"
        }
        encoded = jwt.encode(payload, jwtSecretKey, algorithm='HS256')
        json_format = {
        "token" : encoded,
        "position" : dataUser.position
        }
        user_json = json.dumps(json_format)

        return user_json, 200
    else:
        return 'gagal', 404

@app.route('/getAccRequest')
def getAccRequest():
    decoded = jwt.decode(Request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.filter_by(acc_scm=1, acc_manager=1, acc_owner=1).first()
    req = []
    for request in requests:
        employee = Employee.filter_by(id=request.id).first()
        json_format = {
            "id" : request.id,
            "person_name": employee.fullname,
            "plant": request.plant,
            "budget_type": request.budget_type,
            "currency": request.currency,
            "expected_date": request.expected_date,
            "location" : request.location,
            "budget_source": request.budget_source,
            "justification": request.justification,
            "material" : request.material,
            "description" : request.description,
            "quatity" : request.quatity,
            "unit_measurement": request.unit_measurement,
            "material_picture": request.material_picture,
        }
        req.append(json_format)
        req_json = json.dumps(req)
        return req_json,201

@app.route('/getUserRequest')
def getUserRequest():
    decoded = jwt.decode(Request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.query.filter_by(person_id=decoded["id"])
    request_arr = []
    for request in requests:
        userDB = Employee.query.filter_by(id=decoded["id"])
        request_arr = []
        json_format = {
            "id": request.id,
            "person_name": userDB.fullname,
            "plant": request.plant,
            "budget_type": request.budget_type,
            "currency": request.currency,
            "expected_date": request.expected_date,
            "location" : request.location,
            "budget_source": request.budget_source,
            "justification": request.justification,
            "material" : request.material,
            "description" : request.description,
            "quatity" : request.quatity,
            "unit_measurement": request.unit_measurement,
            "material_picture": request.material_picture
        }
        request_arr.append(json_format)
    request_json = json.dumps(request_arr)
    return request_json,201

@app.route('/getProfile')
def getProfile():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if userDB:        
        postition_name = Position.query.filter_by(id=userDB.position).first()
        json_format = {
            "fullname" : userDB.fullname,
            "email" : userDB.email,
            "position" :  postition_name.name,
            "photoprofile" : userDB.photoprofile
        }
        profile_json = json.dumps(json_format) 
        return profile_json, 201
    else:
        return "gagal",404

@app.route('/getMaterial')
def getMaterial():
    materials = Material.query.all()
    material_arr = []
    for material in materials:
        json_format = {
            "id": material.id,
            "code" : material.code,
            "name" : material.name
        }
        material_arr.append(json_format)
    material_json = json.dumps(material_arr)
    return material_json,201

@app.route('/getPosition')
def getPosition():
    positions = Position.query.all()
    position_arr = []
    for position in positions:
        json_format = {
            "id": position.id,
            "name": position.name
        }
        position_arr.append(json_format)
    position_json = json.dumps(position_arr)
    return position_json,201

@app.route('/getRequestAccScm')
def getRequestAccScm():
    decoded = jwt.decode(Request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.filter_by(acc_scm=1, acc_manager=0, acc_owner=0)
    req = []
    for request in requests:
        employee = Employee.filter_by(id=request.id)
        json_format = {
            "id" : request.id,
            "person_name": employee.fullname,
            "plant": request.plant,
            "budget_type": request.budget_type,
            "currency": request.currency,
            "expected_date": request.expected_date,
            "location" : request.location,
            "budget_source": request.budget_source,
            "justification": request.justification,
            "material" : request.material,
            "description" : request.description,
            "quatity" : request.quatity,
            "unit_measurement": request.unit_measurement,
            "material_picture": request.material_picture,
        }
        req.append(json_format)
        req_json = json.dumps(req)
        return req_json,201

@app.route('/getRequestAccManager')
def getRequestAccManager():
    decoded = jwt.decode(Request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.filter_by(acc_scm=1, acc_manager=1, acc_owner=0)
    req = []
    for request in requests:
        employee = Employee.filter_by(id=request.id)
        json_format = {
            "id" : request.id,
            "person_name": employee.fullname,
            "plant": request.plant,
            "budget_type": request.budget_type,
            "currency": request.currency,
            "expected_date": request.expected_date,
            "location" : request.location,
            "budget_source": request.budget_source,
            "justification": request.justification,
            "material" : request.material,
            "description" : request.description,
            "quatity" : request.quatity,
            "unit_measurement": request.unit_measurement,
            "material_picture": request.material_picture,
        }
        req.append(json_format)
        req_json = json.dumps(req)
        return req_json,201

@app.route('/getRequest')
def getRequest():
    decoded = jwt.decode(Request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    employee = Employee.query.filter_by(id = decoded["id"]).first()
    request_data = request.get_json()
    request_id = request_data.get('id')
    request = Request.query.filter_by(id=request_id)
    json_format = {
        "id" : request.id,
        "person_name": employee.fullname,
        "plant": request.plant,
        "budget_type": request.budget_type,
        "currency": request.currency,
        "expected_date": request.expected_date,
        "location" : request.location,
        "budget_source": request.budget_source,
        "justification": request.justification,
        "material" : request.material,
        "description" : request.description,
        "quatity" : request.quatity,
        "unit_measurement": request.unit_measurement,
        "material_picture": request.material_picture
    }
    req_json = json.dumps(json_format)
    return req_json, 201

# =====================================================================

@app.route('/submitrequest',methods=['POST'])
def submitRequest():
    if request.method == 'POST':
        request_data = request.get_json()
        req_email = request_data['email']
        req_comment = request_data['comment']

        userDB = Employee.query.filter_by(email=req_email).first()
        if userDB:
            user_token = userDB.token
            # data template untuk create record
            record_instance = {
                "data": {
                    "definition": {
                        "id": os.getenv('DEFINITION_ID')
                    }
                }
            }
            r = requests.post(os.getenv("BASE_URL_RECORD"), data=json.dumps(record_instance), headers={"Content-Type":"application/json", "Authorization" : "Bearer %s" %user_token})

            # result from create record
            result = json.loads(r.text)
            record_id = result['data']['id']

            #submit si flow pake record id dan token
            submit_request_result = submit_request(record_id,user_token,'requester_pr@makersinstitute.id')
            process_id = submit_request_result['data']['process_id']

            # gerakin flow dari requester ke manager
            sent_task(req_comment,user_token,process_id)

            # submit ke DB
            # data_db = submit_to_database(record_id,process_instance["data"]["process_id"])

            # return berupa id dan status
            return 'ok',201
            return r.status_text,201
        else:
            return "token not found",404

# fungsi untuk submit record dan gerakin flow ke requester
def submit_request(record_id,user_token,email_requester):
    # data template untuk submit record
    record_instance = {
        "data": {
            "form_data": {
                "pVRequester": email_requester,
                "pVSCM": "scm_pr@makersinstitute.id"
            },
            "comment": "Initiated"
        }
    }
    request_data = json.dumps(record_instance)

    # submit ke nextflow untuk dapetin process_id tiap pesanan masuk/flow
    r = requests.post(os.getenv('BASE_URL_RECORD') +"/"+record_id+"/submit",data=request_data, headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})

    result = json.loads(r.text)
    # print("INI RESULT SUBMIT RECORD", result)
    return result

# fungsi untuk gerakin flow dari requester ke manager
def sent_task(req_comment,user_token,process_id,task_name):

    def recursive():
        # get task id and pVApprover name
        query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (task_name,
            os.getenv("DEFINITION_ID"),process_id)
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
        r = requests.get(url,headers={
            "Content-Type": "application/json","Authorization": "Bearer %s" %user_token
        })
        print(r.text)

        result = json.loads(r.text)
        print("loading")
        if result['data'] is None or len(result['data']) == 0:
            recursive()
        else:
            #get manager email dan task id
            email = result['data'][0]['form_data']['pVSCM']
            task_id = result['data'][0]['id']

            # gerakin flow ke manager dari requester
            submit_data = {
                "data": {
                    "form_data": {
                        'pVSCM': email
                    },
                    "comment": req_comment
                }
            }
            r = requests.post(os.getenv('BASE_URL_TASK') +"/"+task_id+"/submit",data=json.dumps(submit_data), headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})
            result = json.loads(r.text)

    recursive()
    return "OK"

# submit data ke DB
def submit_to_database(record_id,process_id):
    request_data = request.get_json()
    req_code = request_data['code']
    req_price = request_data['price']
    # buat data template ke DB
    data_db = Request(
        person_name= employee.fullname,
        plant= request.plant,
        budget_type= request.budget_type,
        currency= request.currency,
        expected_date= request.expected_date,
        location= request.location,
        budget_source= request.budget_source,
        justification= request.justification,
        material= request.material,
        description= request.description,
        quatity= request.quatity,
        unit_measurement= request.unit_measurement,
        material_picture= request.material_picture,
        process_id = process_id,
        record_id = record_id
    )
    db.session.add(data_db)
    db.session.commit()
    db.session.flush() # fungsinya ketika data telah dimasukan kita mau pakai lagi datanya

    if data_db.id:
        return str(data_db.id)
    else:
        return None


if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))

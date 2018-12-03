from flask import Flask,request,json,session, make_response, render_template
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
    company = db.Column(db.String())
    plant = db.Column(db.String())

class Request(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    person_id = db.Column(db.Integer,db.ForeignKey('employee.id'))
    budget_type = db.Column(db.String())
    currency = db.Column(db.String())
    expected_date = db.Column(db.String())
    location = db.Column(db.String())
    budget_source = db.Column(db.String())
    justification = db.Column(db.String())
    acc_scm = db.Column(db.Integer())
    acc_manager = db.Column(db.Integer())
    acc_owner = db.Column(db.Integer())
    record_id = db.Column(db.String())
    process_id = db.Column(db.String())
    items = db.relationship('Items', backref='owner')

class Items(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    material_name = db.Column(db.String())
    quantity = db.Column(db.Integer())
    unit_measurement = db.Column(db.String())
    material_picture = db.Column(db.String())
    description = db.Column(db.String())
    estimate_price = db.Column(db.Integer())
    total = db.Column(db.Integer())
    request_id =  db.Column(db.Integer,db.ForeignKey('request.id'))




@app.route('/')
def get():
    return "test",201

@app.route('/login',methods=['POST'])
def login():
    request_data = request.get_json()
    req_email = request_data.get('email')
    req_password = request_data.get('password')
    dataUser = Employee.query.filter_by(email=req_email, password=req_password).first()
    if dataUser :
        payload = {
            "id": dataUser.id,
            "secretcode": "kumiskucing"
        }
        encoded = jwt.encode(payload, jwtSecretKey, algorithm='HS256').decode('utf-8')
        json_format = {
        "token" : encoded,
        "position" : dataUser.position
        }
        user_json = json.dumps(json_format)

        return user_json, 200
    else:
        return 'gagal', 404

@app.route('/getUserRequest')
def getUserRequest():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.query.filter_by(person_id=decoded["id"])
    request_arr = []
    for req in requests:
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        if req.acc_scm == 1 and req.acc_manager == 1 and req.acc_owner==1:
            json_format = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by Owner"
            }
        elif req.acc_scm == 1 and req.acc_manager == 1:
            json_format = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by Manager"
            }
        elif req.acc_scm == 1:
            json_format = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by SCM"
            }
        else:
            json_format = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Not yet approved"
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
            "photoprofile" : userDB.photoprofile,
            "payroll": userDB.payroll_number,
            "company": userDB.company,
            "plant": userDB.plant,
            "id" : userDB.id
        }
        profile_json = json.dumps(json_format) 
        return profile_json, 201
    else:
        return "gagal",404

@app.route('/getAllMaterial')
def getAllMaterial():
    materials = Material.query.all()
    arr_material = []
    for material in materials:
        json_format = {
            "code" : material.code,
            "name" : material.name,
            "id_material" : material.id
        }
        arr_material.append(json_format)
    material_json = json.dumps(arr_material)
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

@app.route('/getRequestDetails', methods=['POST'])
def getRequest():
    if request.method == 'POST':
        request_data = request.get_json()
        decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        requestDB = Request.query.filter_by(id=request_data["id"]).first()
        requester_detail = Employee.query.filter_by(id=requestDB.person_id).first()
        position = Position.query.filter_by(id=requester_detail.position).first()
        req_items = Items.query.filter_by(request_id=requestDB.id)
        arr_items = []
        for item in req_items:
            item_json = {
                "material_name" : item.material_name,
                "description" : item.description,
                "estimate_price" : item.estimate_price,
                "quantity" : item.quantity,
                "unit_measurement" : item.unit_measurement,
                "total" : item.total
            }
            arr_items.append(item_json)

        r = requests.get(os.getenv('BASE_URL_RECORD') +"/"+requestDB.record_id+"/stageview", headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % requester_detail.token})
        result = json.loads(r.text)
        # result = json.dumps(result)
        # print("ini result", result)
        # return result,201
        result_length = len(result["data"])
        # return str(result_length),201
        counter = 4
        arr_comment = []
        while counter <= result_length-1:
            print(counter)
            task_name = result["data"][counter]["object"]["display_name"]
            if task_name != "Employee":
                user_position = Position.query.filter_by(name=task_name).first()
                userDB = Employee.query.filter_by(position=user_position.id).first()
                comment_json = {
                    "comment" : result["data"][counter]["target"]["content"],
                    "date" : result["data"][counter]["published"],
                    "user": userDB.fullname,
                    "position" : user_position.name
                }
                arr_comment.append(comment_json)
                print(arr_comment)
                if result["data"][counter]["object"]["display_name"] == "Owner" and result["data"][counter]["name"] == "Task completed":
                    break
                counter += 2
            else:
                print("masuk ke else")
                counter += 2
                continue
        
        # json_format = {
        #     "comment" : arr_comment
        # }
        # req_json = json.dumps(json_format)
        # return req_json,201

        json_format = {
            "requester_detail" : {
                "fullname" : requester_detail.fullname,
                "email" : requester_detail.email,
                "position" : position.name,
                "id_number" : requester_detail.id,
                "company" : requester_detail.company,
                "plant": requester_detail.plant,
                "payroll" : requester_detail.payroll_number
            },
            "request_detail":{
                "budget_type": requestDB.budget_type,
                "currency" : requestDB.currency,
                "location" : requestDB.location,
                "budget_source": requestDB.budget_source,
                "expected_date" : requestDB.expected_date,
                "justification" : requestDB.justification
            },
            "items_detail": arr_items,
            "comment_history" : arr_comment
        }
        req_json = json.dumps(json_format)
        return req_json, 201

def addMaterial(request,req_item):
    data_db = Items(
        material_name = req_item['tableDataItemDetail'],
        quantity = req_item['tableDataQuantity'],
        unit_measurement = req_item['tableDataUnit'],
        description = req_item['tableDataDescription'],
        estimate_price = req_item['tableDataEstimatedPrice'],
        total = req_item['tableDataSubTotal'],
        owner = request
    )
    db.session.add(data_db)
    db.session.commit()
    db.session.flush()
    return data_db.id
# =====================================================================

@app.route('/submitrequest',methods=['POST'])
def submitRequest():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if request.method == 'POST':
        req_email = userDB.email
        req_comment = "test"
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
            position = Position.query.filter_by(id=userDB.position).first()
            task_name = position.name
            # return task_name,201
            sent_task(req_comment,user_token,process_id,task_name)

            # submit ke DB
            data_db = submit_to_database(record_id,process_id,userDB.id)

            # return berupa id dan status
            # return 'ok',201
            return data_db,201
        else:
            return "token not found",404

# fungsi untuk submit record dan gerakin flow ke requester
def submit_request(record_id,user_token,email_requester):
    # data template untuk submit record
    record_instance = {
        "data": {
            "form_data": {
                "pVRequester": email_requester,
                "pVSCM": "scm_pr@makersinstitute.id",
                "pVManager": "manager_pr@makersinstitute.id",
                "pVOwner": "owner_pr@makersinstitute.id",
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
def submit_to_database(record_id,process_id,employee_id):
    request_json = request.get_json()
    # buat data template ke DB
    data_db = Request(
        person_id = employee_id,
        budget_type= request_json['request_data']['budget_type'],
        currency= request_json['request_data']['currency'],
        expected_date= request_json['request_data']['expected_date'],
        location= request_json['request_data']['location'],
        budget_source= request_json['request_data']['budget_source'],
        justification= request_json['request_data']['justification'],
        process_id = process_id,
        record_id = record_id,
        acc_scm = 0,
        acc_manager = 0,
        acc_owner = 0
    )
    db.session.add(data_db)
    db.session.commit()
    db.session.flush() # fungsinya ketika data telah dimasukan kita mau pakai lagi datanya
    req_item = request_json['array_item']
    request_data = Request.query.filter_by(id=data_db.id).first()
    if request_data is not None:
        for item in req_item:
            addMaterial(request_data, item)

    if data_db.id:
        return str(data_db.id)
    else:
        return None

def get_tasklist(task_name,process_id,user_token):
    query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (task_name,
            os.getenv("DEFINITION_ID"),process_id)
    url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
    r = requests.get(url,headers={
        "Content-Type": "application/json","Authorization": "Bearer %s" %user_token
    })
    print(r.text)
    result = json.loads(r.text)
    return result,201

@app.route('/getComment')
def get_comment_history():
    request_data = request.get_json()
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if request.method == 'GET':
        if userDB:
            user_token = userDB.token
    url = os.getenv("BASE_URL_RECORD")+"/"+request_data["record_id"]+"/stageview"
    r = requests.get(url,headers={
        "Content-Type": "application/json","Authorization": "Bearer %s" %user_token
    })
    result = json.loads(r.text)
    result = json.dumps(result)
    return result,201

@app.route('/responseRequest',methods=["POST"])
def responseRequest():
    if request.method == 'POST':

        request_data = request.get_json()
        comment = request_data["comment"]
        decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        user_token = userDB.token
        user_position = Position.query.filter_by(id=userDB.position).first()
        requestDB = Request.query.filter_by(id=request_data["request_id"]).first()
        def recursive():
            # get task id and pVApprover name
            query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (user_position.name,
                os.getenv("DEFINITION_ID"),requestDB.process_id)
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
                if user_position.name == 'SCM':
                    if request_data["response"] == "Yes":
                        print("scm yes")
                        print("ini result",result)
                        email = result['data'][0]['form_data']['pVManager']
                        task_id = result['data'][0]['id']
                        print(task_id)

                        # gerakin flow ke manager dari requester
                        submit_data = {
                            "data": {
                                "form_data": {
                                    "pVManager": "manager_pr@makersinstitute.id",
                                    "pVAction": "Yes"
                                },
                                "comment": comment
                            }
                        }
                        r = requests.post(os.getenv('BASE_URL_TASK') +"/"+task_id+"/submit",data=json.dumps(submit_data), headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})
                        result = json.loads(r.text)
                        requestDB.acc_scm = 1
                        db.session.commit()
                    else:
                        print("scm no")
                        email = result['data'][0]['form_data']['pVRequester']
                        task_id = result['data'][0]['id']

                        # gerakin flow ke manager dari requester
                        submit_data = {
                            "data": {
                                "form_data": {
                                    "pVRequester": "requester_pr@makersinstitute.id",
                                    "pVAction": "No"
                                },
                                "comment": comment
                            }
                        }
                        r = requests.post(os.getenv('BASE_URL_TASK') +"/"+task_id+"/submit",data=json.dumps(submit_data), headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})
                        result = json.loads(r.text)
                
                elif user_position.name == 'Manager':
                    print("manager")
                    email = result['data'][0]['form_data']['pVOwner']
                    task_id = result['data'][0]['id']

                    # gerakin flow ke manager dari requester
                    submit_data = {
                        "data": {
                            "form_data": {
                                "pVOwner": "owner_pr@makersinstitute.id"
                            },
                            "comment": comment
                        }
                    }
                    r = requests.post(os.getenv('BASE_URL_TASK') +"/"+task_id+"/submit",data=json.dumps(submit_data), headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})
                    result = json.loads(r.text)
                    requestDB.acc_manager = 1
                    db.session.commit()
                
                else:
                    print("owner")
                    task_id = result['data'][0]['id']

                    submit_data = {
                        "data": {
                            "form_data": {
                            },
                            "comment": comment
                        }
                    }
                    r = requests.post(os.getenv('BASE_URL_TASK') +"/"+task_id+"/submit",data=json.dumps(submit_data), headers={"Content-Type": "application/json", "Authorization":"Bearer %s" % user_token})
                    result = json.loads(r.text)
                    requestDB.acc_owner = 1
                    db.session.commit()

        recursive()
        return "OK"

@app.route('/getTaskList')
def getTaskList():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    task_name = Position.query.filter_by(id=userDB.position).first()
    task_name = task_name.name
    query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s" % (task_name,
        os.getenv("DEFINITION_ID"))
    url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
    r = requests.get(url,headers={
        "Content-Type": "application/json","Authorization": "Bearer %s" %userDB.token
    })
    result = json.loads(r.text)
    result_length = len(result["data"])
    print("panjang result", result_length)
    arr_tasklist = []
    for x in range(result_length):
        print("ini process id : ",result["data"][x]["process_id"])
        requestDB = Request.query.filter_by(process_id=result["data"][x]["process_id"]).first()
        # print(requestDB)
        if requestDB == None:
            continue
        else:
            requesterDB = Employee.query.filter_by(id=requestDB.person_id).first()
            if task_name == "Employee" or task_name =="SCM":
                status = "Not yet approved"
            elif task_name == "Manager":
                status = "Approved by SCM"
            else : 
                status = "Approved by Manager"    
            format_json = {
                "id" : requestDB.id,
                "fullname" : requesterDB.fullname,
                "company" : requesterDB.company,
                "status" : status
            }
            arr_tasklist.append(format_json)
    request_json = json.dumps(arr_tasklist)
    return request_json,201

@app.route('/showEditData', methods= ["GET"])
def showEditData():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if userDB:        
        json_format = {
            "fullname" : userDB.fullname,
            "email" : userDB.email,
            "photoprofile" : userDB.photoprofile,
        }
        profile_json = json.dumps(json_format) 
        return profile_json, 201

@app.route('/editProfile', methods= ["PUT"])
def editProfile():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()

    if request.method == "PUT":      
        #new data
        req_data = request.get_json()
        fullname = req_data.get('fullname')
        email = req_data.get('email')
        photo_profile = req_data.get('profile_picture')

        userDB.fullname = fullname
        userDB.email = email
        userDB.photo_profile = photo_profile

        db.session.commit()

        return 'Data successfully edited', 200

@app.route('/editPassword', methods = ["PUT"])
def editPassword():
    decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()

    req_data = request.get_json()
    req_current_password = req_data.get('current_password')
    req_new_password = req_data.get('new_password')
    req_verify_password = req_data.get('verify_password')

    if request.method == "PUT":
        if userDB is not None and userDB.password == req_current_password:
            if req_new_password == req_verify_password:
                userDB.password = req_new_password
                db.session.commit()
                return "Password successfully changed ",200
        else:
            return "New password and validate password not match ",400
    else:
        return "Current password is wrong",400

    
@app.route('/getAccRequest')
def getAccRequest():
    requestDB = Request.query.filter_by(acc_scm=1,acc_manager=1,acc_owner=1)
    if requestDB:
        print("ini request db", requestDB)
        arr_accrequest = []
        for acc_request in requestDB:
            userDB = Employee.query.filter_by(id=acc_request.person_id).first()
            format_json = {
                "id":acc_request.id,
                "fullname": userDB.fullname,
                "company":userDB.company,
                "status":"Approved by Owner"
            }
            arr_accrequest.append(format_json)
        request_json = json.dumps(arr_accrequest)
        return request_json,201
    else:
        arr_accrequest = []
        request_json = json.dumps(arr_accrequest)
        return request_json,404


@app.route('/sendRevise',methods=["PUT"])
def sendRevise():
    if request.method == 'PUT':
        decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        position = Position.query.filter_by(id=userDB.position).first()
        request_data = request.get_json()
        print("ini request data",request_data)
        idRequest = request_data["id_request"]
        requestDB = Request.query.filter_by(id=idRequest).first()
        requestDB.budget_source = request_data["request_data"]["budget_source"]
        requestDB.budget_type = request_data["request_data"]["budget_type"]
        requestDB.currency = request_data["request_data"]["currency"]
        requestDB.expected_date = request_data["request_data"]["expected_date"]
        requestDB.justification = request_data["request_data"]["justification"]
        requestDB.location = request_data["request_data"]["location"]
        db.session.commit()
        items = Items.query.filter_by(request_id=idRequest)
        for item in items:
            db.session.delete(item)
            db.session.commit()
        
        req_item = request_data['array_item']
        requestDB = Request.query.filter_by(id=idRequest).first()
        if request_data is not None:
            for item in req_item:
                addMaterial(requestDB, item)
        
        req_comment = ""
        user_token = userDB.token
        process_id = requestDB.process_id
        task_name = position.name

        sent_task(req_comment,user_token,process_id,task_name)
        return "Success",201



# def acc
if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv("HOST"), port=os.getenv("PORT"))

from flask import Flask, request, json, session, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import marshal, fields
import datetime
from flask_cors import CORS, cross_origin
import os
import jwt
import requests
from requests.utils import quote
import smtplib
import random
import string
import base64
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import Message
from jinja2 import Environment


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:kumiskucing@localhost:5432/pr_makers'
CORS(app, support_credentials=True)
app.config['SECRET_KEY'] = os.urandom(24)
db = SQLAlchemy(app)
jwtSecretKey = "goodcompany"


class Position(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String())
    name = db.Column(db.String())


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String())
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    position = db.Column(db.Integer, db.ForeignKey('position.id'))
    photoprofile = db.Column(db.String())
    payroll_number = db.Column(db.Integer())
    token = db.Column(db.String())
    company = db.Column(db.String())
    plant = db.Column(db.String())


class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
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
    id = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String())
    quantity = db.Column(db.Integer())
    unit_measurement = db.Column(db.String())
    material_picture = db.Column(db.String())
    description = db.Column(db.String())
    estimate_price = db.Column(db.Integer())
    total = db.Column(db.Integer())
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))


@app.route('/')
def get():
    return "test", 201

# fungsi untuk login ke web
@app.route('/login', methods=['POST'])
def login():
    requestData = request.get_json()
    reqEmail = requestData.get('email')
    reqPassword = requestData.get('password')
    dataUser = Employee.query.filter_by(
        email=reqEmail, password=reqPassword).first()
    if dataUser:
        payload = {
            "id": dataUser.id,
            "secretcode": "kumiskucing"
        }
        encoded = jwt.encode(payload, jwtSecretKey,
                             algorithm='HS256').decode('utf-8')
        jsonFormat = {
            "token": encoded,
            "position": dataUser.position
        }
        userJson = json.dumps(jsonFormat)

        return userJson, 200
    else:
        return 'gagal', 404

# fungsi untuk menampilkan semua request dari user employee yang login
@app.route('/get-user-request')
def getUserRequest():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    requests = Request.query.filter_by(person_id=decoded["id"])
    requestArray = []
    for req in requests:
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        if req.acc_scm == 1 and req.acc_manager == 1 and req.acc_owner == 1:
            jsonFormat = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by Owner"
            }
        elif req.acc_scm == 1 and req.acc_manager == 1:
            jsonFormat = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by Manager"
            }
        elif req.acc_scm == 1:
            jsonFormat = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by SCM"
            }
        else:
            jsonFormat = {
                "id": req.id,
                "person_name": userDB.fullname,
                "company": userDB.company,
                "status": "Not yet approved"
            }
        requestArray.append(jsonFormat)
    requestJson = json.dumps(requestArray)
    return requestJson, 201

# fungsi untuk menampilkan detail profile dari user yang login
@app.route('/get-profile')
def getProfile():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if userDB:
        postitionName = Position.query.filter_by(id=userDB.position).first()
        jsonFormat = {
            "fullname": userDB.fullname,
            "email": userDB.email,
            "position":  postitionName.name,
            "photoprofile": userDB.photoprofile,
            "payroll": userDB.payroll_number,
            "company": userDB.company,
            "plant": userDB.plant,
            "id": userDB.id
        }
        profileJson = json.dumps(jsonFormat)
        return profileJson, 201
    else:
        return "gagal", 404

# fungsi untuk menampilkan semua material yang terdapat dalam db
@app.route('/get-all-material')
def getAllMaterial():
    materials = Material.query.all()
    arrayMaterial = []
    for material in materials:
        jsonFormat = {
            "code": material.code,
            "name": material.name,
            "id_material": material.id
        }
        arrayMaterial.append(jsonFormat)
    materialJson = json.dumps(arrayMaterial)
    return materialJson, 201

# fungsi untuk menampilkan semua posisi / role dalam db
@app.route('/get-position')
def getPosition():
    positions = Position.query.all()
    positionArray = []
    for position in positions:
        jsonFormat = {
            "id": position.id,
            "name": position.name
        }
        positionArray.append(jsonFormat)
    positionJson = json.dumps(positionArray)
    return positionJson, 201

# menampilkan detail lengkap dari request tertentu
@app.route('/get-request-detail', methods=['POST'])
def getRequest():
    if request.method == 'POST':
        requestData = request.get_json()
        decoded = jwt.decode(request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        requestDB = Request.query.filter_by(id=requestData["id"]).first()
        requesterDetail = Employee.query.filter_by(
            id=requestDB.person_id).first()
        position = Position.query.filter_by(
            id=requesterDetail.position).first()
        reqItems = Items.query.filter_by(request_id=requestDB.id)
        arrItems = []
        for item in reqItems:
            itemJson = {
                "material_name": item.material_name,
                "description": item.description,
                "estimate_price": item.estimate_price,
                "quantity": item.quantity,
                "unit_measurement": item.unit_measurement,
                "total": item.total
            }
            arrItems.append(itemJson)

        r = requests.get(os.getenv('BASE_URL_RECORD') + "/"+requestDB.record_id+"/stageview", headers={
                         "Content-Type": "application/json", "Authorization": "Bearer %s" % requesterDetail.token})
        result = json.loads(r.text)

        resultLength = len(result["data"])
        # return str(resultLength),201
        counter = 4
        arrayComment = []
        while counter <= resultLength-1:
            print(counter)
            taskName = result["data"][counter]["object"]["display_name"]
            if taskName != "Employee":
                userPosition = Position.query.filter_by(name=taskName).first()
                userDB = Employee.query.filter_by(
                    position=userPosition.id).first()
                commentJson = {
                    "comment": result["data"][counter]["target"]["content"],
                    "date": result["data"][counter]["published"],
                    "user": userDB.fullname,
                    "position": userPosition.name
                }
                arrayComment.append(commentJson)
                print(arrayComment)
                if result["data"][counter]["object"]["display_name"] == "Owner" and result["data"][counter]["name"] == "Task completed":
                    break
                counter += 2
            else:
                print("masuk ke else")
                counter += 2
                continue

        jsonFormat = {
            "requester_detail": {
                "fullname": requesterDetail.fullname,
                "email": requesterDetail.email,
                "position": position.name,
                "id_number": requesterDetail.id,
                "company": requesterDetail.company,
                "plant": requesterDetail.plant,
                "payroll": requesterDetail.payroll_number
            },
            "request_detail": {
                "budget_type": requestDB.budget_type,
                "currency": requestDB.currency,
                "location": requestDB.location,
                "budget_source": requestDB.budget_source,
                "expected_date": requestDB.expected_date,
                "justification": requestDB.justification
            },
            "items_detail": arrItems,
            "comment_history": arrayComment
        }
        reqJson = json.dumps(jsonFormat)
        return reqJson, 201

# menambahkan material ke dalam db
def addMaterial(request, reqItem):
    dataDB = Items(
        material_name=reqItem['tableDataItemDetail'],
        quantity=reqItem['tableDataQuantity'],
        unit_measurement=reqItem['tableDataUnit'],
        description=reqItem['tableDataDescription'],
        estimate_price=reqItem['tableDataEstimatedPrice'],
        total=reqItem['tableDataSubTotal'],
        owner=request
    )
    db.session.add(dataDB)
    db.session.commit()
    db.session.flush()
    return dataDB.id

# submit request dari requester ke scm
@app.route('/submit-request', methods=['POST'])
def submitRequestByRequester():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if request.method == 'POST':
        reqEmail = userDB.email
        reqComment = "test"
        if userDB:
            userToken = userDB.token
            # data template untuk create record
            recordInstance = {
                "data": {
                    "definition": {
                        "id": os.getenv('DEFINITION_ID')
                    }
                }
            }
            r = requests.post(os.getenv("BASE_URL_RECORD"), data=json.dumps(recordInstance), headers={
                              "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})

            # result from create record
            print(r.text)
            result = json.loads(r.text)
            recordId = result['data']['id']

            # submit si flow pake record id dan token
            submitRequestResult = submitRequest(
                recordId, userToken, 'requester_pr@makersinstitute.id')
            processId = submitRequestResult['data']['process_id']

            # gerakin flow dari requester ke manager
            position = Position.query.filter_by(id=userDB.position).first()
            taskName = position.name
            # return taskName,201
            sendTask(reqComment, userToken, processId, taskName)

            # submit ke DB
            dataDB = submitToDatabase(recordId, processId, userDB.id)

            # return berupa id dan status
            # return 'ok',201
            return dataDB, 201
        else:
            return "token not found", 404

# fungsi lanjutan dari submitRequestByRequester
def submitRequest(recordId, userToken, email_requester):
    # data template untuk submit record
    recordInstance = {
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
    requestData = json.dumps(recordInstance)

    # submit ke nextflow untuk dapetin process_id tiap pesanan masuk/flow
    r = requests.post(os.getenv('BASE_URL_RECORD') + "/"+recordId+"/submit", data=requestData,
                      headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})

    result = json.loads(r.text)
    # print("INI RESULT SUBMIT RECORD", result)
    return result

# kirim request yang telah di submit ke SCM
def sendTask(reqComment, userToken, processId, taskName):

    def recursive():
        # get task id and pVApprover name
        query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (taskName,
                                                                                                                             os.getenv("DEFINITION_ID"), processId)
        url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
        r = requests.get(url, headers={
            "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
        })
        print(r.text)

        result = json.loads(r.text)
        print("loading")
        if result['data'] is None or len(result['data']) == 0:
            recursive()
        else:
            # get manager email dan task id
            email = result['data'][0]['form_data']['pVSCM']
            taskId = result['data'][0]['id']

            # gerakin flow ke manager dari requester
            submitData = {
                "data": {
                    "form_data": {
                        'pVSCM': email
                    },
                    "comment": reqComment
                }
            }
            r = requests.post(os.getenv('BASE_URL_TASK') + "/"+taskId+"/submit", data=json.dumps(submitData),
                              headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})
            result = json.loads(r.text)

    recursive()
    return "OK"

# save detail request ke DB
def submitToDatabase(recordId, processId, employeeId):
    requestJson = request.get_json()
    # buat data template ke DB
    dataDB = Request(
        person_id=employeeId,
        budget_type=requestJson['request_data']['budget_type'],
        currency=requestJson['request_data']['currency'],
        expected_date=requestJson['request_data']['expected_date'],
        location=requestJson['request_data']['location'],
        budget_source=requestJson['request_data']['budget_source'],
        justification=requestJson['request_data']['justification'],
        process_id=processId,
        record_id=recordId,
        acc_scm=0,
        acc_manager=0,
        acc_owner=0
    )
    db.session.add(dataDB)
    db.session.commit()
    db.session.flush()  # fungsinya ketika data telah dimasukan kita mau pakai lagi datanya
    reqItem = requestJson['array_item']
    requestData = Request.query.filter_by(id=dataDB.id).first()
    if requestData is not None:
        for item in reqItem:
            addMaterial(requestData, item)

    if dataDB.id:
        return str(dataDB.id)
    else:
        return None

# mendapatkan tasklist dari user yang login
def getTasklist(taskName, processId, userToken):
    query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (taskName,
                                                                                                                         os.getenv("DEFINITION_ID"), processId)
    url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
    r = requests.get(url, headers={
        "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
    })
    print(r.text)
    result = json.loads(r.text)
    return result, 201

# mendapatkan commnet dari request tertentu
@app.route('/get-comment')
def getCommentHistory():
    requestData = request.get_json()
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if request.method == 'GET':
        if userDB:
            userToken = userDB.token
    url = os.getenv("BASE_URL_RECORD")+"/"+requestData["recordId"]+"/stageview"
    r = requests.get(url, headers={
        "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
    })
    result = json.loads(r.text)
    result = json.dumps(result)
    return result, 201

# fungsi untuk menerima response untuk request dan melanjutkan flow sesuai response
@app.route('/response-request', methods=["POST"])
def responseRequest():
    if request.method == 'POST':
        requestData = request.get_json()
        comment = requestData["comment"]
        decoded = jwt.decode(
            request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        userToken = userDB.token
        userPosition = Position.query.filter_by(id=userDB.position).first()
        requestDB = Request.query.filter_by(
            id=requestData["request_id"]).first()

        def recursive():
            # get task id and pVApprover name
            query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s&filter[process_id]=%s" % (userPosition.name,
                                                                                                                                 os.getenv("DEFINITION_ID"), requestDB.process_id)
            url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
            r = requests.get(url, headers={
                "Content-Type": "application/json", "Authorization": "Bearer %s" % userToken
            })
            print(r.text)

            result = json.loads(r.text)
            print("loading")
            if result['data'] is None or len(result['data']) == 0:
                recursive()
            else:
                # get manager email dan task id
                if userPosition.name == 'SCM':
                    if requestData["response"] == "Yes":
                        print("scm yes")
                        print("ini result", result)
                        email = result['data'][0]['form_data']['pVManager']
                        taskId = result['data'][0]['id']
                        print(taskId)

                        # gerakin flow ke manager dari requester
                        submitData = {
                            "data": {
                                "form_data": {
                                    "pVManager": "manager_pr@makersinstitute.id",
                                    "pVAction": "Yes"
                                },
                                "comment": comment
                            }
                        }
                        r = requests.post(os.getenv('BASE_URL_TASK') + "/"+taskId+"/submit", data=json.dumps(
                            submitData), headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})
                        result = json.loads(r.text)
                        requestDB.acc_scm = 1
                        db.session.commit()
                    else:
                        print("scm no")
                        email = result['data'][0]['form_data']['pVRequester']
                        taskId = result['data'][0]['id']

                        # gerakin flow ke manager dari requester
                        submitData = {
                            "data": {
                                "form_data": {
                                    "pVRequester": "requester_pr@makersinstitute.id",
                                    "pVAction": "No"
                                },
                                "comment": comment
                            }
                        }
                        r = requests.post(os.getenv('BASE_URL_TASK') + "/"+taskId+"/submit", data=json.dumps(
                            submitData), headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})
                        result = json.loads(r.text)

                elif userPosition.name == 'Manager':
                    print("manager")
                    email = result['data'][0]['form_data']['pVOwner']
                    taskId = result['data'][0]['id']

                    # gerakin flow ke manager dari requester
                    submitData = {
                        "data": {
                            "form_data": {
                                "pVOwner": "owner_pr@makersinstitute.id"
                            },
                            "comment": comment
                        }
                    }
                    r = requests.post(os.getenv('BASE_URL_TASK') + "/"+taskId+"/submit", data=json.dumps(
                        submitData), headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})
                    result = json.loads(r.text)
                    requestDB.acc_manager = 1
                    db.session.commit()

                else:
                    print("owner")
                    taskId = result['data'][0]['id']

                    submitData = {
                        "data": {
                            "form_data": {
                            },
                            "comment": comment
                        }
                    }
                    r = requests.post(os.getenv('BASE_URL_TASK') + "/"+taskId+"/submit", data=json.dumps(
                        submitData), headers={"Content-Type": "application/json", "Authorization": "Bearer %s" % userToken})
                    result = json.loads(r.text)
                    requestDB.acc_owner = 1
                    db.session.commit()
                    requesterDB = Employee.query.filter_by(
                        id=requestDB.person_id).first()
                    sendEmail(requesterDB.email, requestDB)

        recursive()
        return "OK"

# fungsi untuk mendapatkan tasklist dari user yang login
@app.route('/get-tasklist')
def getTaskList():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    taskName = Position.query.filter_by(id=userDB.position).first()
    taskName = taskName.name
    query = "folder=app:task:all&filter[name]=%s&filter[state]=active&filter[definition_id]=%s" % (taskName,
                                                                                                   os.getenv("DEFINITION_ID"))
    url = os.getenv("BASE_URL_TASK")+"?"+quote(query, safe="&=")
    r = requests.get(url, headers={
        "Content-Type": "application/json", "Authorization": "Bearer %s" % userDB.token
    })
    result = json.loads(r.text)
    resultLength = len(result["data"])
    print("panjang result", resultLength)
    arrTasklist = []
    for x in range(resultLength):
        print("ini process id : ", result["data"][x]["process_id"])
        if taskName == "Employee":
            requestDB = Request.query.filter_by(
                process_id=result["data"][x]["process_id"], person_id=userDB.id).first()
        else:
            requestDB = Request.query.filter_by(
                process_id=result["data"][x]["process_id"]).first()
        # print(requestDB)
        if requestDB == None:
            continue
        else:
            requesterDB = Employee.query.filter_by(
                id=requestDB.person_id).first()
            if taskName == "Employee" or taskName == "SCM":
                status = "Not yet approved"
            elif taskName == "Manager":
                status = "Approved by SCM"
            else:
                status = "Approved by Manager"
            formatJson = {
                "id": requestDB.id,
                "fullname": requesterDB.fullname,
                "company": requesterDB.company,
                "status": status
            }
            arrTasklist.append(formatJson)
    requestJson = json.dumps(arrTasklist)
    return requestJson, 201


@app.route('/show-edit-data', methods=["GET"])
def showEditData():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()
    if userDB:
        jsonFormat = {
            "fullname": userDB.fullname,
            "email": userDB.email,
            "photoprofile": userDB.photoprofile,
        }
        profileJson = json.dumps(jsonFormat)
        return profileJson, 201

# fungsi untuk edit profile dari user yang login
@app.route('/edit-profile', methods=["PUT"])
def editProfile():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()

    if request.method == "PUT":
        # new data
        reqData = request.get_json()
        fullname = reqData.get('fullname')
        email = reqData.get('email')
        photoProfile = reqData.get('profile_picture')

        userDB.fullname = fullname
        userDB.email = email
        userDB.photo_profile = photoProfile

        db.session.commit()

        return 'Data successfully edited', 200

# edit password dari user yang login
@app.route('/edit-password', methods=["PUT"])
def editPassword():
    decoded = jwt.decode(
        request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
    userDB = Employee.query.filter_by(id=decoded["id"]).first()

    reqData = request.get_json()
    reqCurrentPassword = reqData.get('current_password')
    reqNewPassword = reqData.get('new_password')
    reqVerifyPassword = reqData.get('verify_password')

    if request.method == "PUT":
        if userDB is not None and userDB.password == reqCurrentPassword:
            if reqNewPassword == reqVerifyPassword:
                userDB.password = reqNewPassword
                db.session.commit()
                return "Password successfully changed ", 200
        else:
            return "New password and validate password not match ", 400
    else:
        return "Current password is wrong", 400

# fungsi untuk menampilkan request yang telah di acc oleh scm, manager , owner
@app.route('/get-acc-request')
def getAccRequest():
    requestDB = Request.query.filter_by(acc_scm=1, acc_manager=1, acc_owner=1)
    if requestDB:
        print("ini request db", requestDB)
        arrAccRequest = []
        for accRequest in requestDB:
            userDB = Employee.query.filter_by(id=accRequest.person_id).first()
            formatJson = {
                "id": accRequest.id,
                "fullname": userDB.fullname,
                "company": userDB.company,
                "status": "Approved by Owner"
            }
            arrAccRequest.append(formatJson)
        requestJson = json.dumps(arrAccRequest)
        return requestJson, 201
    else:
        arrAccRequest = []
        requestJson = json.dumps(arrAccRequest)
        return requestJson, 404

# fungsi untuk mengirimkan request yang telah di revisi
@app.route('/send-revise', methods=["PUT"])
def sendRevise():
    if request.method == 'PUT':
        decoded = jwt.decode(
            request.headers["Authorization"], jwtSecretKey, algorithm='HS256')
        userDB = Employee.query.filter_by(id=decoded["id"]).first()
        position = Position.query.filter_by(id=userDB.position).first()
        requestData = request.get_json()

        print("ini request data", requestData)
        idRequest = requestData["id_request"]
        requestDB = Request.query.filter_by(id=idRequest).first()

        requestDB.budget_source = requestData["request_data"]["budget_source"]
        requestDB.budget_type = requestData["request_data"]["budget_type"]
        requestDB.currency = requestData["request_data"]["currency"]
        requestDB.expected_date = requestData["request_data"]["expected_date"]
        requestDB.justification = requestData["request_data"]["justification"]
        requestDB.location = requestData["request_data"]["location"]
        db.session.commit()

        items = Items.query.filter_by(request_id=idRequest)
        for item in items:
            db.session.delete(item)
            db.session.commit()

        reqItem = requestData['array_item']
        requestDB = Request.query.filter_by(id=idRequest).first()
        if requestData is not None:
            for item in reqItem:
                addMaterial(requestDB, item)

        reqComment = ""
        userToken = userDB.token
        processId = requestDB.process_id
        taskName = position.name

        sendTask(reqComment, userToken, processId, taskName)
        return "Success", 201

# fungsi untuk mengirimkan email setelah request di acc oleh owner
def sendEmail(email_requester, requestDB):
    host = "smtp.gmail.com"
    port = 587
    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_KEY")
    from_email = username
    to_list = email_requester

    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(username, password)
    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = "Request Approved"
    the_msg['From'] = from_email
    html_txt = """\
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Approved Request Email</title>
    <style type="text/css" media="screen">

        /* Force Hotmail to display emails at full width */
        .ExternalClass {
        display: block !important;
        width: 100%;
        }

        /* Force Hotmail to display normal line spacing */
        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
        line-height: 100%;
        }

        body,
        p,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
        margin: 0;
        padding: 0;
        }

        body,
        p,
        td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        color: #333333;
        line-height: 1.5em;
        }

        h1 {
        font-size: 24px;
        font-weight: normal;
        line-height: 24px;
        }

        body,
        p {
        margin-bottom: 0;
        -webkit-text-size-adjust: none;
        -ms-text-size-adjust: none;
        }

        img {
        line-height: 100%;
        outline: none;
        text-decoration: none;
        -ms-interpolation-mode: bicubic;
        }

        a img {
        border: none;
        }

        .background {
        background-color: #333333;
        }

        table.background {
        margin: 0;
        padding: 0;
        width: 100% !important;
        }

        .block-img {
        display: block;
        line-height: 0;
        }

        a {
        color: white;
        text-decoration: none;
        }

        a,
        a:link {
        color: #2A5DB0;
        text-decoration: underline;
        }

        table td {
        border-collapse: collapse;
        }

        td {
        vertical-align: top;
        text-align: left;
        }

        .wrap {
        width: 600px;
        }

        .wrap-cell {
        padding-top: 30px;
        padding-bottom: 30px;
        }

        .header-cell,
        .body-cell,
        .footer-cell {
        padding-left: 20px;
        padding-right: 20px;
        }

        .header-cell {
        background-color: #eeeeee;
        font-size: 24px;
        color: #ffffff;
        }

        .body-cell {
        background-color: #ffffff;
        padding-top: 30px;
        padding-bottom: 34px;
        }

        .footer-cell {
        background-color: #eeeeee;
        text-align: center;
        font-size: 13px;
        padding-top: 30px;
        padding-bottom: 30px;
        }

        .card {
        width: 400px;
        margin: 0 auto;
        }

        .data-heading {
        text-align: right;
        padding: 10px;
        background-color: #ffffff;
        font-weight: bold;
        }

        .data-value {
        text-align: left;
        padding: 10px;
        background-color: #ffffff;
        }

        .force-full-width {
        width: 100% !important;
        }

    </style>
    <style type="text/css" media="only screen and (max-width: 600px)">
        @media only screen and (max-width: 600px) {
        body[class*="background"],
        table[class*="background"],
        td[class*="background"] {
            background: #eeeeee !important;
        }

        table[class="card"] {
            width: auto !important;
        }

        td[class="data-heading"],
        td[class="data-value"] {
            display: block !important;
        }

        td[class="data-heading"] {
            text-align: left !important;
            padding: 10px 10px 0;
        }

        table[class="wrap"] {
            width: 100% !important;
        }

        td[class="wrap-cell"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        }
    </style>
    </head>

    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" bgcolor="" class="background">
    <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" class="background">
        <tr>
        <td align="center" valign="top" width="100%" class="background">
            <center>
            <table cellpadding="0" cellspacing="0" width="600" class="wrap">
                <tr>
                <td valign="top" class="wrap-cell" style="padding-top:30px; padding-bottom:30px;">
                    <table cellpadding="0" cellspacing="0" class="force-full-width">
                    <tr>
                        <td style="text-align: center;" height="60" valign="top" class="header-cell" >
                            <img width="55" height="55" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png" alt="Good Company" style="margin-top: 8px; ">
                        </td>
                    </tr>
                    <tr>
                        <td valign="top" class="body-cell">
                        <table cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff">
                            <tr>
                            <td valign="top" style="padding-bottom:20px; background-color:#ffffff;">
                            <b>Hi {{name}},</b><br \><br \>
                            <b>Congratulation!</b><br \>
                            We would like you to know that your request has been approved. To check any further please <a href="#">click here</a> to login.
                            </td>
                            </tr>
                            <tr>
                            <td>
                                <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff">
                                <tr>
                                <td align="center" style="padding:20px 0;">
                                    <center>
                                    <table cellspacing="0" cellpadding="0" class="card">
                                        <tr>
                                        <td style="background-color:#1f618d; text-align:center; padding:10px; color:white; ">
                                            Request Details
                                        </td>
                                        </tr>
                                        <tr>
                                        <td style="border:1px solid #1f618d;">
                                            <table cellspacing="0" cellpadding="20" width="100%">
                                            <tr>
                                                <td>
                                                <table cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff">
                                                    <tr>
                                                    <td width="150" class="data-heading">
                                                        Request ID:
                                                    </td>
                                                    <td class="data-value">
                                                        {{request_id}}
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td width="150" class="data-heading">
                                                        Record ID:
                                                    </td>
                                                    <td class="data-value">
                                                        {{recordId}}
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td width="150" class="data-heading">
                                                        Process ID:
                                                    </td>
                                                    <td class="data-value">
                                                        {{process_id}}
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td width="150" class="data-heading">
                                                        Budget Type:
                                                    </td>
                                                    <td class="data-value">
                                                        {{budget_type}}
                                                    </td>
                                                    </tr>
                                                    <tr>
                                                    <td width="150" class="data-heading">
                                                        Justification:
                                                    </td>
                                                    <td class="data-value">
                                                        {{justification}}
                                                    </td>
                                                    </tr>    
                                                </table>
                                                </td>
                                            </tr>
                                            </table>
                                        </td>
                                        </tr>
                                    </table>
                                    </center>
                                </td>
                                </tr>
                            </table>
                            </td>
                            </tr>
                            <tr>
                            <td style="padding-top:20px;background-color:#ffffff;">
                                Have a nice day!<br>
                                Administator Good Company
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    <tr>
                        <td valign="top" class="footer-cell">
                        Good Company<br>
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </center>
        </td>
        </tr>
    </table>

    </body>
    </html>
    """
    userDB = Employee.query.filter_by(id=requestDB.person_id).first()
    part_2 = MIMEText(Environment().from_string(html_txt).render(
        name=userDB.fullname, request_id=requestDB.id, recordId=requestDB.record_id, process_id=requestDB.process_id, budget_type=requestDB.budget_type, justification=requestDB.justification
    ), 'html')
    the_msg.attach(part_2)
    email_conn.sendmail(from_email, to_list, the_msg.as_string())
    email_conn.quit()
    return "Success", 201

# fungsi untuk mengirimkan password sementara melalui email (forgot password)
def sendEmailChangePass(email_requester, new_password, userFullname):
    host = "smtp.gmail.com"
    port = 587
    username = os.getenv("EMAIL_ADDRESS")
    password = os.getenv("EMAIL_KEY")
    from_email = username
    to_list = email_requester

    email_conn = smtplib.SMTP(host, port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(username, password)
    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = "Reset Password Request"
    the_msg['From'] = from_email
    html_txt = """\
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Forgot Password Email</title>
    <style type="text/css" media="screen">

        /* Force Hotmail to display emails at full width */
        .ExternalClass {
        display: block !important;
        width: 100%;
        }

        /* Force Hotmail to display normal line spacing */
        .ExternalClass,
        .ExternalClass p,
        .ExternalClass span,
        .ExternalClass font,
        .ExternalClass td,
        .ExternalClass div {
        line-height: 100%;
        }

        body,
        p,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6 {
        margin: 0;
        padding: 0;
        }

        body,
        p,
        td {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 15px;
        color: #333333;
        line-height: 1.5em;
        }

        h1 {
        font-size: 24px;
        font-weight: normal;
        line-height: 24px;
        }

        body,
        p {
        margin-bottom: 0;
        -webkit-text-size-adjust: none;
        -ms-text-size-adjust: none;
        }

        img {
        outline: none;
        text-decoration: none;
        -ms-interpolation-mode: bicubic;
        }

        a img {
        border: none;
        }

        .background {
        background-color: #333333;
        }

        table.background {
        margin: 0;
        padding: 0;
        width: 100% !important;
        }

        .block-img {
        display: block;
        line-height: 0;
        }

        a {
        color: white;
        text-decoration: none;
        }

        a,
        a:link {
        color: #2A5DB0;
        text-decoration: underline;
        }

        table td {
        border-collapse: collapse;
        }

        td {
        vertical-align: top;
        text-align: left;
        }

        .wrap {
        width: 600px;
        }

        .wrap-cell {
        padding-top: 30px;
        padding-bottom: 30px;
        }

        .header-cell,
        .body-cell,
        .footer-cell {
        padding-left: 20px;
        padding-right: 20px;
        }

        .header-cell {
        background-color: #eeeeee;
        font-size: 24px;
        color: #ffffff;
        }

        .body-cell {
        background-color: #ffffff;
        padding-top: 30px;
        padding-bottom: 34px;
        }

        .footer-cell {
        background-color: #eeeeee;
        text-align: center;
        font-size: 13px;
        padding-top: 30px;
        padding-bottom: 30px;
        }

        .card {
        width: 400px;
        margin: 0 auto;
        }

        .data-heading {
        text-align: right;
        padding: 10px;
        background-color: #ffffff;
        font-weight: bold;
        }

        .data-value {
        text-align: left;
        padding: 10px;
        background-color: #ffffff;
        }

        .force-full-width {
        width: 100% !important;
        }

    </style>
    <style type="text/css" media="only screen and (max-width: 600px)">
        @media only screen and (max-width: 600px) {
        body[class*="background"],
        table[class*="background"],
        td[class*="background"] {
            background: #eeeeee !important;
        }

        table[class="card"] {
            width: auto !important;
        }

        td[class="data-heading"],
        td[class="data-value"] {
            display: block !important;
        }

        td[class="data-heading"] {
            text-align: left !important;
            padding: 10px 10px 0;
        }

        table[class="wrap"] {
            width: 100% !important;
        }

        td[class="wrap-cell"] {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        }
    </style>
    </head>

    <body leftmargin="0" marginwidth="0" topmargin="0" marginheight="0" offset="0" bgcolor="" class="background">
    <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" class="background">
        <tr>
        <td align="center" valign="top" width="100%" class="background">
            <center>
            <table cellpadding="0" cellspacing="0" width="600" class="wrap">
                <tr>
                <td valign="top" class="wrap-cell" style="padding-top:30px; padding-bottom:30px;">
                    <table cellpadding="0" cellspacing="0" class="force-full-width">
                    <tr>
                    <td style="text-align: center;" height="60" valign="top" class="header-cell" >
                        <img width="55" height="55" src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/SNice.svg/1200px-SNice.svg.png" alt="Good Company" style="margin-top: 3px; ">
                        </td>
                    </tr>
                    <tr>
                        <td valign="top" class="body-cell">

                        <table cellpadding="0" cellspacing="0" width="100%" bgcolor="#ffffff">
                            <tr>
                            <td valign="top" style="padding-bottom:15px; background-color:#ffffff;">
                                <h1>Reset Password Request</h1>
                            </td>
                            </tr>
                            <tr>
                            <td valign="top" style="padding-bottom:20px; background-color:#ffffff;">
                                <b>Hello {{name}} </b>, <br>
                                We recently received a request to reset your account password. Here is your new password : <b>{{new_password}}</b> <br \>
                                We suggest you to log in with this password and change it on your profile.
                            </td>
                            </tr>
                            <tr>
                            <td>
                                <table cellspacing="0" cellpadding="0" width="100%" bgcolor="#ffffff">
                                <tr>
                                    <td style="width:180px;background: #ffca28;">
                                    <div>
                                            <a href="localhost:8000/login.html"
                                    style="background-color: #ffca28;color:#1f618d;display:inline-block;font-family:sans-serif;font-size:18px;line-height:40px;text-align:center;text-decoration:none;width:180px;-webkit-text-size-adjust:none;">Log In Now!</a>
                                        </div>
                                    </td>
                                    <td width="360" style="background-color:#ffffff; font-size:0; line-height:0;"></td>
                                </tr>
                                </table>
                            </td>
                            </tr>
                            <tr>
                            <td style="padding-top:20px;background-color:#ffffff;">
                                Regards,<br>
                                Administrator Good Company
                            </td>
                            </tr>
                        </table>
                        </td>
                    </tr>
                    <tr>
                        <td valign="top" class="footer-cell">
                        Good Company
                        </td>
                    </tr>
                    </table>
                </td>
                </tr>
            </table>
            </center>
        </td>
        </tr>
    </table>

    </body>
    </html>
    """

    part_2 = MIMEText(Environment().from_string(html_txt).render(
        name=userFullname, new_password=new_password
    ), 'html')
    the_msg.attach(part_2)
    email_conn.sendmail(from_email, to_list, the_msg.as_string())
    email_conn.quit()
    return "Success", 201

# fungsi untuk merandom string sebagai password sementara
def randomword():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(8))

# fungsi untuk enkripsi string kedalam base64
def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

# ubah base64 ke string
def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

# fungsi untuk forgot password
@app.route('/forgot-password', methods=["PUT"])
def forgotPassword():
    if request.method == 'PUT':
        requestData = request.get_json()
        email = requestData["email"]
        user = Employee.query.filter_by(email=email).first()
        userFullname = user.fullname
        if user:
            tmpPassStr = randomword()
            tmpPassEncode = str(stringToBase64(tmpPassStr))
            length = len(tmpPassEncode) - 1
            print(tmpPassStr, tmpPassEncode)
            tmpPassEncode = tmpPassEncode[2:length]
            print(tmpPassEncode)
            user.password = str(tmpPassEncode)
            db.session.commit()
            sendEmailChangePass(email, tmpPassStr, userFullname)
            return "Success", 201

        else:
            return "User not found", 404


# def acc
if __name__ == '__main__':
    app.run(debug=os.getenv("DEBUG"), host=os.getenv(
        "HOST"), port=os.getenv("PORT"))

import smtpd
from time import sleep
from tkinter import E
from urllib import response
from flask import Flask, render_template, request, flash,Response, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import JSON, true
from typing import Any, List
from flask_marshmallow import Marshmallow 
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

hostname = 'localhost'
database = 'alerts'
username = 'postgres'
password = 'wordpass123'   #add password for thepostresql db
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{username}:{password}@{hostname}/{database}'   #connection to db
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'secret string' #secret key for connection
app.config['SECRET_KEY'] = 'thisissecret'
db = SQLAlchemy(app)
ma = Marshmallow(app)

class User(db.Model):          #Schemaclass for users to make db create
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(255))
    name = db.Column(db.String(50))
    password = db.Column(db.String(255))
    admin = db.Column(db.Boolean)


@app.route('/admin_user', methods=['POST'])    #First route to make a admin user to create all user

def admin_create_user():

    hashed_password = generate_password_hash("1234", method='sha256')  

    new_user = User(public_id=str(uuid.uuid4()), name="Admin", password=hashed_password, admin=True)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'First Admin User Created....'})


def req_token(f):               #decorator to identify it is authorised or not
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']   #access token for from postman headers as KEY

        if not token:
            return jsonify({'message' : 'Need to Login'}), 221

        try: 
            data = jwt.decode(token, "HHHHH", algorithms=['HS256'])             #decoding the token
            current_user = User.query.filter_by(public_id=data['public_id']).first() # all users from the publicid encrypted in token
        except Exception as err:
            return jsonify({'message' : str(err)}), 221
        print(current_user.id)
        return f(current_user, *args, **kwargs)

    return decorated
#all routes all below 

@app.route('/user', methods=['GET'])    #
@req_token   #decorator to identify if it is authorised
def get_all_users(current_user):

    if not current_user.admin:
        return jsonify({'message' : 'Need to Be an Admin'})

    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['admin'] = user.admin
        output.append(user_data)

    return jsonify({'users' : output})

@app.route('/user/<public_id>', methods=['GET'])
@req_token
def get_one_user(current_user, public_id):

    if not current_user.admin:
        return jsonify({'message' : 'Need to Be an Admin'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['admin'] = user.admin

    return jsonify({'user' : user_data})

@app.route('/user', methods=['POST'])
@req_token
def create_user(current_user):
    if current_user.admin:
        return jsonify({'message' : 'Need to Be an Admin'})

    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), name=data['name'], password=hashed_password, admin=False)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@app.route('/user/<public_id>', methods=['PUT'])
@req_token
def promote_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Need to Be an Admin'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user.admin = True
    db.session.commit()

    return jsonify({'message' : 'The user has been promoted!'})

@app.route('/user/<public_id>', methods=['DELETE'])
@req_token
def delete_user(current_user, public_id):
    if not current_user.admin:
        return jsonify({'message' : 'Cannot perform that function!'})

    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message' : 'The user has been deleted!'})

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow()+ datetime.timedelta(minutes=30)},"HHHHH")

        return jsonify({'token' : token})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})












# Routes for the alerts
#--------------------------------------------------------------------------------------#
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    public_id = db.Column(db.String(255))
    

    def __init__(self, id, price,email,status, public_id):
        self.id = id
        self.price = price
        self.email = email
        self.status = status
        self.public_id= public_id
        

class AlertSchema(ma.Schema):  #schema to get values
  class Meta:
    fields = ('id', 'price', 'email', 'status')

Alerts_schema = AlertSchema(many=True)
Alert_schema = AlertSchema()
@app.route('/alerts/create', methods=['POST'])
@req_token
def createAlert(current_user):

    data=request.get_json()
    id = data.get('id')
    price = data.get('price')
    email = data.get('email')
    status = data.get('status')
    public_id=current_user.public_id
    entry = Alert(id,price,email,status, public_id)
    db.session.add(entry)
    db.session.commit()
    #return make_response('Created...',201)
    return Alert_schema.jsonify(entry)

@app.route('/alerts/getalert',methods=['GET'])
@req_token
def fetchAllAlerts():
    alert = Alert.query.all() 
    print(alert)
    # return jsonify(JSON.dump(alert))
    result = Alerts_schema.dump(alert)
    return make_response(jsonify(result), 201)
    
@app.route('/alerts/<public_id>', methods=['GET'])
@req_token
def get_product(id):
  product = Alert.query.get(id)
  return Alert_schema.jsonify(product)


@app.route('/alerts/change/<public_id>', methods=['PUT'])
@req_token
def update_product(current_user):
    product = Alert.query.get(current_user.public_id)
    price= request.json['price']
    product.price=price
    product.status="Changed";
    db.session.commit()
    return Alert_schema.jsonify(product)


@app.route('/alerts/delete/<public_id>', methods=['DELETE'])
@req_token
def delete_product(current_user):
    product = Alert.query.get(current_user.public_id)
    product.status="Deleted";
    db.session.commit()
    return Alert_schema.jsonify(product)

def getvaluefromAPI(): #function to get bitcoin value
    response_API = request.get("https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false")

    data = response_API.text
    parse_json = JSON.loads(data)
    price = parse_json[0]["current_price"]
    return price

def trigger(): # trigger function to trigger the mail it will get th request from the api we created fromn the databasee Postresql
    alerts_values=request.get("http://127.0.0.1:5000/alerts/getalert")
    bit_value=getvaluefromAPI()
    data = alerts_values.text
    parse_json = JSON.loads(data)
    for i in len(alerts_values):
        
        price = parse_json[i]["price"]
        if(price>=bit_value):
            sendmail(bit_value, price, parse_json[i]["email"] )

def sendmail(b,p,s): #Function to send mail
    sender_email = ''  #ADD sender' email
    password = ''       #add passwrd must not be 2 way authenticator to bypass this method will given in ReadME.md
    message = 'ALERT!'+'\nYour stock has reached ' + b + '\nAlert set for '+p
    server = smtpd.SMTP()
    try:
        server.starttls()
        server.login(sender_email, password)
        print('Logged Into Email Account')
        server.sendmail(sender_email, s, message)
        print("Alert Sent")
    except Exception as error:
        print('Error Occured: ',error)

db.create_all()
app.run()
while True:
    trigger()
    sleep(60)   #run in every 60 secs

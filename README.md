# Crypto-Price-Alert

install the packages


- Flask
- URL Lib
- Flask - SQLAlchemy
- JWT
- Flask - Marshmallow
- 

Made together with Chaitanya Sapre 19BAI10131


create a table in Postsql give the table name and pass in the app.py file
run the app

use POSTMAN to send queries 
port given for me - http://127.0.0.1:5000<br>
GET - http://127.0.0.1:5000/admin_user<br>
GET - http://127.0.0.1:5000/login

GET - http://127.0.0.1:5000/user

add KEY  and VALUE in headers KEY=x-access-token VALUE= "Token you got after login route"

GET - http://127.0.0.1:5000/user/<public_id> - Copy the public id got in response of any users paste to get the details of use

POST -http://127.0.0.1:5000/user - gives all user

PUT -  http://127.0.0.1:5000/user/<public_id> - to change the admin value to true of false

DELETE - http://127.0.0.1:5000/user/delete/<public_id> - Delete alert
 
 
You must first login through postman 


for Alerts 

POST - http://127.0.0.1:5000/alerts/create - creating alerts

GET - http://127.0.0.1:5000/alerts/getalert - fetching all the alerts, It will be used to fetch the data from database to chect the value of price to send mail alert

GET - http://127.0.0.1:5000/alerts/<public_id> - get a particuler alert it will 

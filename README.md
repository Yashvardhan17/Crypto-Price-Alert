# Crypto-Price-Alert

install the packages


- Flask  = for restAPI
- URL Lib  = for URLs
- Flask - SQLAlchemy =for DATABASE 
- JWT  = for authentication
- Flask - Marshmallow = Schema
- smtpd = for EMAIL

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

GET - http://127.0.0.1:5000/alerts/<public_id> - get a particuler alert 



trigger function will run every 60 seconds it will call the which will send the email


DISCRIPTION flow of code



The file app.py will run the application will help to get the requests whenerver the flask app server is running 
After that run the main.py to get the email alerts
App is basic when the server is running it will fetch the value from the database
before run the flask APP

main.py code is also written in the app to run in a single file



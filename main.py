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
        
while True:
  trigger()
  sleep(60)

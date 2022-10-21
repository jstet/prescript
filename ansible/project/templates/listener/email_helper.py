import smtplib
from email.message import EmailMessage


# set your email and password
# please use App Password
address = "{{  SMTP_ADDRESS  }}"
password = "{{  SMTP_PW  }}"
host = "{{  SMTP_HOST  }}"
recipient = "{{  SMTP_RECIPIENT  }}"




def send_email(success, text):
    smtp = smtplib.SMTP(host, 587, timeout=10)
    smtp.ehlo()  # send the extended hello to our server
    smtp.starttls()  # tell server we want to communicate with TLS encryption
    smtp.login(address, password)
    
    msg = EmailMessage()
    msg['From'] = address
    msg['To'] = recipient
    msg['Subject'] = "Your script report"
    
    if success:  
        msg.set_content(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>Your script has finished!</h2>
                <p>Find the output in your storage box</p>
                <p>{text}</p>
            </body>
        </html>
        """, subtype='html')
        
    else:
        msg.set_content(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>An error has occured!</h2>
                <p>{text}</p>
            </body>
        </html>
        """, subtype='html')
    
    smtp.send_message(msg)
    smtp.quit()

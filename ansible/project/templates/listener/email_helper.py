import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
load_dotenv()

# set your email and password
# please use App Password
address = "{{  SMTP_ADDRESS  }}"
password = "{{  SMTP_PW  }}"
host = "{{  SMTP_HOST  }}"
recipient = "{{  SMTP_RECIPIENT  }}"

footer = "<p>This Mail was generated by running <a href='https://github.com/jstet/prescript'>Prescript</a>.</p>"


def send_email(success):
    smtp = smtplib.SMTP(host, 587, timeout=10)
    smtp.ehlo()  # send the extended hello to our server
    smtp.starttls()  # tell server we want to communicate with TLS encryption
    smtp.login(address, password)
    msg = EmailMessage()
    msg['From'] = address
    msg['To'] = recipient
    if success == 1:
        msg['Subject'] = "Prescript - Your script report"
        msg.set_content(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>Your script has finished!</h2>
                <p>Find the output in your storage box.</p>
                <p>The server has been deleted.</p>
                <br>
                {footer}
            </body>
        </html>
        """, subtype='html')
    elif success == 0:
        msg['Subject'] = "Prescript - Your script failed!"
        msg.set_content(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>An error occured during the execution of your script!</h2>
                <p>Find output (if there is any) in your storage box.</p>
                <p>The server has <strong>not</strong> been deleted.</p>
                <br>
                {footer}
            </body>
        </html>
        """, subtype='html')
    else:
        msg['Subject'] = "Prescript - The event listener has failed"
        msg.set_content(f"""
        <!DOCTYPE html>
        <html>
            <body>
                <h2>The event listener has failed!</h2>
                <p>Connect to server to see what happened...</p>
                <br>
                {footer}
            </body>
        </html>
        """, subtype='html')
    smtp.send_message(msg)
    smtp.quit()

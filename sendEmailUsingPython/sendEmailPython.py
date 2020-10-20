import smtplib as s
import credentials
from email.message import EmailMessage
import csv

def get_login_details():
    email = credentials.EMAIL
    password = credentials.PASSWORD
    return email, password


def mail_send():
    try:
        mail_obj = s.SMTP("smtp.gmail.com",587)
        mail_obj.starttls()
        email,password=get_login_details()
        mail_obj.login(email,password)
        print("logged in")

        subject="test mail using python"
        with open("email_content.txt") as f:
            message = EmailMessage()
            message.set_content(f.read())
            message['Subject'] =subject
            message['From']=email
            with open("details.csv", newline="") as csvfile:
                id_reader=csv.reader(csvfile, delimiter=",")
                for id in id_reader:
                    id_to_send=str(id[1])
                    message['To']=id_to_send
                    mail_obj.send_message(message,email,id_to_send)
                    print("Email sent successfully to "+id[1])


        mail_obj.quit()
    except s.SMTPException:
        print("Error: unable to send email")



if __name__ == "__main__":
    mail_send()




import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
fname = 'trend.rrd'

mailsender = "jose.angel.pruebas.redes@gmail.com"
mailreceip = "jose.angel.pruebas.redes@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'HfBIu$mB0!!Q'

def send_alert_attached(subject):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    fp = open('deteccion.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()
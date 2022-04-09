
# -------------ສົ່ງເມລ໌ພາສາລາວ-------------
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def sendthai(sendto, subj="ທົດສອບສົ່ງອີເມລລ໌", detail="ສະບາຍດີ!\nເຈົ້າສະບາຍດີບໍ?\n"):

    myemail = 'thitphavanh23@gmail.com'
    mypassword = 'hery18205208038'
    receiver = sendto

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subj
    msg['From'] = 'ຈາກ Phenomenal Bottega'
    msg['To'] = receiver
    text = detail

    part1 = MIMEText(text, 'plain')
    msg.attach(part1)

    s = smtplib.SMTP('smtp.gmail.com:587')
    s.ehlo()
    s.starttls()

    s.login(myemail, mypassword)
    s.sendmail(myemail, receiver.split(','), msg.as_string())
    s.quit()
    print('ສົ່ງແລ້ວ!')

#-------------Start sending-------------
subject = 'ຍືນຍັນການສະໝັກ Website E-Commerce !! Phenomenal Bottega'
newmember_name = 'Annie'
content = '''
ເນື່ອງຈາກຄວາມປອດໄພຂອງການເຂົ້າໃຊ້
ກະລູນາຍືນຍັນອີເມລ໌ ຜ່ານລິ້ງຄ໌ດ້ານລຸ່ມ
'''
link = 'http://phenomenal.com/confirm/ph12345'

msg = 'ສະບາຍດີ {} \n\n {} Verify Link : {}'.format(newmember_name, content, link)

sendthai('thitphavanh23@gmail.com, thitphavanh.psv@gmail.com', subject, msg)






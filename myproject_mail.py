import gmail

email_id='example@gmail.com'        #ONLY GMAIL ID!
app_pass='enter your gmail app password here'

def acn_opening(user,acno,acn_open_date,acn_pass,recipient):
    con_gmail=gmail.GMail(email_id,app_pass)
    subject_mail='ABC Bank - Opening your account'
    body=f'''Dear {user},

Congratulations! Your account having account number {acno} has been successfully opened in ABC Bank on {acn_open_date}.
Your temporary password is {acn_pass}. Kindly change your password once you login.

Thanks & regards,
ABC Bank'''
    acn_opening_msg=gmail.Message(to=recipient,subject=subject_mail,text=body)
    con_gmail.send(acn_opening_msg)


def acn_deletion(acno,user,otp,recipient):
    con_gmail=gmail.GMail(email_id,app_pass)
    subject_mail=f'ABC Bank - OTP for closing account {acno}'
    body=f'''Dear {user},

Your OTP for closing account {acno} is {otp}. Kindly share this OTP with the authorized bank official.

Thanks & Regards,
ABC Bank'''
    acn_closure_msg=gmail.Message(to=recipient,subject=subject_mail,text=body)
    con_gmail.send(acn_closure_msg)
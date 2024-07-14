import smtplib, ssl

# The SMTP server configuration remains as defined by your teammate
smtp_server = "smtp.gmail.com"
port = 465
sender_email = "sublimecosc310@gmail.com"
sender_password = "syjo thtf nbxw gxbr"

# This function now purely focuses on sending the verification email
def send_verification_email(receiver_email, verification_code):
    # The message to be sent is formatted with the verification code
    message = f"""\
Subject: Your Verification Code

Your verification code is: {verification_code}

Please enter this code on our website to verify your email address. Thank you for joining us!"""

    context = ssl.create_default_context()
    try:
        # Securely connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message)
            print(f"Verification email sent to {receiver_email}.")
    except smtplib.SMTPException as e:
        # Graceful error handling in case of any issue while sending the email
        print(f"Failed to send verification email to {receiver_email}: {e}")



# from django.core.mail import BadHeaderError, send_mail
# from django.http import HttpResponse, HttpResponseRedirect
#
#
# def send_email(request):
#     subject = request.POST.get("subject", "")
#     message = request.POST.get("message", "")
#     from_email = request.POST.get("from_email", "")
#     if subject and message and from_email:
#         try:
#             send_mail(subject, message, from_email, ["admin@example.com"])
#         except BadHeaderError:
#             return HttpResponse("Invalid header found.")
#         return HttpResponseRedirect("/contact/thanks/")
#     else:
#         return HttpResponse("Make sure all fields are entered and valid.")


# settings.py
# from decouple import config

# EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_POST = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = config("EMAIL_HOST_USER")
# EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")
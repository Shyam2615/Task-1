# import json
# import os
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from dotenv import load_dotenv

# load_dotenv()

# def send_email(event, context):
#     try:
#         body = json.loads(event['body'])
#     except Exception as e:
#         return {
#             "statusCode": 400,
#             "body": json.dumps({
#                 "error": str(e),
#                 "message" : "please Enter the required fields"
#             })
#         }

#     receiver_email = body.get('receiver_email')
#     subject = body.get('subject')
#     body_text = body.get('body_text')

#     if not receiver_email:
#         return {
#             "statusCode": 400,
#             "body": json.dumps({
#                 "message": "Missing required fields: receiver_email"
#             })
#         }
#     if not subject:
#         return {
#             "statusCode": 400,
#             "body": json.dumps({
#                 "message": "Missing required fields: subject"
#             })
#         }
#     if not body_text:
#         return {
#             "statusCode": 400,
#             "body": json.dumps({
#                 "message": "Missing required fields: body_text"
#             })
#         }

#     sender_email = os.environ.get('EMAIL')
#     password = os.environ.get('PASSWORD')

#     msg = MIMEMultipart()
#     msg['From'] = sender_email
#     msg['To'] = receiver_email
#     msg['Subject'] = subject
#     msg.attach(MIMEText(body_text, 'plain'))

#     try:
#         server = smtplib.SMTP('smtp.gmail.com', 587)
#         server.set_debuglevel(1)
#         server.starttls()
#         server.login(sender_email, password)
#         text = msg.as_string()
#         server.sendmail(sender_email, receiver_email, text)
#         server.quit()

#         return {
#             "statusCode": 200,
#             "body": json.dumps({
#                 "message": "Email sent successfully"
#             })
#         }
#     except Exception as e:
#         return {
#             "statusCode": 500,
#             "body": json.dumps({
#                 "message": "Failed to send email",
#                 "error": str(e)
#             })
#         }



import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(event, context):
    print("Received event:", event)
    try:
        body = json.loads(event['body'])
        receiver_email = body['receiver_email']
        subject = body['subject']
        body_text = body['body_text']

        smtp_username = os.environ.get('SMTP_USERNAME')
        smtp_password = os.environ.get('SMTP_PASSWORD')

        if not (smtp_username and smtp_password):
            raise ValueError("SMTP credentials not configured correctly")

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as smtp_conn:
            smtp_conn.starttls()
            smtp_conn.login(smtp_username, smtp_password)

            message = MIMEMultipart()
            message['From'] = smtp_username
            message['To'] = receiver_email
            message['Subject'] = subject

            message.attach(MIMEText(body_text, 'plain'))

            smtp_conn.sendmail(smtp_username, receiver_email, message.as_string())

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'message': 'Email sent successfully'})
        }

    except ValueError as ve:
        return {
            'statusCode': 400,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(ve)})
        }

    except smtplib.SMTPAuthenticationError:
        return {
            'statusCode': 401,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': 'SMTP authentication failed. Check your credentials.'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'error': str(e)})
}
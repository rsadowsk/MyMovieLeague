from MovieLeague import SGMail, app
from sendgrid.helpers.mail import *
from itsdangerous import URLSafeSerializer



class SendEmail(object):
    def __init__(self):
        self.serial = URLSafeSerializer(app.config["SECRET_KEY"])
        self.sg = SGMail

    def send_invite_email(self, sender, league, to_email):
        from_email = Email("no-reply@movieleague.co.uk")
        to_email = Email(to_email)
        subject = "Invite to join %s" % league
        content = Content("text/plain", "%s has invited you to join %s") % sender, league
        mail = Mail(from_email, subject, to_email, content)
        response = self.sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)

    def token_dump(self, data):
        return self.serial.dumps(data)

    def token_load(self, token):
        return self.serial.loads(token)

if __name__ == '__main__':
    se = SendEmail()
    a = 'test'
    token = se.token_dump(a)
    print token
    print se.token_load('InRlc3RlZCI.-BiqYaFjRr4pDK6CJk99sAWBLxY')

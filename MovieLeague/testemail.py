from MovieLeague import SGMail, app
from sendgrid.helpers.mail import *
from itsdangerous import URLSafeSerializer
import jinja2


class SendEmail(object):
    def __init__(self):
        self.serial = URLSafeSerializer(app.config["SECRET_KEY"])
        self.sg = SGMail
        self.template = "./template/email_template.html"

    def send_invite_email(self, sender, league, to_email):
        j2_env=jinja2.Environment(loader=jinja2.FileSystemLoader('templates'), trim_blocks=True)
        template=j2_env.get_template('email_template.html')
        from_email = Email("no-reply@mymovieleague.com")
        to_email = Email(to_email)
        subject = "Invite to join %s" % league
        html = template.render(sender=sender, league=league, token=self.token_dump(league))

        content = Content("text/html", html)
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
    se.send_invite_email("TestPlayer1","testleague","richard.j.sadowski@gmail.com")

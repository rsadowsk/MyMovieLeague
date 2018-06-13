from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.fields.html5 import DateField
from wtforms import validators, ValidationError
from wtforms.validators import InputRequired, Email, Length
import re, htmlentitydefs


def validate_date(form, field):
    year = field.data.year
    if int(year) < 2015:
        raise ValidationError('Year must be after 2015')
    if int(year) > 2050:
        raise ValidationError('Year must be before 2050')


def fix_special_characters(form, text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is

    text = str(text)
    ret = re.sub("&#?\w+;", fixup, text)
    if str(ret) != text:
        raise ValidationError('Special characters are not allowed.')



class CreateLeagueForm(FlaskForm):
    league_name = StringField("League Name",
                              validators=[validators.DataRequired("Please enter a valid name."),
                                          fix_special_characters])
    start_date = DateField('Start Date', format='%Y-%m-%d',
                           validators=[validators.DataRequired("Please enter a valid date."),
                                       validate_date])
    end_date = DateField('End Date', format='%Y-%m-%d',
                         validators=[validators.DataRequired("Please enter a valid date."),
                                     validate_date])
    end_record = DateField('End Record', format='%Y-%m-%d',
                           validators=[validators.DataRequired("Please enter a valid date."),
                                       validate_date])
    submit = SubmitField("Create")

    def validate(self):
        if not FlaskForm.validate(self):
            return False
        ret = True
        if self.start_date.data >= self.end_date.data:
            self.end_date.errors.append("End Date must be after Start Date")
            ret = False
        if self.end_date.data > self.end_record.data:
            self.end_record.errors.append("End Record must be after or equal to End Date")
            ret = False
        return ret


class ManageUsersMovies(FlaskForm):
    name = StringField("Name", id="UsersName")
    movie = StringField("Movie", id="UsersMovie")
    ret = HiddenField(id='ret')
    submit = SubmitField("Submit")


class InviteFriends(FlaskForm):
    email = StringField("Email", id="email_0",
                        validators=[validators.DataRequired(), validators.Email()],
                        description="email...")
    submit = SubmitField("Invite")


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


if __name__=='__main__':
    fix_special_characters(None, '<input id="league_name" name="league_name" type="text" value="We&#x27;re Testing This">')

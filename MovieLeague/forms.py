from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms import validators, ValidationError


def validate_date(form, field):
    year = field.data.year
    if int(year) < 2015:
        raise ValidationError('Year must be after 2015')
    if int(year) > 2050:
        raise ValidationError('Year must be before 2050')


class CreateLeagueForm(Form):
    league_name = StringField("League Name",
                              validators=[validators.DataRequired("Please enter a valid name.")])
    start_date = DateField('Start Date', format='%Y-%m-%d',
                           validators=[validators.DataRequired("Please enter a valid date."),
                                       validate_date])
    end_date = DateField('End Date', format='%Y-%m-%d',
                         validators=[validators.DataRequired("Please enter a valid date."),
                                     validate_date])
    end_record = DateField('End Record', format='%Y-%m-%d',
                           validators=[validators.DataRequired("Please enter a valid date."),
                                       validate_date])
    submit = SubmitField("Enter Test Stuff")

    def validate(self):
        if not Form.validate(self):
            return False
        ret = True
        if self.start_date.data >= self.end_date.data:
            self.end_date.errors.append("End Date must be after Start Date")
            ret = False
        if self.end_date.data > self.end_record.data:
            self.end_record.errors.append("End Record must be after or equal to End Date")
            ret = False
        return ret


class ManageUsersMovies(Form):
    name = StringField("Name", id="UsersName")

    movie = StringField("Movie", id="UsersMovie")
    submit = SubmitField("Enter Test Stuff")


if __name__=='__main__':
    pass

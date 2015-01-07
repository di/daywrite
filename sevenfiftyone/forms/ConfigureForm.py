from flask.ext.wtf import Form
from wtforms import SelectField, SubmitField
from wtforms.validators import Required
import pytz

class ConfigureForm(Form):
    timezone = SelectField('Timezone', [Required()], description="Choose a timezone", choices=[(x, x) for x in pytz.common_timezones])

    submit = SubmitField('Save')

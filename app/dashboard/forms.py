from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
from app.models import Files


class UploadFile(FlaskForm):
    #uploaded_file = FileField('Upload File', validators=[DataRequired(),FileAllowed(['jpg', 'png' , 'pdf'])])
    uploaded_file = FileField('Upload File', validators=[DataRequired()])
    upload = SubmitField('Upload')

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, MultipleFileField


class FilesForm(FlaskForm):
    files = MultipleFileField(
        'Multiple Files',
        validators=[
            FileAllowed(['png', 'jpg', 'bmp'])
        ]
    )
    submit = SubmitField('Upload')

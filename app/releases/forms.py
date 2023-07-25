from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, StringField, MultipleFileField
from wtforms.validators import DataRequired


class ReleaseForm(FlaskForm):
    def __init__(self, last_version, *args, **kwargs):
        super(ReleaseForm, self).__init__(*args, **kwargs)
        self.last_version = last_version
        self.version.description = 'Inserisci la versione del rilascio, l\'ultima versione è la ' \
                                   + str(last_version) if last_version else ''
        # self.version.render_kw = {'placeholder': str(float(last_version) + 0.1) if last_version else '0.1'}

    version = StringField(
        'Versione',
        validators=[DataRequired()],
    )
    files = MultipleFileField('Carica il/i Documento/i', validators=[
        FileRequired(),
        FileAllowed('pdf', 'Solo file PDF!'),
    ])
    submit = SubmitField('Carica')

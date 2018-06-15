from wtforms import Form, validators, IntegerField, FloatField, StringField

class TransactionForm(Form):
    sender = IntegerField('sender', [validators.NumberRange(min=1)])
    receiver = IntegerField('receiver', [validators.NumberRange(min=1)])
    amount = FloatField('amount', [validators.NumberRange(min=0)])
    #base64exp = '^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$'
    #signature = StringField('signature', [validators.Regexp(base64exp)])
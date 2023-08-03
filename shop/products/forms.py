from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import Form, StringField, TextAreaField, PasswordField, SubmitField, validators, ValidationError
from wtforms.validators import DataRequired, Email, NumberRange
from flask_wtf import FlaskForm
from wtforms import Form, IntegerField, StringField, DecimalField, TextAreaField, validators

class Addproducts(Form):
    name = StringField('Name', [validators.DataRequired()])
    price = DecimalField('Price',[validators.DataRequired()])
    discount = IntegerField('Discount', default=0)
    stock = IntegerField('Stock', [validators.DataRequired()])
    desc =TextAreaField('Description', [validators.DataRequired()])
    colors = TextAreaField('Colors', [validators.DataRequired()])
    
    image_1 = FileField('Image 1', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_2 = FileField('Image 2', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])
    image_3 = FileField('Image 3', validators=[FileAllowed(['jpg', 'png', 'gif', 'jpeg'])])

class ProductReviewForm(FlaskForm):
    content = TextAreaField('Review Content', validators=[DataRequired()])
    rating = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])

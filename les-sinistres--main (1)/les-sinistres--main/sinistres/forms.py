from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, SelectField
import wtforms
from wtforms.validators import DataRequired, Length, Email, EqualTo

from wtforms import DateField
class RegistrationForm(FlaskForm):
    username = StringField('Nom client',
                           validators=[DataRequired()])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    pivot = FloatField('Pivôt(en mm)', validators=[DataRequired()])
    couts = FloatField('Couts fixes journalier(en €)',
                                     validators=[DataRequired()])
    
    ca= FloatField(' Chiffre d affaire max possible journalier(en €)',
                                     validators=[DataRequired()])
    date1 = DateField('Date de début de contrat', format='%d/%m/%Y')
  
    v = [('1', 'Nice'), ('2', 'Lyon'), ('3', 'Paris'), ('4', 'Brest'), ('5', 'Lille'), 
         ('6', 'Strasbourg'), ('7', 'Toulouse'),
         ('8', 'Renne'),
         ('9', 'Marseille'),
         ('10', 'Aix-en-Provence'),
         ('11', 'Perpignan'),
         ('12', 'Grenoble'),
         ('13', 'Bordeaux'),
         ('14', 'Nîmes'),
         ('15', 'Cannes'),
         ('16', 'Angers'),
         ('17', 'Avignon'),
         ('18', 'Dijon'),
         ('19', 'Clermont-Ferrand'),
         ('20', 'Biarritz'),
         ('21', 'Metz'),
         ('22', 'Orléans'),
         ('23', 'Annecy'),
         ('24', 'Troyes'),
         ('25', 'Pau'),
         ('26', 'Quimper'),
         ('27', 'Caen'),
         ('28', 'Rouen'),
         ('29', 'Limoges')]
    ville = SelectField('Ville', choices=v)
    

    submit1 = SubmitField('imprimer')



class LoginForm(FlaskForm):
    v = [('1', 'Nice'), 
         ('2', 'Lyon'),
         ('3', 'Paris'), 
         ('4', 'Brest'),
         ('5', 'Lille'), 
         ('6', 'Strasbourg'),
         ('7', 'Toulouse'),
         ('8', 'Renne'),
         ('9', 'Marseille'),
         ('10', 'Aix-en-Provence'),
         ('11', 'Perpignan'),
         ('12', 'Grenoble'),
         ('13', 'Bordeaux'),
         ('14', 'Nîmes'),
         ('15', 'Cannes'),
         ('16', 'Angers'),
         ('17', 'Avignon'),
         ('18', 'Dijon'),
         ('19', 'Clermont-Ferrand'),
         ('20', 'Biarritz'),
         ('21', 'Metz'),
         ('22', 'Orléans'),
         ('23', 'Annecy'),
         ('24', 'Troyes'),
         ('25', 'Pau'),
         ('26', 'Quimper'),
         ('27', 'Caen'),
         ('28', 'Rouen'),
         ('29', 'Limoges')]
    ville = SelectField('Ville', choices=v)
    pivot = FloatField('Pivôt(en mm)', validators=[DataRequired()])
    couts = FloatField('Couts fixes journalier(en €)',
                                     validators=[DataRequired()])
    
    ca= FloatField(' Chiffre d affaire max possible journalier(en €)',
                                     validators=[DataRequired()])
    submit = SubmitField('Confirmer formulaire')
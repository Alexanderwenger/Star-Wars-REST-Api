from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__= 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = "people"
    uid = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique = False, nullable = False )
    height = db.Column(db.Integer, unique = False, nullable = True )
    gender = db.Column(db.String(40), unique = False, nullable = True )

    def __repr__(self):
        return '<People %r>' %self.name

    def serialize (self):
        return {
            "uid": self.uid,
            "name": self.name,
            "height": self.height,
            "gender": self.gender
        }
class Planets(db.Model):
    __tablename__ = "planets"
    uid = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), unique = False, nullable = False )

    def __repr__(self):
        return '<Planets %r>' %self.name

    def serialize (self):
        return {
            "uid": self.uid,
            "name": self.name,
        }

class FavPeople(db.Model):
    __tablename__= 'favpeople'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), db.ForeignKey('user.email'))
    people = db.Column(db.Integer, db.ForeignKey('people.uid'))
    rel_user = db.relationship('User')
    rel_people = db.relationship('People')

    def __repr__(self):
        return '<FavPeople %r>' %self.id

    def serialize (self):
        return {
            "id": self.id,
            "user": self.user,
            "people": self.people
        }

class FavPlanets(db.Model):
    __tablename__= 'favplanets'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(120), db.ForeignKey('user.email'))
    planet = db.Column(db.Integer, db.ForeignKey('planets.uid'))
    rel_user = db.relationship('User')
    rel_planets = db.relationship('Planets')

    def __repr__(self):
        return '<FavPlanets %r>' %self.id

    def serialize (self):
        return {
            "id": self.id,
            "user": self.user,
            "planet": self.planet
        }
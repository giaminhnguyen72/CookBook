from ..app import db

class Recipe(db.Model):
    __tablename__ = 'recipe'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10000000), nullable=False)
    cookingTime = db.Column(db.String(10000000), nullable=False)
    ingredient = db.Column(db.String(10000000), nullable=False)
    description = db.Column(db.String(10000000), nullable=False)
    directions = db.Column(db.String(10000000), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


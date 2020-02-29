from datetime import datetime
from database.sqlalchemy import db


class Textbook(db.Model):
    __tablename__ = 'textbooks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    users = db.relationship(
        'User', backref=db.backref('textbooks'), lazy=True)
    chapters = db.relationship(
        'Chapter', backref=db.backref('textbooks'), lazy=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Textbook %r>' % self.name

    def get_all_textbook():
        return db.session.query(Textbook).all()

    def get_textbook(textbook_id):
        return db.session.query(Textbook).filter_by(id=textbook_id).first()

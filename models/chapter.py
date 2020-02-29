from datetime import datetime
from database.sqlalchemy import db


class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    textbook_id = db.Column(db.Integer, db.ForeignKey(
        'textbooks.id'), nullable=False)
    words = db.relationship(
        'Word', backref=db.backref('chapters'), lazy=True)
    users = db.relationship(
        'User', backref=db.backref('chapters'), lazy=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Chapter %r>' % self.name

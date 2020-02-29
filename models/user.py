from datetime import datetime
from database.sqlalchemy import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    line_id = db.Column(db.String(255), nullable=False)
    textbook_id = db.Column(db.Integer, db.ForeignKey(
        'textbooks.id'), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapters.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<User %r>' % self.line_id

    def get_user(line_id):
        print('searching line user id: ' + line_id)
        return db.session.query(User).filter_by(line_id=line_id).first()

    def create_user(line_id):
        newUser = User(line_id=line_id, textbook_id=5, chapter_id=1)
        db.session.add(newUser)
        db.session.commit()

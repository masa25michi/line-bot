from datetime import datetime
from database.sqlalchemy import db
from models import User, Textbook, Chapter


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapters.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    meaning = db.Column(db.String(255), nullable=False)
    example = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return '<Chapters %r>' % self.name

    def get_words(user_line_id):
        return Word.query.join(Chapter, Chapter.id == Word.chapter_id).join(Textbook, Textbook.id == Chapter.textbook_id).join(
            User, User.textbook_id == Textbook.id).filter(User.line_id == user_line_id).filter(User.chapter_id == Chapter.id).all()

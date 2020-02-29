from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.config.from_object('database.config.Config')

db = SQLAlchemy(app)


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
        return '<Words %r>' % self.name

    def get_words(user_line_id):
        return Word.query.join(Chapter, Chapter.id == Word.chapter_id).join(Textbook, Textbook.id == Chapter.textbook_id).join(
            User, User.textbook_id == Textbook.id).filter(User.line_id == user_line_id).filter(User.chapter_id == Chapter.id).all()


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


Migrate(app, db)

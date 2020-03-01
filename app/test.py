from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort
from flask_migrate import Migrate
from datetime import datetime
import pandas as pd
import numpy as np

app = Flask(__name__)
app.config.from_object('database.config.Config')

db = SQLAlchemy(app)


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey(
        'chapters.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    spell = db.Column(db.String(255), nullable=False)
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

    def get_word(name):
        print('searching word: ' + name)
        return db.session.query(Word).filter_by(name=name).first()

    def get_words_by_chapter(chapter_id):
        return db.session.query(Word).filter_by(chapter_id=chapter_id).all()

    def create_word(name, spell, meaning, chapter_id):
        # check if already exists
        if (Word.get_word(name) != None):
            print('Word Already Existed')
            return 0

        print('Creating ' + name)

        new_word = Word(name=name, spell=spell,
                        meaning=meaning, chapter_id=chapter_id)
        db.session.add(new_word)
        db.session.commit()

        return 1


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

    def get_chapter(name, textbook_id):
        return db.session.query(Chapter).filter_by(textbook_id=textbook_id, name=name).first()

    def create_chapter(textbook_id, chapter_number):
        new_chapter_name = 'Chapter ' + str(chapter_number)

        # check if already exists
        if (Chapter.get_chapter(new_chapter_name, textbook_id) != None):
            print('Chapter Already Existed')
            return 0

        new_chapter = Chapter(textbook_id=textbook_id, name=new_chapter_name)
        db.session.add(new_chapter)
        db.session.commit()

        return 1


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

words_df = pd.read_excel('~/Desktop/n2.xls', skiprows=[0, 1, 2, 3])

word_counts = 1
chapter_count = 1
new_words_len = len(words_df)

textbook = Textbook.get_textbook(2)

if textbook != None:
    # number_of_chapters_need = round(new_words_len / 10) + 2
    number_of_chapters_need = 3

    for chapter_number in range(number_of_chapters_need):
        Chapter.create_chapter(textbook.id, chapter_number + 1)

for index, word in words_df.iterrows():
    chapter_name = 'Chapter ' + str(chapter_count)
    chapter = Chapter.get_chapter(chapter_name, textbook.id)
    chapter_id = chapter.id

    word_name = word['漢字']
    word_spell = word['単語']
    word_meaning = word['意味']

    if isinstance(word_name, str) == False:
        word_name = word_spell

    if Word.get_word(word_name) != None:
        continue

    while Word.get_words_by_chapter(chapter_id) != None and len(Word.get_words_by_chapter(chapter_id)) >= 10:
        chapter_count += 1

        chapter_name = 'Chapter ' + str(chapter_count)
        chapter = Chapter.get_chapter(chapter_name, textbook.id)
        chapter_id = chapter.id

    if Word.create_word(word_name, word_spell, word_meaning, chapter_id) == 0:
        continue

    word_counts += 1
    if word_counts == 10:
        chapter_count += 1

    if (chapter_count == number_of_chapters_need + 1):
        print('DONE')
        break

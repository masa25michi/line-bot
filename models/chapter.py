from datetime import datetime
from database.sqlalchemy import db


class Chapter(db.Model):
    __tablename__ = 'chapters'

    id = db.Column(db.Integer, primary_key=True)
    textbook_id = db.Column(db.Integer, db.ForeignKey(
        'textbooks.id'), nullable=False)
    number = db.Column(db.Integer)
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

    def get_next_chapter(textbook_id, chapter_id):
        # not chapter_id.....
        next_chapter_name = 'Chapter ' + chapter_id
        next_chapter = Chapter.get_chapter(next_chapter_name, textbook_id)

        if next_chapter == None and next_chapter_name != 'Chapter 1':
            next_chapter = Chapter.get_chapter('Chapter 1', textbook_id)

        if next_chapter == None:
            print('cannot found chapter')

        return next_chapter

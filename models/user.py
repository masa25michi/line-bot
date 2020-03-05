from datetime import datetime
from database.sqlalchemy import db
from models.chapter import Chapter


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

    def get_all_users():
        return db.session.query(User).all()

    def create_user(line_id):
        first_textbook_id = 2
        first_chapter_model = Chapter.get_chapter_by_number(
            1, first_textbook_id)
        newUser = User(line_id=line_id, textbook_id=2,
                       chapter_id=first_chapter_model.id)
        db.session.add(newUser)
        db.session.commit()

    def update_chapter(line_id):
        print('updating user chapter: ' + line_id)
        user = User.get_user(line_id)
        next_chapter_model = Chapter.get_next_chapter(user.chapter_id)

        if next_chapter_model != None:
            user.chapter_id = next_chapter_model.id
        db.session.commit()

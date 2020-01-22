from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, email_address, password):
        self.email_address = email_address
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email_address(cls, email_address):
        return cls.query.filter_by(email_address=email_address).first()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()

from urllib import parse

from flask import Flask, request
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://{}:{}@{}:{}/{}".format(DB_USER, parse.quote(DB_PASSWORD),
                                                                                DB_HOST, DB_PORT, DB_NAME)
db = SQLAlchemy()
migrate = Migrate()

db.init_app(app)
migrate.init_app(app, db)

with app.app_context():
    db.create_all()




class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_number = db.Column(db.String(15), nullable=False)
    email_address = db.Column(db.String(30), nullable=True)
    contact_type = db.Column(db.String(10), nullable=True)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'contact_number': self.contact_number,
            'email_address': self.email_address,
            'contact_type': self.contact_number
        }


@app.route("/contact", methods=["GET"])
@cross_origin()
def get_contacts():
    contacts = Contact.query.all()
    return [contact.serialize for contact in contacts]


@app.route("/contact/<int:id>", methods=["GET"])
@cross_origin()
def get_contact_by_id(id):
    contact = Contact.query.filter_by(id=id).first()
    return contact.serialize


@app.route("/contact/<int:id>", methods=["DELETE"])
@cross_origin()
def delete_contact_by_id(id):
    contact = Contact.query.filter_by(id=id).first()
    contact.delete()
    db.session.commit()
    return contact.serialize


@app.route("/contact", methods=["POST"])
@cross_origin()
def create_contact():
    data = request.json

    contact = Contact(name=data['name'],contact_number=data['contact_number'],
            email_address=data['email_address'], contact_type=data['contact_type'])
    db.session.add(contact)
    db.session.commit()
    return contact.serialize


@app.errorhandler(Exception)
@cross_origin(supports_credentials=True)
def handle_error(error):
    print(error)
    return {"Message": str(error)}


if __name__ == "__main__":
    app.run(debug=True)

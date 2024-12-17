from app import db


class Client(db.Model):
    __tablename__ = 'Client'

    person_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    lastname = db.Column(db.Text, nullable=False)
    firstname = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, unique=True)
    driver_license = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    trips = db.relationship('Trip', backref='client', lazy=True)


class Car(db.Model):
    __tablename__ = 'Cars'

    car_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model = db.Column(db.Text, nullable=False)
    status = db.Column(db.Text, nullable=False)
    location = db.Column(db.Text, nullable=False)
    license_plate = db.Column(db.Text, unique=True, nullable=False)

    trips = db.relationship('Trip', backref='car', lazy=True)


class Trip(db.Model):
    __tablename__ = 'Trips'

    trip_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, db.ForeignKey('Client.person_id'), nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('Cars.car_id', ondelete='CASCADE'), nullable=False)
    total_cost = db.Column(db.Float, nullable=False)

    fines = db.relationship('Fine', backref='trip', lazy=True)


class Fine(db.Model):
    __tablename__ = 'Fines'

    fine_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('Trips.trip_id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)



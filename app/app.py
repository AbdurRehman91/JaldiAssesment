import os, jwt, uuid, csv
from functools import wraps
from datetime import datetime, timedelta
from flask import Flask, render_template, request, redirect, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from flask_migrate import Migrate

app = Flask(__name__, static_folder='static')

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

if not 'WEBSITE_HOSTNAME' in os.environ:
   # local development, where we'll use environment variables
   app.config.from_object('app.settings.development')
else:
   # production
   print("Loading config.production.")
   app.config.from_object('app.settings.production')

app.config.update(
    SQLALCHEMY_DATABASE_URI=app.config.get('DATABASE_URI'),
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
)

from .models import db, User, Listing

# Initialize the database connection
#db = SQLAlchemy(app)
db.init_app(app) #Add this line Before migrate line

migrate = Migrate(app, db)

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'access_token' in request.headers:
            token = request.headers['access_token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'JWT token is required'}), 401
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except Exception as ex:
            print("= exception is : ",str(ex))
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(*args, **kwargs)
  
    return decorated

# Create user
@app.route('/user', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if user:
            return jsonify({'message': 'User already exists'})
        new_user = User(name=data['name'], password=generate_password_hash(data['password'], method='sha256'), 
        email=data['email'],public_id=str(uuid.uuid4()), phone_number=data['phone_number'], 
        user_address=data['user_address'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'})
    except Exception as ex:
        return jsonify({'error':str(ex)})

# Login
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'message': 'Invalid email or password'})
        user.login_count += 1
        db.session.commit()
        # generates the JWT Token
        token = jwt.encode({'public_id': user.public_id, 'exp' : datetime.utcnow() + timedelta(minutes = 60) }, 
        app.config['SECRET_KEY'])
        return make_response(jsonify({'message': 'Login successful', 'token':token.decode('UTF-8')}))
    except Exception as ex:
        return jsonify({'error':str(ex)})

# Get user data
@app.route('/user/<email>', methods=['GET'])
@token_required
def get_user_data(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({'name': user.name, 'email': user.email, 'phone_number': user.phone_number,
                            'user_address': user.user_address, 'login_count': user.login_count})
        else:
            return jsonify({'message': 'User not found'})
    except Exception as ex:
        return jsonify({'error':str(ex)})

# Generate listing
@app.route('/user/listing', methods=['POST'])
@token_required
def generate_listing():
    try:
        data = request.get_json()
        csv_fields = ['email', 'description','price', 'address']
        with open("./listing.csv", 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_fields)
            writer.writeheader()
            for row in data:
                user = User.query.filter_by(email=row['email']).first()
                if user:
                    writer.writerow(row)
                    new_listing = Listing(user = user.id, description = row['description'], 
                    price = row['price'], location_address = row['address'])
                    db.session.add(new_listing)
                    db.session.commit()
                else:
                    return jsonify({'message': 'User not found'})
        return make_response(jsonify({'message': 'File successfully created'}))
    except Exception as ex:
        return jsonify({'error':str(ex)})

@app.route('/user/listing/<email>', methods=['GET'])
@token_required
def get_user_listing(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            user_listing = Listing.query.filter_by(user = user.id)
            #user_listing = Listing.query.all()
            listingArr = []
            for listing in user_listing:
                listingArr.append(listing.toDict()) 
            return jsonify(listingArr)
        else:
            return jsonify({'message': 'User not found'})
    except Exception as ex:
        return jsonify({'error':str(ex)})

@app.route('/user/<email>', methods=['PUT'])
@token_required
def update_user(email):
    try:
        user = User.query.filter_by(email=email).first()
        if user:
            data = request.get_json()
            user.name = data['name']
            user.phone_number = data['phone_number']
            user.user_address = data['address']
            db.session.commit()
            return jsonify({'message': 'User updated successfully'})
        else:
            return jsonify({'message': 'User not found'})
    except Exception as ex:
        return jsonify({'error':str(ex)})

if __name__ == '__main__':
   app.run(debug=True)

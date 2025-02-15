# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate
from server.models import db, Earthquake  # Update import path to server.models

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Task #3: View to get earthquake by ID
@app.route('/earthquakes/<int:id>', methods=['GET'])
def get_earthquake(id):
    earthquake = Earthquake.query.filter_by(id=id).first()
    
    if earthquake:
        return jsonify({
            "id": earthquake.id,
            "location": earthquake.location,
            "magnitude": earthquake.magnitude,
            "year": earthquake.year
        })
    else:
        return jsonify({"message": f"Earthquake {id} not found."}), 404

# Task #4: View to get earthquakes by minimum magnitude
@app.route('/earthquakes/magnitude/<float:magnitude>', methods=['GET'])
def get_earthquakes_by_magnitude(magnitude):
    # Query the database to find all earthquakes with a magnitude greater than or equal to the provided value
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()

    # Return the count and data of matching earthquakes
    return jsonify({
        "count": len(earthquakes),
        "quakes": [
            {
                "id": quake.id,
                "location": quake.location,
                "magnitude": quake.magnitude,
                "year": quake.year
            } for quake in earthquakes
        ]
    })

if __name__ == '__main__':
    app.run(port=5555, debug=True)

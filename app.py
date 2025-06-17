from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///superheroes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to the Superheroes API!"})


@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [hero.to_dict() for hero in heroes]
    return jsonify(heroes_data), 200


@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": []
    }

    for hp in hero.hero_powers:
        hero_power_data = {
            "id": hp.id,
            "strength": hp.strength,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        }
        hero_data["hero_powers"].append(hero_power_data)

    return jsonify(hero_data), 200


@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{
        "id": power.id,
        "name": power.name,
        "description": power.description
    } for power in powers]
    return jsonify(powers_data), 200


@app.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data), 200


@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    data = request.get_json()
    description = data.get("description")

    if not description or len(description.strip()) < 20:
        return jsonify({"errors": ["Description must be at least 20 characters"]}), 400

    power.description = description.strip()
    db.session.commit()

    return jsonify({
        "id": power.id,
        "name": power.name,
        "description": power.description
    }), 200


@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    print("Received data:", data)

    strength = data.get("strength")
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")

    print("Parsed strength:", strength)
    print("Looking up Hero and Power...")

    valid_strengths = ["Strong", "Weak", "Average"]
    if not strength or strength not in valid_strengths:
        return jsonify({"errors": ["Strength must be one of: Strong, Weak, Average"]}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    print("Hero:", hero)
    print("Power:", power)

    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 400

    hero_power = HeroPower(
        strength=strength, hero_id=hero.id, power_id=power.id)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify({
        "id": hero_power.id,
        "hero_id": hero.id,
        "power_id": power.id,
        "strength": hero_power.strength,
        "hero": {
            "id": hero.id,
            "name": hero.name,
            "super_name": hero.super_name
        },
        "power": {
            "id": power.id,
            "name": power.name,
            "description": power.description
        }
    }), 201


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

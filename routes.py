from flask import Blueprint, request, jsonify, current_app as app
from flask_mail import Message
from app import mail
from models import db, Hero, Power, HeroPower

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return jsonify({"message": "Welcome to the Superheroes API!"}), 200


# GET /heroes — list all heroes
@api.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    return jsonify([hero.to_dict() for hero in heroes]), 200


# GET /heroes/<id> — get hero details with nested powers
@api.route('/heroes/<int:id>', methods=['GET'])
def get_hero_by_id(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404

    return jsonify(hero.to_dict()), 200


# GET /powers — list all powers
@api.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    return jsonify([power.to_dict() for power in powers]), 200


# GET /powers/<id> — get a single power
@api.route('/powers/<int:id>', methods=['GET'])
def get_power_by_id(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404

    return jsonify(power.to_dict()), 200


# PATCH /powers/<id> — update power's description
@api.route('/powers/<int:id>', methods=['PATCH'])
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

    return jsonify(power.to_dict()), 200


# POST /hero_powers — create a new hero_power association
@api.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()

    strength = data.get("strength")
    hero_id = data.get("hero_id")
    power_id = data.get("power_id")

    valid_strengths = ["Strong", "Weak", "Average"]
    if not strength or strength not in valid_strengths:
        return jsonify({"errors": ["Strength must be one of: Strong, Weak, Average"]}), 400

    hero = Hero.query.get(hero_id)
    power = Power.query.get(power_id)

    if not hero or not power:
        return jsonify({"errors": ["Hero or Power not found"]}), 400

    hero_power = HeroPower(strength=strength, hero_id=hero.id, power_id=power.id)
    db.session.add(hero_power)
    db.session.commit()

    return jsonify(hero_power.to_dict()), 201


# POST /send_email — send an email via Flask-Mail
@api.route('/send_email', methods=['POST'])
def send_email():
    data = request.get_json()

    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')

    # Validate required fields
    if not to or not subject or not body:
        return jsonify({"error": "Missing 'to', 'subject', or 'body' fields"}), 400

    try:
        msg = Message(
            subject=subject,
            recipients=[to],
            body=body,
            sender=app.config.get('MAIL_DEFAULT_SENDER') or app.config.get('MAIL_USERNAME')
        )
        mail.send(msg)
        return jsonify({"message": f"Email sent to {to}"}), 200

    except Exception as e:
        return jsonify({"error": f"Failed to send email: {str(e)}"}), 500

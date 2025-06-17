from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable=False)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates='hero',
        cascade='all, delete-orphan'
    )

    serialize_rules = ('-hero_powers.hero',)  # Prevent recursion
    serialize_only = ('id', 'name', 'super_name')

    def __repr__(self):
        return f"<Hero {self.name}>"


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates='power',
        cascade='all, delete-orphan'
    )

    serialize_rules = ('-hero_powers.power',)
    serialize_only = ('id', 'name', 'description')

    @validates('description')
    def validate_description(self, key, value):
        if not value or len(value.strip()) < 20:
            raise ValueError("Description must be at least 20 characters long.")
        return value

    def __repr__(self):
        return f"<Power {self.name}>"


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'
    __table_args__ = (db.UniqueConstraint('hero_id', 'power_id', name='unique_hero_power'),)

    
    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    hero = db.relationship('Hero', back_populates='hero_powers')
    power = db.relationship('Power', back_populates='hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')
    serialize_only = ('id', 'strength', 'hero_id', 'power_id')

    @validates('strength')
    def validate_strength(self, key, value):
        if value not in ['Strong', 'Weak', 'Average']:
            raise ValueError("Strength must be 'Strong', 'Weak', or 'Average'")
        return value

    def __repr__(self):
        return f"<HeroPower Hero={self.hero_id} Power={self.power_id} Strength={self.strength}>"
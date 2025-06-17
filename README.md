# Superhero API

A RESTful API built with Flask and SQLAlchemy for managing heroes, powers, and their associated strengths. This API is designed to support a simple frontend or client application that interacts with superhero data.

## Features

- CRUD operations for heroes and powers
- Create associations between heroes and powers with strengths
- Input validation to ensure data integrity
- JSON responses compatible with client-side applications

## Technologies Used

- Python 3.x
- Flask
- SQLAlchemy
- Flask SQLAlchemy
- Flask Migrate
- SQLAlchemy Serializer Mixin
- SQLite (default)

## Project Structure

├── app.py
├── models.py
├── seed.py
├── README.md
├── requirements.txt
├── migrations/
└──pyrightconfig.json

## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Emananii/Superheroes.git
cd Superheroes

### 2. Create and Activate a Virtual Environment (Optional but Recommended)

python3 -m venv venv
source venv/bin/activate(MacOs)

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Database Migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

### 5. Seed the Database
python3 -m seed

### 6. Run the Server
python app.py

## License

This project is licensed under the MIT License.

## Author
Emmanuel Wambugu Ndiritu
# Superhero API
A RESTful API built with Flask and SQLAlchemy for managing heroes, powers, and the strength of their associations. This project simulates a backend system that could be used by a superhero database application, allowing clients to fetch data, assign powers to heroes, and define how strong a particular power is for a given hero.

## Features

🦸 Full CRUD operations for Heroes and Powers

🧬 Assign Powers to Heroes with customizable strengths (e.g., "Strong", "Average", "Weak")

🔒 Input validation to prevent bad data (e.g., blank fields, unsupported values)

🔁 Consistent JSON responses for seamless frontend integration

⚙️ Built using RESTful principles

## Technologies Used

Python 3.x

Flask — web framework

Flask SQLAlchemy — ORM integration

Flask Migrate — database migrations

SQLAlchemy Serializer Mixin — object serialization

SQLite — development database

## Project Structure
```
Superheroes/
├── app.py                 # Main app entry point
├── models.py              # SQLAlchemy models
├── seed.py                # Seed data for local testing
├── README.md              # This documentation
├── requirements.txt       # Python dependencies
├── pyrightconfig.json     # Optional type checking config
└── migrations/            # Auto-generated migration files
```
## Setup Instructions

### 1. Clone the Repository

git clone https://github.com/Emananii/Superheroes.git
cd Superheroes

### 2. (Optional) Create and Activate a Virtual Environment

python3 -m venv venv
source venv/bin/activate  # Mac/Linux
#### or
venv\Scripts\activate     # Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Database Migrations

flask db init
flask db migrate -m "Initial migration"
flask db upgrade

### 5. Seed the Database

python3 -m seed

### 6. Start the Development Server

python app.py

## How to Use the API
Once the server is running, access endpoints using a REST client like Postman, Insomnia, or simply via curl.

### Example Endpoints
#### GET /heroes
Fetch all heroes

#### GET /powers
Fetch all powers

#### GET /heroes/<id>
View detailed info about a hero and their powers

#### PATCH /powers/<id>
Update a power's description

#### POST /hero_powers
Assign a power to a hero with a specified strength
Body Example:

{
  "hero_id": 1,
  "power_id": 3,
  "strength": "Average"
}
Example Hero Response

{
  "id": 1,
  "name": "Storm",
  "super_name": "Ororo Munroe",
  "powers": [
    {
      "id": 2,
      "name": "Weather Control",
      "description": "Ability to control the weather",
      "strength": "Strong"
    }
  ]
}

## 🚫 Known Limitations

No authentication or rate limiting

No pagination or filtering on list endpoints

SQLite used for development — not suitable for production

No deployed version or Swagger/OpenAPI documentation (yet)

## 💡 Future Improvements
Add unit tests

Support power-level evolution over time

Add user roles for admins/editors
 
Integrate with a frontend (React, Vue, etc.)

##📬 Contact
For support, questions, or suggestions:

Emmanuel Wambugu Ndiritu
📧 emmanuelwambugu5@gmail.com
🔧 GitHub: @Emananii

📄 License
This project is licensed under the MIT License.


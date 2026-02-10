# Visual Task Board - Backend

Flask-based REST API for the Visual Task Board application.

## Technology Stack

- **Framework**: Flask 3.0
- **ORM**: SQLAlchemy
- **Database**: MySQL
- **Testing**: pytest, Hypothesis
- **Code Formatting**: Black

## Project Structure

```
backend/
├── models/          # Database models (Board, List, Card)
├── routes/          # API route handlers
├── services/        # Business logic layer
├── utils/           # Utility functions and validators
├── tests/           # Unit and integration tests
├── app.py           # Flask application entry point
├── config.py        # Configuration settings
└── requirements.txt # Python dependencies
```

## Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update the database connection string:

```bash
cp .env.example .env
```

### 4. Initialize Database

```bash
python -c "from app import db; db.create_all()"
```

### 5. Run Development Server

```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Testing

Run all tests:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=. --cov-report=html
```

Run property-based tests:
```bash
pytest tests/test_properties.py
```

## API Endpoints

### Boards
- `GET /api/boards` - Get all boards
- `POST /api/boards` - Create a new board
- `GET /api/boards/:id` - Get a specific board
- `PUT /api/boards/:id` - Update a board
- `DELETE /api/boards/:id` - Delete a board

### Lists
- `GET /api/boards/:boardId/lists` - Get all lists in a board
- `POST /api/boards/:boardId/lists` - Create a new list
- `GET /api/lists/:id` - Get a specific list
- `PUT /api/lists/:id` - Update a list
- `DELETE /api/lists/:id` - Delete a list
- `PUT /api/lists/:id/position` - Update list position

### Cards
- `GET /api/lists/:listId/cards` - Get all cards in a list
- `POST /api/lists/:listId/cards` - Create a new card
- `GET /api/cards/:id` - Get a specific card
- `PUT /api/cards/:id` - Update a card
- `DELETE /api/cards/:id` - Delete a card
- `PUT /api/cards/:id/move` - Move a card

## Code Formatting

Format code with Black:
```bash
black .
```

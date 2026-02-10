# Visual Task Board

A visual task management tool similar to Trello, built with Vue.js and Flask.

## Overview

Visual Task Board is a web-based application that helps you organize and track work using a three-tier structure:
- **Boards**: Top-level workspaces for different projects
- **Lists**: Columns within boards representing workflow stages
- **Cards**: Individual tasks with details like descriptions, due dates, and tags

## Features

- ✅ Create and manage multiple boards
- ✅ Add unlimited lists to organize workflow stages
- ✅ Create cards with titles, descriptions, due dates, and tags
- ✅ Drag and drop cards between lists
- ✅ Drag and drop lists to reorder them
- ✅ Real-time data persistence
- ✅ Responsive design for all devices
- ✅ RESTful API architecture

## Technology Stack

### Frontend
- Vue.js 3
- Vuex 4 (State Management)
- Axios (HTTP Client)
- Vue.Draggable (Drag & Drop)
- Jest (Testing)

### Backend
- Python Flask
- SQLAlchemy (ORM)
- MySQL (Database)
- pytest + Hypothesis (Testing)

### Deployment
- Docker & Docker Compose
- Nginx (Frontend Server)

## Project Structure

```
visual-task-board/
├── backend/              # Flask API server
│   ├── models/          # Database models
│   ├── routes/          # API endpoints
│   ├── services/        # Business logic
│   ├── utils/           # Utilities
│   └── tests/           # Backend tests
├── frontend/            # Vue.js application
│   ├── src/
│   │   ├── components/  # Vue components
│   │   ├── store/       # Vuex store
│   │   └── services/    # API services
│   └── tests/           # Frontend tests
└── .kiro/               # Project specifications
    └── specs/
        └── visual-task-board/
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- MySQL 8.0+
- Docker & Docker Compose (for containerized deployment)

### Quick Start with Docker (Recommended)

The easiest way to run the application is using Docker Compose:

```bash
# Clone the repository
git clone <repository-url>
cd visual-task-board

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The application will be available at:
- **Frontend**: http://localhost
- **Backend API**: http://localhost:5000
- **MySQL**: localhost:3306

### Development Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure database
cp .env.example .env
# Edit .env with your database configuration:
# DATABASE_URL=mysql+pymysql://user:password@localhost:3306/kanban

# Run migrations
python migrate.py

# Start development server
python app.py
```

The backend API will be available at http://localhost:5000

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run serve
```

The frontend will be available at http://localhost:8080

### Docker Deployment

#### Architecture

The Docker deployment consists of three services:

1. **MySQL Database** (port 3306)
   - Persistent data storage with Docker volumes
   - Automatic initialization with schema

2. **Flask Backend** (port 5000)
   - Python Flask API server
   - Connects to MySQL database

3. **Nginx Frontend** (port 80)
   - Serves Vue.js static files
   - Proxies API requests to backend

#### Configuration

The `docker-compose.yml` file defines all services and their configuration:

```yaml
services:
  mysql:      # Database service
  backend:    # Flask API
  frontend:   # Nginx + Vue.js
```

#### Environment Variables

Backend environment variables (configured in docker-compose.yml):
- `DATABASE_URL`: MySQL connection string
- `FLASK_ENV`: Application environment (production/development)

#### Data Persistence

MySQL data is persisted using Docker volumes:
```bash
# View volumes
docker volume ls

# Backup database
docker exec kanban-mysql mysqldump -u kanban_user -pkanban_password kanban > backup.sql

# Restore database
docker exec -i kanban-mysql mysql -u kanban_user -pkanban_password kanban < backup.sql
```

#### Troubleshooting

**Backend not connecting to database:**
```bash
# Check if MySQL is healthy
docker-compose ps

# View backend logs
docker-compose logs backend

# Restart backend service
docker-compose restart backend
```

**Frontend not loading:**
```bash
# Check Nginx logs
docker-compose logs frontend

# Rebuild frontend
docker-compose up -d --build frontend
```

**Reset everything:**
```bash
# Stop and remove all containers, networks, and volumes
docker-compose down -v

# Rebuild and start
docker-compose up -d --build
```

## Testing

### Backend Tests

```bash
cd backend
pytest --cov=. --cov-report=html
```

### Frontend Tests

```bash
cd frontend
npm run test:unit
npm run test:coverage
```

## API Documentation

The backend provides a RESTful API. See [backend/README.md](backend/README.md) for detailed API documentation.

## Development Workflow

This project follows an incremental development approach:

1. ✅ **Task 1**: Project structure and environment setup
2. **Task 2**: Database models and initialization
3. **Task 3**: Board API endpoints
4. **Task 4**: List API endpoints
5. **Task 5**: Card API endpoints
6. **Task 6**: Error handling and validation
7. **Task 7**: Flask application configuration
8. **Task 9-10**: Frontend state management and API services
9. **Task 11**: UI components
10. **Task 12-13**: UI enhancements and drag & drop
11. **Task 15**: Docker containerization
12. **Task 16**: Integration testing

## Contributing

1. Follow the task list in `.kiro/specs/visual-task-board/tasks.md`
2. Write tests for all new features
3. Use Black for Python code formatting
4. Use ESLint + Prettier for JavaScript code formatting
5. Ensure all tests pass before committing

## License

This project is for educational purposes.

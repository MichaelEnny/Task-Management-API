# Task Management API

A simple REST API for managing tasks and users.

## Features

- User authentication
- Task CRUD operations
- Task assignment to users
- Task status tracking

## Setup

```bash
pip install -r requirements.txt
python app.py
```

## API Endpoints

### Tasks
- `GET /api/tasks` - List all tasks
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/<id>` - Get task details
- `PUT /api/tasks/<id>` - Update a task
- `DELETE /api/tasks/<id>` - Delete a task

### Users
- `POST /api/users/register` - Register new user
- `POST /api/users/login` - User login

## Configuration

Set environment variables in `.env` file (see `.env.example`)

## Notes

- Authentication is required for most endpoints
- Tasks have priorities: low, medium, high
- Default page size is 20 items
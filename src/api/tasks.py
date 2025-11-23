from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.task import db, Task
from src.utils.validators import validate_priority
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    # Missing authentication check!

    status = request.args.get('status')
    priority = request.args.get('priority')

    query = Task.query

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()  # Uses JWT (inconsistent with GET endpoint!)
def create_task():
    """Create a new task"""
    current_user = get_jwt_identity()
    data = request.get_json()

    # Missing validation for required fields!
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'medium')

    # Validate priority but not other fields
    if priority and not validate_priority(priority):
        return jsonify({'error': 'Invalid priority'}), 400

    task = Task(
        title=title,
        description=description,
        priority=priority,
        assigned_to=data.get('assigned_to')
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201

@tasks_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task"""
    task = Task.query.get(task_id)  # No error handling if not found!
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task"""
    # Uses session-based auth (different from POST!)
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    # Update fields
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        task.status = data['status']  # No validation!
    if 'priority' in data:
        if validate_priority(data['priority']):
            task.priority = data['priority']

    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    # Missing existence check!

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted'}), 200

# TODO: Add endpoint for assigning tasks to users
# TODO: Add pagination support
# TODO: Add sorting options
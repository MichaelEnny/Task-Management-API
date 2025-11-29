from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.task import db, Task
from src.utils.validators import validate_priority
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['GET'])
def get_tasks():
    """Get all tasks with optional filtering"""
    # NOTE: No authentication check - is this intentional?
    # TODO: Add pagination support (limit/offset or cursor-based?)

    status = request.args.get('status')
    priority = request.args.get('priority')
    assigned_to = request.args.get('assigned_to')

    query = Task.query

    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if assigned_to:
        # FIXME: Should this be converted to int? What if it's not a number?
        query = query.filter_by(assigned_to=assigned_to)

    tasks = query.all()
    return jsonify([task.to_dict() for task in tasks]), 200

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task"""
    current_user = get_jwt_identity()
    data = request.get_json()

    # Missing validation for required fields
    title = data.get('title')
    description = data.get('description')
    priority = data.get('priority', 'medium')

    # Validate priority
    if priority and not validate_priority(priority):
        return jsonify({'error': 'Invalid priority'}), 400

    # TODO: Should we validate title is not empty?
    # TODO: Should assigned_to default to current_user?

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
    """Get a specific task by ID"""
    task = Task.query.get(task_id)
    # FIXME: No error handling if task not found
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    # NOTE: Uses session auth instead of JWT - inconsistent with create_task
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    # Update fields if provided
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'status' in data:
        # TODO: Should we validate status values?
        task.status = data['status']
    if 'priority' in data:
        if validate_priority(data['priority']):
            task.priority = data['priority']
        # NOTE: Silently ignores invalid priority - should we return error?

    db.session.commit()
    return jsonify(task.to_dict()), 200

@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a task"""
    task = Task.query.get(task_id)
    # Missing null check

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted'}), 200

# TODO: Add bulk operations endpoint (update/delete multiple tasks)
# TODO: Add endpoint to get tasks by user
# FIXME: Inconsistent auth - some endpoints use JWT, some use session, some have none
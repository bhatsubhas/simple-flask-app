from flask import Flask, url_for
from flask import jsonify, request
from flask import abort, make_response
from repositories import get_repo_list

app = Flask(__name__)

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/todo/api/v1.0/tasks", methods=['GET'])
def get_tasks():
    return jsonify({'tasks': [make_public_task(task) for task in tasks]})


@app.route("/todo/api/v1.0/task/<int:task_id>", methods=['GET'])
def get_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': f'No task found with id {task_id}'})
    return jsonify({'task': make_public_task(task[0])})


@app.route("/todo/api/v1.0/tasks", methods=['POST'])
def create_task():
    if not request.json or not 'title' in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': make_public_task(task)}), 201


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=['DELETE'])
def delete_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': f'No task found with id {task_id}'})
    tasks.remove(task[0])
    return jsonify({'result': True})


@app.route("/todo/api/v1.0/tasks/<int:task_id>", methods=['PUT'])
def update_task(task_id):
    task = [task for task in tasks if task['id'] == task_id]
    if len(task) == 0:
        return jsonify({'error': f'No task found with id {task_id}'})
    if not request.json:
        abort(400)
    if 'title' in request.json or 'description' in request.json:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get(
        'description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': make_public_task(task[0])})


def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for(
                'get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

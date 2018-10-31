from flask import request
from flask_restful import Resource
from todo.models import TodoList, Task
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required
from user.models import User

class TodoListsApi(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_id(get_jwt_identity())
        todo = TodoList.query.filter_by(user_id=user.userID).all()

        return {'todoLists': [t.to_dict() for t in todo] }, 201


class TodoListApi(Resource):

    @jwt_required
    def get(self, id):
        pass

    def post(self):
        data = request.get_json()

        task_lst = []
        for task in data['tasks']:
            obj = Task(
                task_name=task['task_name'],
                task_done=task['task_done']
                )
            task_lst.append(obj)

        todoList = TodoList(
            todoList_name=data['todoList_name'],
            todoList_done=data['todoList_done'],
        )
        todoList.tasks = task_lst

        todoList.save()

        return {'message': 'Successfully saved new data'}, 201

    def put(self, id):
        data = request.get_json()

        todoList = TodoList.get_by_id(id)

        if todoList is None:
            task_lst = []
            for task in data['tasks']:
                obj = Task(
                    task_name=task['task_name'],
                    task_done=task['task_done']
                    )
                task_lst.append(obj)

            todoList = TodoList(
                todoList_name=data['todoList_name'],
                todoList_done=data['todoList_done'],
            )
            todoList.tasks = task_lst

            todoList.save()

            return {'message': 'Successfully saved new data'}, 201
        else:
            todoList.todoList_name = data['todoList_name']
            todoList.todoList_done = data['todoList_done']
            for t in data['tasks']:
                task = Task.query.get(t['taskID'])
                task.task_name = t['task_name']
                task.task_done = t['task_done']


            todoList.save()
            return {'message': 'Updated data with '}

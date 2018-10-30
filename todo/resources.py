from flask import request
from flask_restful import Resource
from todo.models import TodoList, Task
from app import db


class TodoListsApi(Resource):
    def get(self):
        todo = TodoList.get_all()

        return {'todoLists': [t.to_dict() for t in todo] }, 201


class TodoListApi(Resource):
    def get(self, id):
        todoList = TodoList.get_by_id(id)

        return {'todoList': todoList.to_dict() }, 201

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

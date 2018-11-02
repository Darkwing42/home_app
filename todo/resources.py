from flask import request
from flask_restful import Resource
from todo.models import TodoList, Task
from app import db
from flask_jwt_extended import get_jwt_identity, jwt_required, fresh_jwt_required	
from user.models import User
from sqlalchemy import and_
from app.utils.uuid_converter import str2uuid

class TodoListsApi(Resource):
    @jwt_required
    def get(self):
        user = User.find_by_id(get_jwt_identity())
        todo = TodoList.query.filter_by(user_id=user.userID).all() #change to class method

        return {'todoLists': [t.to_dict() for t in todo] }, 201


class TodoListApi(Resource):

    @jwt_required
    def get(self, list_id):
        user = User.find_by_id(get_jwt_identity())
        todo = TodoList.query.filter(and_(TodoList.id == list_id, TodoList.user_id == user.userID)).first()

        if todo is None:
            return {'message': 'No Todolist found'}, 404
        
        return {'todoList': todo.to_dict() }, 201



        

    @fresh_jwt_required	
    def post(self):
        data = request.get_json()

        user = User.find_by_id(get_jwt_identity())


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
            user_id=user.userID
        )
        todoList.tasks = task_lst

        todoList.save()

        return {'message': 'Successfully saved new data'}, 201

    @fresh_jwt_required
    def put(self, list_id):
        data = request.get_json()

        user = User.find_by_id(get_jwt_identity())

        todoList = TodoList.query.filter(and_(TodoList.id == list_id, TodoList.user_id == user.userID)).first()

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
                user_id=user.userID
            )
            todoList.tasks = task_lst

            todoList.save()

            return {'message': 'Successfully saved new data'}, 201
        else:
            todoList.todoList_name = data['todoList_name']
            todoList.todoList_done = data['todoList_done']
            for t in data['tasks']:
                if t['id'] is "":
                    task = Task(
                        task_name=t['task_name'],
                        task_done=t['task_done']
                    )
                    todoList.tasks.append(task)
                else:
                    task = Task.get_by_id(t['id'])
                    task.task_name = t['task_name']
                    task.task_done = t['task_done']


            todoList.save()
            return {'message': 'Updated data'}

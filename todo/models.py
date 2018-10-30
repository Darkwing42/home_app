from app import db
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
import uuid
from app.utils.uuid_converter import str2uuid
from user.models import User


class Task(db.Model):

    __tablename__ = 'tasks'

    id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4().hex)
    taskID = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200))
    todoList_id = db.Column(db.Integer, db.ForeignKey('todoLists.todoListID'), nullable=False)
    task_done = db.Column(db.Boolean, default=False)

    def __init__(self, task_name, task_done):
        self.task_done = task_done
        self.task_name = task_name

    def to_dict(self):
        return dict(
            id=str(self.id),
            task_name=self.task_name,
            task_done=self.task_done
        )
    def save(self):
        db.session.add(self)
        db.session.commit()
		

    def delete(self):
        db.session.delete(self)
        db.session.commit()



class TodoList(db.Model):
    __tablename__ = 'todoLists'

    id = db.Column(UUID(as_uuid=True), default=lambda: uuid.uuid4())
    todoListID = db.Column(db.Integer, primary_key=True)
    todoList_name = db.Column(db.String(200))
    todoList_done = db.Column(db.Boolean, default=False)
    tasks = db.relationship('Task', backref='todoList', lazy=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.userID'))

    def __init__(self,todoList_name, todoList_done):
        self.todoList_name = todoList_name
        self.todoList_done = todoList_done

    def to_dict(self):
        return dict(
            id=str(self.id),
            
            todoList_name=self.todoList_name,
            todoList_done=self.todoList_done,
            tasks=[ task.to_dict() for task in self.tasks ]
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(todoListID=id).first()

	@classmethod
	def get_all_by_user(cls, user_id):
		user = User.find_by_id(user_id)
		return cls.query.filter_by(user_id=user.userID).all()
		

import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()

# ジャンル管理用テーブル
class Genre(db.Model):
    __tablename__ = 'genre'
    
    genre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    
    # リレーションシップ
    tasks = db.relationship('Task', backref='genre', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Genre {self.genre_id}: {self.name}>'


# タスク管理用テーブル
class Task(db.Model):
    __tablename__ = 'task'
    
    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.genre_id', onupdate='CASCADE', ondelete='SET NULL'))
    
    # リレーションシップ
    task_weekdays = db.relationship('TaskWeekday', backref='task', cascade='all, delete-orphan')
    task_logs = db.relationship('TaskLog', backref='task', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Task {self.task_id}: {self.title}>'


# タスクの曜日指定用テーブル
class TaskWeekday(db.Model):
    __tablename__ = 'task_weekday'
    
    task_weekday_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    weekday = db.Column(db.SmallInteger, nullable=False)
    
    __table_args__ = (
        db.CheckConstraint('weekday BETWEEN 0 AND 6'),
        db.UniqueConstraint('task_id', 'weekday'),
    )
    
    def __repr__(self):
        return f'<TaskWeekday {self.task_weekday_id}: task_id={self.task_id}, weekday={self.weekday}>'


# タスクの実行記録管理用テーブル
class TaskLog(db.Model):
    __tablename__ = 'task_log'
    
    task_id = db.Column(db.Integer, db.ForeignKey('task.task_id', onupdate='CASCADE', ondelete='CASCADE'), primary_key=True)
    date = db.Column(db.Date, primary_key=True, nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    completed_at = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<TaskLog task_id={self.task_id}, date={self.date}, is_completed={self.is_completed}>'
from flask import Flask, render_template, request, redirect, url_for
from app.models import db, Genre, Task, TaskWeekday, TaskLog
from dotenv import load_dotenv
from datetime import datetime, timedelta
import os
from uuid import UUID

# .envファイルを読み込む
load_dotenv()

# 環境変数からデータベース接続情報を取得
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')

app = Flask(__name__)

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# セッション設定
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

db.init_app(app)

@app.before_request
def create_tables():
    db.create_all()

# 今日の曜日を特定し今日のタスク一覧を表示、task_logと比較し未完了タスクを表示
@app.route('/')
def index():
    today_date = datetime.today().date()
    today_weekday = today_date.weekday()  
    
    # すべてのタスクを取得
    all_tasks = Task.query.all()
    
    # 今日の曜日に基づくタスクIDセットを作成
    assigned_today_task_ids = set()
    for task in all_tasks:
        for tw in task.task_weekdays:
            if tw.weekday == today_weekday:
                assigned_today_task_ids.add(task.task_id)
                break
    
    # タスクを割り当てられているものと割り当てられていないものに分ける
    assigned_tasks = [task for task in all_tasks if task.task_id in assigned_today_task_ids]
    unassigned_tasks = [task for task in all_tasks if task.task_id not in assigned_today_task_ids]
    
    # 割り当てられているものを上側に配置
    sorted_tasks = assigned_tasks + unassigned_tasks
    
    # 今日完了したタスクのIDを取得
    completed_task_ids = {log.task_id for log in TaskLog.query.filter_by(date=today_date).all()}
    
    return render_template('index.html', tasks=sorted_tasks, completed_task_ids=completed_task_ids, assigned_today_task_ids=assigned_today_task_ids)
#今日のタスク

# タスク完了ボタン
@app.route('/task/<int:task_id>/complete', methods=['POST'])
def complete_task(task_id):
    today_date = datetime.today().date()
    today_weekday = today_date.weekday()
    
    task = Task.query.get_or_404(task_id)
    
    # タスクが今日の曜日に割り当てられているか確認
    is_assigned_today = any(tw.weekday == today_weekday for tw in task.task_weekdays)
    
    if not is_assigned_today:
        # エラーログを表示するため、エラーメッセージをセッションに格納
        from flask import session
        session['error'] = f'エラー: タスク「{task.title}」は今日の曜日に割り当てられていません。'
        print(f'[ERROR] 未割り当てタスクの完了操作: task_id={task_id}, title={task.title}, today_weekday={today_weekday}')
        return redirect(url_for('index'))
    
    # 既に完了しているか確認
    existing_log = TaskLog.query.filter_by(task_id=task_id, date=today_date).first()
    if not existing_log:
        new_log = TaskLog(task_id=task_id, date=today_date, is_completed=True, completed_at=datetime.now())
        db.session.add(new_log)
        db.session.commit()
    
    return redirect(url_for('index'))


# タスク詳細を右側に表示 
@app.route('/task/<int:task_id>')
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    today_date = datetime.today().date()
    is_completed = TaskLog.query.filter_by(task_id=task_id, date=today_date).first() is not None
    genres = Genre.query.all()
    
    # 曜日リストをテンプレートに渡す
    task_weekdays = [tw.weekday for tw in task.task_weekdays]
    
    # 過去1ヶ月のログを取得
    thirty_days_ago = today_date - timedelta(days=30)
    logs = TaskLog.query.filter(
        TaskLog.task_id == task_id,
        TaskLog.date >= thirty_days_ago,
        TaskLog.date <= today_date
    ).all()
    
    # 達成率を計算
    completed_count = len(logs)
    total_days = 31  # 過去1ヶ月（31日間）
    completion_rate = (completed_count / total_days * 100) if total_days > 0 else 0
    
    # ログを日付でソート
    logs_by_date = {log.date: log for log in logs}
    
    return render_template(
        'view_memo.html',
        task=task,
        is_completed=is_completed,
        genres=genres,
        task_weekdays=task_weekdays,
        completion_rate=int(completion_rate),
        completed_count=completed_count,
        logs_by_date=logs_by_date,
        thirty_days_ago=thirty_days_ago,
        today_date=today_date,
        timedelta=timedelta
    )


# タスク編集ページ
@app.route('/task/<int:task_id>/edit', methods=['POST'])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    
    task.title = request.form.get('title')
    task.description = request.form.get('description')
    task.genre_id = int(request.form.get('genre_id')) if request.form.get('genre_id') else None
    
    # 曜日情報の更新
    weekdays = request.form.getlist('weekdays')
    
    # 既存の曜日情報を削除
    TaskWeekday.query.filter_by(task_id=task_id).delete()
    
    # 新しい曜日情報を追加
    for weekday in weekdays:
        task_weekday = TaskWeekday(task_id=task_id, weekday=int(weekday))
        db.session.add(task_weekday)
    
    db.session.commit()
    return redirect(url_for('index'))


# タスク作成ページ
@app.route('/task/create', methods=['GET', 'POST'])
def create_task():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        genre_id = request.form.get('genre_id')
        weekdays = request.form.getlist('weekdays')
        
        new_task = Task(
            title=title,
            description=description,
            genre_id=int(genre_id) if genre_id else None
        )
        db.session.add(new_task)
        db.session.flush()  # task_idを取得するためにflush
        
        # 曜日情報を追加
        for weekday in weekdays:
            task_weekday = TaskWeekday(task_id=new_task.task_id, weekday=int(weekday))
            db.session.add(task_weekday)
        
        db.session.commit()
        return redirect(url_for('index'))
    
    # GETリクエストの場合、テンプレートのみを返す
    genres = Genre.query.all()
    return render_template('create_memo.html', genres=genres)


# タスク削除
@app.route('/task/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# やることリスト Type-2

曜日ごとにタスクを管理できる、Webアプリケーションです。
<img width="1920" height="1032" alt="Image" src="https://github.com/user-attachments/assets/2f47517c-fab5-49f5-b276-6b3d24d854fa" />

## 概要

このアプリケーションは、日々のタスクを曜日単位で管理し、完了状況を記録・追跡できるタスク管理システムです。Docker Composeを使用して、Flask（Python）とPostgreSQLで構築されています。

## 主な機能

### タスク管理
- **タスク作成・編集・削除**: タイトル、説明、実行曜日、ジャンルを指定してタスクを管理
- **曜日別割り当て**: タスクごとに実行する曜日を複数選択可能（月〜日）
- **ジャンル分類**: タスクをカテゴリー（ジャンル）で分類
<img width="1338" height="909" alt="Image" src="https://github.com/user-attachments/assets/041e98ff-fe26-47ed-92d5-1a76eca80ae1" />


### 進捗管理
- **完了率表示**: 当日割り当てられたタスクの完了率をプログレスバーで可視化
- **完了記録**: タスク完了時に日付とタイムスタンプを記録
- **実行履歴**: 過去30日間のタスク実行履歴を確認
- **達成率統計**: タスクごとの過去1ヶ月の達成率を表示

### UI/UX
- **ダークテーマ**: サイドバーがダークモードで見やすいデザイン
- **リアルタイム更新**: 非同期読み込みによるスムーズなUI操作
- **視覚的フィードバック**: 
  - 完了タスクは暗く表示
  - 割り当てなしタスクも暗く表示
  - ホバー時のアニメーション効果

## 技術スタック

### バックエンド
- **Flask**: Python Webフレームワーク
- **SQLAlchemy**: ORM（Object-Relational Mapping）
- **PostgreSQL**: リレーショナルデータベース
- **python-dotenv**: 環境変数管理

### フロントエンド
- **HTML5/CSS3**: レスポンシブデザイン
- **Vanilla JavaScript**: 非同期通信とDOM操作
- **Jinja2**: テンプレートエンジン

### インフラ
- **Docker**: コンテナ化
- **Docker Compose**: マルチコンテナ管理

## データベース構造

### テーブル
1. **genre**: ジャンル管理
   - genre_id（主キー）
   - name（ジャンル名）

2. **task**: タスク管理
   - task_id（主キー）
   - title（タイトル）
   - description（説明）
   - genre_id（外部キー）

3. **task_weekday**: タスク曜日割り当て
   - task_weekday_id（主キー）
   - task_id（外部キー）
   - weekday（曜日: 0=月曜, 6=日曜）

4. **task_log**: タスク実行記録
   - task_id（複合主キー）
   - date（複合主キー）
   - is_completed（完了フラグ）
   - completed_at（完了日時）

## 使い方

### 1. タスクの作成
1. サイドバー下部の「新しいタスクを作成」ボタンをクリック
2. タスクのタイトル、説明、ジャンル、実行曜日を入力
3. 「作成」ボタンで保存

### 2. タスクの実行
1. 当日割り当てられたタスクが上部に表示されます
2. 「完了」ボタンをクリックしてタスクを完了
3. 完了したタスクは暗く表示され、「✓ 完了」と表示されます

### 3. タスクの詳細確認・編集
1. タスクカードの「詳細」ボタンをクリック
2. 右側にタスクの詳細情報が表示されます
3. 「編集」ボタンで内容を変更可能
4. 過去30日間の実行履歴と達成率を確認できます

### 4. タスクの削除
1. タスク詳細画面で「削除」ボタンをクリック
2. 確認後、タスクが削除されます

## プロジェクト構造

```
docker-flask-app-tx-v5.0/
├── app/
│   ├── __init__.py
│   ├── main.py              # アプリケーションエントリーポイント
│   ├── models.py            # データベースモデル
│   ├── requirements.txt     # Pythonパッケージ
│   ├── Dockerfile
│   ├── static/
│   │   └── css/
│   │       └── styles.css   # スタイルシート
│   └── templates/
│       ├── index.html       # メインページ
│       ├── create_memo.html # タスク作成フォーム
│       ├── create_task.html
│       └── view_memo.html   # タスク詳細ビュー
├── db/
│   ├── Dockerfile
│   └── init-sql/
│       ├── init-pgcrypto.sql
│       └── task_initialize.sql
├── compose.yml              # Docker Compose設定
├── .env                     # 環境変数（要作成）
└── readme.md               # このファイル
```

## API エンドポイント

### ページ表示
- `GET /` - メインページ（タスク一覧）
- `GET /task/<task_id>` - タスク詳細
- `GET /task/create` - タスク作成フォーム

### データ操作
- `POST /task/create` - タスク作成
- `POST /task/<task_id>/edit` - タスク編集
- `POST /task/<task_id>/complete` - タスク完了
- `POST /task/<task_id>/delete` - タスク削除


### データベースマイグレーション
アプリケーションは起動時に自動的にテーブルを作成します（`app.before_request`デコレータで`create_tables()`を実行）。

# これはプレゼン資料ではありません！（セットアップの解説です）

## セットアップ

### 必要な環境
- Docker
- Docker Compose

### インストール手順

1. **リポジトリのクローン**
```bash
git clone <repository-url>
cd docker-flask-app-tx-v5.0
```

2. **環境変数の設定**

`.env`ファイルをプロジェクトルートに作成：
```env
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=task_db
POSTGRES_HOST=db
DB_PORT=5432
API_PORT=5000
SECRET_KEY=your-secret-key-change-in-production
```

3. **Dockerコンテナの起動**
```bash
docker compose up -d
```

4. **アプリケーションへアクセス**
```
http://localhost:5000
```

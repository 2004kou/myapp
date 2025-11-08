
**最初に環境変数ファイル（.env）を作成します**
- Mac、Windows(PowerShell、Git Bash)の場合
```
cp .env.example .env
```
- Windows(コマンドプロンプト)の場合
```
copy .env.example .env
```
**chatappのディレクトリに移動し**
source venv/bin/activate

- Windows(コマンドプロンプト)の場合
venv\Scripts\activate

**hackathon-Gteamに移動し**

**起動方法**
```
docker compose up --build
```

**ブラウザで確認**
```
http://localhost:55000/login
```


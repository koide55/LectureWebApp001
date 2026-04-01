# 実装者向け詳細設計 改訂版

## 1. 目的

本設計は、Flask を用いた講義用 Web アプリの実装方針を定義する。対象は実装担当者であり、認証機能と各種脆弱性演習を段階的に追加できる構成を目指す。

## 2. 基本方針

- 最初は安全寄りの最小実装を提供する
- 脆弱性は設定フラグまたは専用ルートで段階的に有効化する
- 学生がコードを追いやすいよう責務を分離する
- Flask の標準機能を優先し、拡張は最小限に留める
- 安全版と脆弱版の差分が教材として見える構成にする

## 3. 対象機能

初期実装の対象は以下とする。

- ログイン
- ログアウト
- 認証済みページ
- Cookie 型認証
- サーバセッション型認証
- 認証方式の Web 切替
- CSRF 保護の Web 切替
- デバッグ表示
- ユーザ検索
- 掲示板
- プロフィール更新
- 反射型 XSS デモページ
- lab-settings 画面

将来追加対象は以下とする。

- SQLインジェクション
- 蓄積型XSS
- 反射型XSS
- CSRF
- セッション固定
- Cookie 設定不備
- 認可不備
- コマンドインジェクション

## 4. 想定構成

```text
vuln-webapp/
  app/
    __init__.py
    routes.py
    config.py
    models.py
    auth/
      __init__.py
      interfaces.py
      cookie_auth.py
      server_session_auth.py
      helpers.py
      decorators.py
    services/
      __init__.py
      user_service.py
      auth_service.py
      board_service.py
      lab_service.py
      command_service.py
      server_session_store.py
    db/
      schema.sql
      seed.py
    templates/
      base.html
      index.html
      login.html
      me.html
      profile.html
      users.html
      board.html
      reflect.html
      lab_settings.html
      debug_session.html
      admin.html
      ping.html
    static/
      style.css
  instance/
    app.sqlite3
  run.py
  csrf_demo_server.py
  README.md
  IMPLEMENTER_DESIGN.md
```

## 5. 主要コンポーネント

### 5.1 `config.py`

環境変数または設定クラスで以下を管理する。

- `DEFAULT_AUTH_MODE`
- `SECRET_KEY`
- `DATABASE_PATH`
- `SESSION_COOKIE_NAME`
- `SESSION_COOKIE_HTTPONLY`
- `SESSION_COOKIE_SECURE`
- `SESSION_COOKIE_SAMESITE`
- `SERVER_SESSION_COOKIE_NAME`
- `AUTH_MODE_COOKIE_NAME`
- `STORED_XSS_MODE_COOKIE_NAME`
- `CSRF_MODE_COOKIE_NAME`
- `REFLECTED_XSS_MODE_COOKIE_NAME`
- `SQLI_MODE_COOKIE_NAME`
- `COMMAND_INJECTION_MODE_COOKIE_NAME`
- `ENABLE_DEBUG_ROUTES`
- `DEFAULT_VULN_SQLI`
- `DEFAULT_VULN_STORED_XSS`
- `DEFAULT_CSRF_PROTECTION`
- `DEFAULT_VULN_REFLECTED_XSS`
- `DEFAULT_VULN_COMMAND_INJECTION`
- 将来追加:
  - `ENABLE_VULN_SESSION_FIXATION`
  - `ENABLE_VULN_COMMAND_INJECTION`
  - `ENABLE_VULN_BROKEN_AUTHZ`

### 5.2 `models.py`

最低限のユーザモデルを定義する。

- `User`
  - `id`
  - `username`
  - `password`
  - `role`
  - `display_name`
  - `bio`

### 5.3 `services/user_service.py`

責務:

- ユーザ取得
- ユーザ認証
- 安全なユーザ検索
- 脆弱なユーザ検索
- プロフィール更新

主な関数:

- `get_user_by_username(username)`
- `get_user_by_id(user_id)`
- `verify_user(username, password)`
- `search_users_safe(keyword)`
- `search_users_unsafe(keyword)`
- `update_profile(user_id, display_name, bio)`

設計方針:

- `search_users_safe` はプレースホルダを使う
- `search_users_unsafe` は文字列連結で SQL を生成し、SQLインジェクション演習に使う
- 脆弱版は通常の認証処理とは分離し、`/users` の独立ルートで扱う
- プロフィール更新は CSRF の被害例として使えるようにする

### 5.4 `auth/interfaces.py`

認証方式の共通インターフェースを定義する。

- `login(user)`
- `logout()`
- `get_current_user()`

### 5.5 `auth/cookie_auth.py`

Cookie 型認証を担当する。

責務:

- Flask 標準の署名付き Cookie ベース `session` に `user_id` を保存する
- Cookie からユーザ識別情報を復元する
- ログアウト時に Cookie 上の状態を削除する

教材上の意味:

- 認証状態がクライアント側 Cookie に載る構造を観察しやすい

### 5.6 `auth/server_session_auth.py`

サーバセッション型認証を担当する。

責務:

- ログイン時にランダムな `session_id` を発行する
- `server_sessions` テーブルに `session_id` と `user_id` を保存する
- クライアント側には `server_session_id` Cookie のみを持たせる
- ログアウト時にサーバ側セッションを破棄する

教材上の意味:

- クライアント側には識別子だけが保存される構造を比較できる

### 5.7 `auth/helpers.py`

認証方式、CSRF、蓄積型 XSS の状態管理を集約する。

主な関数:

- `get_auth_mode()`
- `get_auth_backend()`
- `login_user(user)`
- `logout_user()`
- `current_user()`
- `get_stored_xss_mode()`
- `stored_xss_enabled()`
- `get_csrf_mode()`
- `csrf_protection_enabled()`
- `get_csrf_token()`
- `csrf_token_is_valid(submitted_token)`

設計方針:

- 既定値は環境変数で与える
- 実際のモードは Cookie でブラウザごとに保持する
- 認証方式変更時は強制ログアウトする

### 5.8 `auth/decorators.py`

アクセス制御と CSRF 検証を担当する。

- `login_required`
- `role_required(role_name)`
- `csrf_protect`

### 5.9 `services/auth_service.py`

ログイン処理全体をまとめる。

責務:

- 入力検証
- ユーザ認証
- 認証バックエンドへの委譲

### 5.10 `services/board_service.py`

掲示板機能を担当する。

- `list_posts()`
- `create_post(author_username, title, body)`

設計方針:

- 投稿本文は DB にそのまま保存する
- 通常は Jinja2 の自動エスケープで安全に表示する
- 演習時のみ `DEFAULT_VULN_STORED_XSS` と Cookie により unsafe 表示へ切り替える

### 5.11 `services/lab_service.py`

演習用モードの状態判定を担当する。

- `get_sqli_mode()`
- `sqli_enabled()`
- `get_command_injection_mode()`
- `command_injection_enabled()`
- `get_reflected_xss_mode()`
- `reflected_xss_enabled()`

### 5.12 `services/command_service.py`

コマンドインジェクション演習用機能を分離する。

主な関数:

- `safe_ping(host)`
- 将来追加: `unsafe_ping(raw_input)`

### 5.13 `services/server_session_store.py`

サーバセッション保存を担当する。

- `create_server_session(user_id)`
- `get_server_session(session_id)`
- `delete_server_session(session_id)`

保存先は SQLite の `server_sessions` テーブルとする。

## 6. データベース設計

### 6.1 `users` テーブル

```sql
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL UNIQUE,
  password TEXT NOT NULL,
  role TEXT NOT NULL,
  display_name TEXT NOT NULL DEFAULT '',
  bio TEXT NOT NULL DEFAULT ''
);
```

### 6.2 `server_sessions` テーブル

```sql
CREATE TABLE server_sessions (
  session_id TEXT PRIMARY KEY,
  user_id INTEGER NOT NULL,
  created_at TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
```

### 6.3 `posts` テーブル

```sql
CREATE TABLE posts (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_username TEXT NOT NULL,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  created_at TEXT NOT NULL
);
```

### 6.4 初期ユーザ

- `alice / alicepass / user / Alice / I like web security labs.`
- `bob / bobpass / user / Bob / I enjoy breaking sample apps.`
- `admin / adminpass / admin / Admin / I manage the classroom environment.`

## 7. ルーティング詳細

- `GET /`
  - トップページ
- `GET,POST /login`
  - ログイン画面と認証処理
- `POST /logout`
  - ログアウト処理
- `POST /switch-auth`
  - 認証方式切替
- `POST /switch-csrf`
  - CSRF 保護切替
- `POST /switch-sqli`
  - SQLインジェクション切替
- `POST /switch-command-injection`
  - コマンドインジェクション切替
- `POST /switch-stored-xss`
  - 蓄積型 XSS 表示切替
- `POST /switch-reflected-xss`
  - 反射型 XSS 表示切替
- `GET /me`
  - 認証済みユーザページ
- `GET,POST /profile`
  - プロフィール更新
- `GET /debug/session`
  - Cookie / Session / 認証結果表示
- `GET,POST /users`
  - ユーザ検索
  - SQLインジェクション演習の比較対象
- `GET,POST /board`
  - 掲示板
  - 蓄積型 XSS 演習の比較対象
- `GET /reflect`
  - 反射型 XSS 演習用
- `GET /lab-settings`
  - 演習設定の集中管理画面
- `GET,POST /ping`
  - コマンドインジェクション演習の比較対象
- `GET /admin`
  - 認可演習用ページ

## 8. 画面仕様

### 8.1 共通ヘッダ

- 現在の各モード表示
- ナビゲーション
- ログイン中ユーザ表示
- lab-settings への導線

### 8.2 ログイン画面

- ユーザ名
- パスワード
- 既定アカウント表示

### 8.3 認証済み画面

- `id`
- `username`
- `display_name`
- `role`
- `bio`
- ログアウトボタン

### 8.4 プロフィール画面

- 表示名編集
- 自己紹介編集
- 現在のプロフィール表示

### 8.5 デバッグ画面

- 受信 Cookie 一覧
- Flask `session` 内容
- 現在解決されたユーザ
- 既定認証方式
- 既定 CSRF モード
- 既定 XSS モード

### 8.6 ユーザ検索画面

- 検索キーワード入力
- 結果一覧
- 脆弱版有効時は生成された SQL 文の表示

### 8.7 掲示板画面

- 投稿タイトル入力
- 投稿本文入力
- 投稿一覧表示
- 表示モード切替フォーム
- 脆弱版有効時は本文を unsafe に描画

### 8.8 反射型 XSS 画面

- メッセージ入力
- 反映結果表示
- safe / vulnerable の比較対象

### 8.9 lab-settings 画面

- 認証方式切替
- CSRF 保護切替
- SQLインジェクション切替
- コマンドインジェクション切替
- 蓄積型 XSS 切替
- 反射型 XSS 切替
- 現在の演習状態の一覧表示

### 8.10 `ping` 画面

- safe / vulnerable 表示モード表示
- ホスト名入力
- 脆弱版有効時は実行コマンド文字列表示
- 実行結果表示

## 9. 認証処理詳細

### 9.1 ログイン処理

1. `username`, `password` を受け取る
2. 必須入力チェック
3. `verify_user()` で照合
4. 現在の認証方式に対応する backend でログイン状態を作る
5. 必要に応じて Cookie を発行する
6. `/me` へリダイレクトする

### 9.2 ログアウト処理

1. 現在の認証方式を判定する
2. Cookie 型なら Flask `session` をクリアする
3. サーバセッション型なら DB 上の `server_sessions` を削除する
4. 必要に応じて Cookie を削除する
5. `/login` へリダイレクトする

### 9.3 認証方式切替

1. フォームから `auth_mode` を受信する
2. `cookie` または `server_session` のみ受け付ける
3. 現在ログイン中なら強制ログアウトする
4. 新しい `auth_mode` を Cookie に保存する
5. 元の画面またはトップページへ戻す

## 10. SQLインジェクション演習設計

### 10.1 目的

- SQL 文を文字列連結で組み立てる危険性を理解する
- プレースホルダを使った対策を理解する
- 認証処理とは別のルートで安全に教材化する

### 10.2 安全版

- ルート: `/users`
- 既定値: `DEFAULT_VULN_SQLI=false`
- 実装: `search_users_safe(keyword)`

### 10.3 脆弱版

- ルート: `/users`
- 既定値: `DEFAULT_VULN_SQLI=true`
- 実装: `search_users_unsafe(keyword)`
- 特徴:
  - SQL 文へ入力値を直接連結する
  - 生成した SQL 文を画面に表示する

### 10.4 切替方法

- 実際の表示モードは `/lab-settings` から切り替える
- 状態は Cookie に保存する
- 環境変数は初期値としてのみ扱う

## 11. 蓄積型XSS演習設計

### 11.1 目的

- 保存された入力が別ユーザ閲覧時に実行される危険性を理解する
- エスケープの重要性を理解する

### 11.2 安全版

- ルート: `/board`
- 既定値: `DEFAULT_VULN_STORED_XSS=false`
- 実装:
  - DB には入力をそのまま保存する
  - 表示時は Jinja2 の自動エスケープを使う

### 11.3 脆弱版

- ルート: `/board`
- 既定値: `DEFAULT_VULN_STORED_XSS=true`
- 実装:
  - 保存済み本文を `|safe` で描画する

### 11.4 切替方法

- 実際の表示モードは `/lab-settings` から切り替える
- 状態は Cookie に保存する
- 環境変数は初期値としてのみ扱う

## 12. 反射型XSS演習設計

### 12.1 目的

- 反射された入力がその場で実行される危険性を理解する
- 蓄積型 XSS との違いを比較する

### 12.2 安全版

- ルート: `/reflect`
- 既定値: `DEFAULT_VULN_REFLECTED_XSS=false`
- 実装:
  - クエリ文字列の `message` を通常描画する

### 12.3 脆弱版

- ルート: `/reflect`
- 既定値: `DEFAULT_VULN_REFLECTED_XSS=true`
- 実装:
  - `message` を `|safe` で描画する

### 12.4 切替方法

- 実際の表示モードは `/lab-settings` から切り替える
- 状態は Cookie に保存する

## 13. CSRF演習設計

### 13.1 保護対象

- `/logout`
- `/users`
- `/board`
- `/profile`
- `/ping`
- 各種切替フォーム

### 13.2 安全版

- hidden フィールドに CSRF トークンを埋め込む
- `csrf_protect` で POST 時に検証する

### 13.3 脆弱版

- ブラウザ上の CSRF 保護モードを `disabled` に切り替える

### 13.4 デモ環境

- 攻撃側サーバは `csrf_demo_server.py` を使う
- `localhost` と `127.0.0.1` の違いを使うと SameSite の説明に向く

## 14. 将来追加する脆弱性演習ポイント

### 14.1 セッション固定

- ログイン時にセッション再生成をしない設定を追加

### 14.2 Cookie 設定不備

- `HttpOnly`, `Secure`, `SameSite` を設定で緩める

### 14.3 認可不備

- `/admin` のチェックを外す設定を追加

### 14.4 コマンドインジェクション

- `/ping` に `unsafe_ping()` を追加
- 安全版は `subprocess.run([...], shell=False)`
- 脆弱版は文字列連結と `shell=True`
- 実際の表示モードは `/lab-settings` から切り替える
- 状態は Cookie に保存する

## 15. テスト観点

最低限の確認項目:

- 正しい認証情報でログインできる
- 誤った認証情報では失敗する
- 未認証では `/me` に入れない
- 認証方式を切り替えるとログアウトされる
- Cookie 型認証で状態が維持される
- サーバセッション型認証で状態が維持される
- `/users` の安全版検索が動作する
- `/board` で投稿と表示ができる
- `/profile` で表示名と自己紹介を更新できる
- `/reflect` で safe / vulnerable の差を確認できる
- `/admin` の認可が動作する
- `/ping` の安全版が動作する
- CSRF 保護有効時にトークンなし POST が 403 になる

脆弱性演習用確認:

- `/lab-settings` 上の切替で SQLi safe / vulnerable が切り替わる
- `/lab-settings` 上の切替で command injection safe / vulnerable が切り替わる
- `/lab-settings` 上の切替で stored XSS safe / vulnerable が切り替わる
- `/lab-settings` 上の切替で CSRF 保護 enabled / disabled が切り替わる
- `/lab-settings` 上の切替で reflected XSS safe / vulnerable が切り替わる

## 16. 実装順序

1. Flask アプリ骨組み
2. SQLite と初期データ
3. `/login`, `/logout`, `/me`
4. Cookie 型認証
5. サーバセッション型認証
6. 認証方式切替 UI
7. `/debug/session`
8. `/users`
9. `/board`
10. `/profile`
11. `/reflect`
12. `/lab-settings`
13. `/admin`
14. `/ping`
15. 各脆弱性フラグの導入

## 17. 非推奨事項

- 初期段階から認証ライブラリを入れすぎること
- 脆弱版コードを通常版と見分けにくく混在させること
- 本番運用向けの複雑な抽象化を先に入れること
- 演習環境以外で脆弱フラグを有効にすること

## 18. 実装メモ

- まずは読めることを優先する
- 学生が差分を確認しやすいよう、各脆弱性は関数やフラグ単位で分離する
- デバッグ画面は講義中のみ有効化する想定とする
- 外部公開はしない

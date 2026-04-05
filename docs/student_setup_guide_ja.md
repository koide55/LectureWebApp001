# Webアプリケーション脆弱性演習
## 学生向け統合セットアップ資料

この資料は、授業で使う開発環境と演習環境を準備するための統合ガイドです。  
Windows と macOS の両方に対応しています。

授業では、教材を以下の GitHub repository から取得します。

- Repository:
  - [https://github.com/koide55/LectureWebApp001](https://github.com/koide55/LectureWebApp001)

---

## 1. この資料に含まれる内容

この資料は、次の4つを1つにまとめたものです。

- Windows 向け環境構築手順
- macOS 向け環境構築手順
- 授業前チェックリスト
- 学生配布用の簡潔なセットアップ手順

---

## 2. 授業で使うツール

### 必須

- `Git`
  - ソースコード取得用
- `Python 3`
  - Webアプリ実行用
- `Visual Studio Code`
  - エディタ
- `Google Chrome`
  - ブラウザ

### 推奨

- `DB Browser for SQLite`
  - SQLite ファイルを GUI で確認するため
- `Burp Suite Community Edition`
  - HTTP リクエスト観察用

### 公式配布元

- Git:
  - [https://git-scm.com/downloads](https://git-scm.com/downloads)
- Python 3:
  - [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Visual Studio Code:
  - [https://code.visualstudio.com/Download](https://code.visualstudio.com/Download)
- Google Chrome:
  - [https://www.google.com/chrome/](https://www.google.com/chrome/)
- DB Browser for SQLite:
  - [https://sqlitebrowser.org/](https://sqlitebrowser.org/)
- Burp Suite Community Edition:
  - [https://portswigger.net/burp/communitydownload](https://portswigger.net/burp/communitydownload)

---

## 3. 推奨する最小構成

授業開始時点では、まず以下の4つが入っていれば十分です。

- Git
- Python 3
- Visual Studio Code
- Google Chrome

最初から DB Browser や Burp を入れなくても進められます。  
必要になる回が近づいたら追加します。

---

## 4. Windows 向けセットアップ手順

### 4.1 Git を入れる

1. [Git の公式サイト](https://git-scm.com/downloads)を開く
2. Windows 版をダウンロードする
3. インストーラを実行する
4. 基本的には既定値のままで進めてよい

確認:

```powershell
git --version
```

---

### 4.2 Python 3 を入れる

1. [Python 公式サイト](https://www.python.org/downloads/)を開く
2. Windows 用の最新版 Python 3 をダウンロードする
3. インストーラを実行する
4. 可能なら `Add Python to PATH` を有効にする

確認:

```powershell
python --version
```

または

```powershell
python3 --version
```

---

### 4.3 Visual Studio Code を入れる

1. [VS Code 公式サイト](https://code.visualstudio.com/Download)を開く
2. Windows 版をダウンロードする
3. インストーラを実行する

起動確認:

- VS Code を開けること

推奨拡張:

- `Python`

---

### 4.4 Google Chrome を入れる

1. [Chrome 公式サイト](https://www.google.com/chrome/)を開く
2. ダウンロードしてインストールする

起動確認:

- Chrome が開けること

---

## 5. macOS 向けセットアップ手順

### 5.1 Git を確認する

macOS には Git がすでに入っている場合があります。  
まず確認します。

```bash
git --version
```

入っていない場合:

1. コマンド実行時に案内が出たらインストールを進める
2. または [Git 公式サイト](https://git-scm.com/downloads) から導入する

---

### 5.2 Python 3 を入れる

1. [Python 公式サイト](https://www.python.org/downloads/)を開く
2. macOS 用の Python 3 をダウンロードする
3. インストーラを実行する

確認:

```bash
python3 --version
```

---

### 5.3 Visual Studio Code を入れる

1. [VS Code 公式サイト](https://code.visualstudio.com/Download)を開く
2. macOS 版をダウンロードする
3. アプリケーションフォルダへ移動する

起動確認:

- VS Code を開けること

推奨拡張:

- `Python`

---

### 5.4 Google Chrome を入れる

1. [Chrome 公式サイト](https://www.google.com/chrome/)を開く
2. macOS 版をダウンロードしてインストールする

起動確認:

- Chrome が開けること

---

## 6. 教材の取得

以下の repository を clone します。

- [https://github.com/koide55/LectureWebApp001](https://github.com/koide55/LectureWebApp001)

### Windows PowerShell

```powershell
git clone https://github.com/koide55/LectureWebApp001.git
cd LectureWebApp001
```

### macOS Terminal

```bash
git clone https://github.com/koide55/LectureWebApp001.git
cd LectureWebApp001
```

---

## 7. 初回起動手順

### Windows PowerShell

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m app.db.seed
python run.py
```

### macOS Terminal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -m app.db.seed
python3 run.py
```

ブラウザで開く:

- [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 8. ログイン確認

初期ユーザ:

- `alice / alicepass`
- `bob / bobpass`
- `admin / adminpass`

最初は `alice / alicepass` でログインしてください。

---

## 9. 授業前チェックリスト

以下をすべて確認してください。

- Git が使える
- Python 3 が使える
- VS Code が起動する
- Chrome が起動する
- repository を clone できる
- `pip install -r requirements.txt` が通る
- `python -m app.db.seed` または `python3 -m app.db.seed` が通る
- `python run.py` または `python3 run.py` でアプリが起動する
- Chrome で `http://127.0.0.1:5000` を開ける
- `alice / alicepass` でログインできる

---

## 10. 動作確認コマンド

### Windows

```powershell
git --version
python --version
code --version
```

### macOS

```bash
git --version
python3 --version
code --version
```

`code --version` が通らない場合は、VS Code のコマンドライン起動設定が未設定でも大丈夫です。  
その場合は VS Code を普通に起動してください。

---

## 11. よくあるトラブル

### `git` が見つからない

- Git が未インストールの可能性があります
- 再起動後に使えるようになることがあります

### `python` または `python3` が見つからない

- Python 3 が未インストールの可能性があります
- Windows では PATH 設定が反映されていないことがあります

### `pip install -r requirements.txt` が失敗する

- ネットワーク接続を確認してください
- まず仮想環境が有効になっているか確認してください

### `python run.py` で起動しない

- 先に `python -m app.db.seed` または `python3 -m app.db.seed` を実行してください
- エラーメッセージをそのまま控えてください

---

## 12. 授業でのおすすめ運用

- ブラウザは Chrome に統一する
- コード閲覧は VS Code に統一する
- 初回は Burp Suite なしで進める
- DB Browser for SQLite は必要になった時点で追加する

---

## 13. 授業開始前に先生へ伝えるべきこと

以下に当てはまる場合は、授業開始前に相談してください。

- 自分のPCにソフトウェアを入れられない
- Git や Python のインストール権限がない
- PowerShell や Terminal の操作に不安がある
- 途中でエラーが出て解決できない

---

## 14. 最短版

急いでいる場合は、最低限これだけ行ってください。

1. Git を入れる
2. Python 3 を入れる
3. VS Code を入れる
4. Chrome を入れる
5. repository を clone する
6. 仮想環境を作る
7. `pip install -r requirements.txt`
8. `python -m app.db.seed` または `python3 -m app.db.seed`
9. `python run.py` または `python3 run.py`
10. Chrome で開いてログインする

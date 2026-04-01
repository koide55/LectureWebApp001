# Web Application Vulnerability Lab
## Unified Student Setup Guide

This document is a unified guide for preparing the development and lab environment used in class.  
It supports both Windows and macOS.

The course material is distributed through the following GitHub repository.

- Repository:
  - [https://github.com/koide55/LectureWebApp001](https://github.com/koide55/LectureWebApp001)

---

## 1. What This Guide Includes

This document combines the following four materials into one.

- Windows setup instructions
- macOS setup instructions
- Pre-class checklist
- A short student handout version of the setup procedure

---

## 2. Tools Used in This Course

### Required

- `Git`
  - For obtaining the source code
- `Python 3`
  - For running the web application
- `Visual Studio Code`
  - As the editor
- `Google Chrome`
  - As the browser

### Recommended

- `DB Browser for SQLite`
  - To inspect SQLite files with a GUI
- `Burp Suite Community Edition`
  - For observing HTTP requests

### Official Download Sources

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

## 3. Recommended Minimum Setup

At the beginning of the course, the following four tools are enough.

- Git
- Python 3
- Visual Studio Code
- Google Chrome

Students do not need DB Browser or Burp Suite on day one.  
Those can be added later when needed.

---

## 4. Windows Setup Instructions

### 4.1 Install Git

1. Open [the official Git website](https://git-scm.com/downloads)
2. Download the Windows version
3. Run the installer
4. The default options are usually fine

Check:

```powershell
git --version
```

---

### 4.2 Install Python 3

1. Open [the official Python website](https://www.python.org/downloads/)
2. Download the latest Windows version of Python 3
3. Run the installer
4. If possible, enable `Add Python to PATH`

Check:

```powershell
python --version
```

or

```powershell
python3 --version
```

---

### 4.3 Install Visual Studio Code

1. Open [the official VS Code website](https://code.visualstudio.com/Download)
2. Download the Windows version
3. Run the installer

Check:

- VS Code should open successfully

Recommended extension:

- `Python`

---

### 4.4 Install Google Chrome

1. Open [the official Chrome website](https://www.google.com/chrome/)
2. Download and install Chrome

Check:

- Chrome should open successfully

---

## 5. macOS Setup Instructions

### 5.1 Check Git

Git may already be installed on macOS.  
Check it first.

```bash
git --version
```

If Git is not available:

1. Follow the installation prompt shown by macOS
2. Or install it from [the official Git website](https://git-scm.com/downloads)

---

### 5.2 Install Python 3

1. Open [the official Python website](https://www.python.org/downloads/)
2. Download the macOS version of Python 3
3. Run the installer

Check:

```bash
python3 --version
```

---

### 5.3 Install Visual Studio Code

1. Open [the official VS Code website](https://code.visualstudio.com/Download)
2. Download the macOS version
3. Move the app into the Applications folder

Check:

- VS Code should open successfully

Recommended extension:

- `Python`

---

### 5.4 Install Google Chrome

1. Open [the official Chrome website](https://www.google.com/chrome/)
2. Download and install the macOS version

Check:

- Chrome should open successfully

---

## 6. Get the Course Material

Clone the following repository.

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

## 7. First Run Procedure

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

Open in the browser:

- [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 8. Login Check

Default users:

- `alice / alicepass`
- `bob / bobpass`
- `admin / adminpass`

Use `alice / alicepass` first.

---

## 9. Pre-Class Checklist

Please make sure all of the following work.

- Git is available
- Python 3 is available
- VS Code opens successfully
- Chrome opens successfully
- The repository can be cloned
- `pip install -r requirements.txt` completes
- `python -m app.db.seed` or `python3 -m app.db.seed` completes
- `python run.py` or `python3 run.py` starts the app
- Chrome can open `http://127.0.0.1:5000`
- You can log in with `alice / alicepass`

---

## 10. Verification Commands

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

If `code --version` does not work, that is still okay.  
In that case, simply start VS Code normally.

---

## 11. Common Problems

### `git` is not found

- Git may not be installed yet
- A system restart may be required after installation

### `python` or `python3` is not found

- Python 3 may not be installed yet
- On Windows, the PATH setting may not have been applied

### `pip install -r requirements.txt` fails

- Check your network connection
- Make sure the virtual environment is activated first

### `python run.py` does not start

- Run `python -m app.db.seed` or `python3 -m app.db.seed` first
- Save the full error message

---

## 12. Recommended Course Workflow

- Standardize on Chrome as the browser
- Standardize on VS Code for reading and editing code
- Do not require Burp Suite in the first class
- Add DB Browser for SQLite only when it becomes useful

---

## 13. When You Should Contact the Instructor Before Class

Please ask for help before class if any of the following apply.

- You are not allowed to install software on your computer
- You do not have permission to install Git or Python
- You are not comfortable using PowerShell or Terminal
- You encounter an error and cannot resolve it

---

## 14. Short Version

If you are in a hurry, do at least the following.

1. Install Git
2. Install Python 3
3. Install VS Code
4. Install Chrome
5. Clone the repository
6. Create a virtual environment
7. Run `pip install -r requirements.txt`
8. Run `python -m app.db.seed` or `python3 -m app.db.seed`
9. Run `python run.py` or `python3 run.py`
10. Open the app in Chrome and log in

# Student Performance Analysis System

A beginner-friendly Python + Streamlit + MySQL project for managing student records, marks, and academic performance reports.

## Features
- Student and subject management
- Add, edit, and delete assessment marks
- MySQL persistence
- Student totals, averages, percentage, grades, and pass/fail result
- Topper and low-performer reports
- Subject-wise and section-wise summaries
- Matplotlib charts and CSV report download
- Input validation for marks

## Grade rules
- A+: 90–100%
- A: 80–89.99%
- B: 70–79.99%
- C: 60–69.99%
- D: 50–59.99%
- E: 40–49.99%
- F: below 40%

The student report aggregates all saved assessment rows for each student. The percentage is total marks obtained divided by the sum of the maximum marks for those saved rows. Pass/fail in the student summary uses an overall 40% threshold. Subject pass percentages use each subject's configured pass marks.

## Requirements
- Python 3.10 or newer
- MySQL Server 8.x
- Git (for GitHub upload)

## Setup on Windows PowerShell

### 1. Open the project folder
```powershell
cd path\to\Student-Performance-Analysis-System
```

### 2. Create and activate a virtual environment
```powershell
py -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

### 3. Install packages
```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Create the MySQL database
Open MySQL Workbench, connect to your local MySQL server, open `database/schema.sql`, and execute the whole file.

Optional: execute `database/sample_data.sql` to add demonstration students, subjects, and marks.

### 5. Configure database credentials
Copy `.env.example` to `.env` in the project root:
```powershell
Copy-Item .env.example .env
notepad .env
```
Enter your own MySQL username and password. Do not upload `.env` to GitHub.

Example:
```text
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_actual_password
DB_NAME=student_performance
```

### 6. Run the application
```powershell
python -m streamlit run app.py
```
Open the Local URL shown in the terminal, usually `http://localhost:8501`.

To stop the app, press `Ctrl + C` in PowerShell.

## Run tests
```powershell
python -m unittest discover -s tests -v
```

## Upload to GitHub
Create a new empty repository on GitHub named `Student-Performance-Analysis-System`. Do not initialize it with a README, license, or gitignore.

Then run these commands in PowerShell from the project root:
```powershell
git init
git add .
git commit -m "Initial commit - Student Performance Analysis System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Student-Performance-Analysis-System.git
git push -u origin main
```
Replace `YOUR-USERNAME` with your GitHub username. If `origin` already exists, use:
```powershell
git remote set-url origin https://github.com/YOUR-USERNAME/Student-Performance-Analysis-System.git
```

After pushing, open the repository page on GitHub to see your files.

## Important
Use sample or institution-approved data only. Keep student personal information private. Never commit `.env`, passwords, or real student records to a public repository.

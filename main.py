from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            naam TEXT,
            grondtype TEXT,
            pandtype TEXT,
            locatie TEXT,
            budget REAL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS kosten (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            categorie TEXT,
            bedrag REAL,
            FOREIGN KEY(project_id) REFERENCES projects(id)
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM projects")
    projecten = c.fetchall()
    conn.close()
    return render_template('dashboard.html', projecten=projecten)

@app.route('/project-toevoegen', methods=['POST'])
def project_toevoegen():
    naam = request.form['naam']
    grondtype = request.form['grondtype']
    pandtype = request.form['pandtype']
    locatie = request.form['locatie']
    budget = request.form['budget']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO projects (naam, grondtype, pandtype, locatie, budget) VALUES (?, ?, ?, ?, ?)",
              (naam, grondtype, pandtype, locatie, budget))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
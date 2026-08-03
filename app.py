import sqlite3
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/author")
def author():
    return render_template("author.html")

@app.route("/planner")
def planner():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, description, created_at FROM tasks ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    tasks_list = []
    for row in rows:
        tasks_list.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "created_at": row[3]
        })
        
    return render_template("planner.html", tasks=tasks_list)

@app.route("/add_task", methods=["POST"])
def add_task():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    
    if title:
        import datetime
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, created_at) VALUES (?, ?, ?)",
            (title, description, now)
        )
        conn.commit()
        conn.close()
        
    return redirect(url_for("planner"))

@app.route("/delete/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    return redirect(url_for("planner"))

if __name__ == "__main__":
    init_db()
    app.run(port=8080)

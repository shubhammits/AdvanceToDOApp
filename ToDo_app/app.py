from flask import Flask, render_template, request, redirect, url_for
import pyodbc

app = Flask(__name__)

def get_db_connection():
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};'
                          'SERVER=MUSKAN_SWARNKAR\\SQLEXPRESS;'
                          'DATABASE=ToDoApp;'
                          'Trusted_Connection=yes;')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks')
    tasks = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add_todo', methods=['POST'])
def add_todo():
    task = request.form['task']
    
    # Priority mapping from string to integer
    priority_map = {'low': 1, 'medium': 2, 'high': 3}
    priority = priority_map[request.form['priority']]  # Map priority to integer
    
    due_date = request.form.get('due_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (task, completed, priority, due_date) VALUES (?, ?, ?, ?)",
        (task, 0, priority, due_date)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/not_completed/<int:task_id>')
def not_completed_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = 0 WHERE id = ?", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET'])
def edit_task(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_task.html', task=task)

@app.route('/edit_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    task = request.form['task']
    due_date = request.form.get('due_date')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tasks SET task = ?, due_date = ? WHERE id = ?",
        (task, due_date, task_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

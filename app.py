import os
import time
from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__, template_folder='templates', static_folder='static')

# Config from env
app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'mysql')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'root')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'devops')
app.config['MYSQL_PORT'] = int(os.environ.get('MYSQL_PORT', 3306))

mysql = MySQL(app)

def wait_for_db(max_attempts=30, delay=2):
    attempts = 0
    while attempts < max_attempts:
        try:
            conn = MySQLdb.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                passwd=app.config['MYSQL_PASSWORD'],
                db=app.config['MYSQL_DB'],
                port=app.config['MYSQL_PORT'],
                connect_timeout=5
            )
            conn.close()
            return True
        except Exception:
            attempts += 1
            time.sleep(delay)
    raise RuntimeError("DB unreachable after retries")

def init_db():
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute('''
          CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT
          );
        ''')
        mysql.connection.commit()
        cur.close()

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT message FROM messages')
    messages = cur.fetchall()
    cur.close()
    return render_template('index.html', messages=messages)

@app.route('/submit', methods=['POST'])
def submit():
    msg = request.form.get('new_message')
    if msg:
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO messages (message) VALUES (%s)', [msg])
        mysql.connection.commit()
        cur.close()
        return jsonify({'message': msg})
    return jsonify({'error': 'Empty'}), 400

@app.route('/health')
def health():
    return jsonify({'status': 'ok'}), 200

if __name__ == '__main__':
    wait_for_db()
    init_db()
    app.run(host='0.0.0.0', port=5000)

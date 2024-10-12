from AI import AI_request
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import sqlite3
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Modelos
class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(150))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Rota para a página inicial (Home)
@app.route("/")
def home():
    return render_template("home.html")

# Função para obter todos os dados (sem filtro)
def get_dados():
    try:
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT temperatura, corrente, vibracao_base, vibracao_braco, data_registro FROM dados")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("Nenhum dado encontrado no banco de dados.")
            return None

        temperatura = [row[0] for row in rows]
        corrente = [row[1] for row in rows]
        vibracao_base = [row[2] for row in rows]
        vibracao_braco = [row[3] for row in rows]
        timestamp = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m') for row in rows]

        return {
            'corrente': corrente,
            'vibracao_base': vibracao_base,
            'temperatura': temperatura,
            'vibracao_braco': vibracao_braco,
            'tempo': timestamp,
        }
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função que filtra os dados com base no intervalo de tempo e limita a 100 valores
def get_dados_filtrados(time_range):
    try:
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()

        now = datetime.now()

        # Filtra com base no intervalo de tempo selecionado
        if time_range == 'day':
            start_time = now - timedelta(days=1)
        elif time_range == 'week':
            start_time = now - timedelta(weeks=1)
        elif time_range == 'month':
            start_time = now - timedelta(days=30)
        elif time_range == 'year':
            start_time = now - timedelta(days=365)
        else:
            start_time = now  # Default para dia atual

        # Consulta o banco de dados com base no timestamp filtrado
        cursor.execute("""
            SELECT temperatura, corrente, vibracao_base, vibracao_braco, data_registro
            FROM dados
            WHERE data_registro >= ?
            ORDER BY data_registro DESC
            LIMIT 10
        """, (start_time.strftime('%Y-%m-%d %H:%M:%S'),))
        
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print(f"Nenhum dado encontrado para o intervalo: {time_range}")
            return None

        temperatura = [row[0] for row in rows]
        corrente = [row[1] for row in rows]
        vibracao_base = [row[2] for row in rows]
        vibracao_braco = [row[3] for row in rows]
        timestamp = [datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S').strftime('%d/%m/%Y %H:%M') for row in rows]

        return {
            'temperatura': temperatura,
            'corrente': corrente,
            'vibracao_base': vibracao_base,
            'vibracao_braco': vibracao_braco,
            'tempo': timestamp,
        }
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route('/api/dados')
def api_dados():
    time_range = request.args.get('time_range', 'day')
    data = get_dados_filtrados(time_range)
    #data= data[:20]
    if data is None:
        return jsonify({'error': f'Erro ao obter dados para o intervalo: {time_range}'}), 500
    return jsonify(data)

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    return render_template("dashboard.html")

# Registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registro realizado com sucesso! Você pode fazer login agora.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')

# Login de usuário
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login ou senha incorretos. Tente novamente.', 'error')

    return render_template('login.html')

# Outras rotas
@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/chat") 
def index():
    return render_template("chat.html")

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    response = AI_request(msg)
    return response

if __name__ == "__main__":
    app.run(debug=True)

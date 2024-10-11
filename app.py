from AI import AI_request
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import sqlite3
from datetime import datetime

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

def get_dados():
    try:
        conn = sqlite3.connect('instance/dados.db')
        cursor = conn.cursor()
        cursor.execute("SELECT corrente, vibracao, temperatura, timestamp FROM dados")
        rows = cursor.fetchall()
        conn.close()

        corrente = [row[0] for row in rows]
        vibracao = [row[1] for row in rows]
        temperatura = [row[2] for row in rows]
        timestamp = [datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S').strftime('%d/%m') for row in rows]



        # Mostrar um dos dados obtidos
        print(f"Primeiro dado de corrente: {corrente[0]}")
        
        return {
            'corrente': corrente,
            'vibracao': vibracao,
            'temperatura': temperatura,
            'tempo': timestamp,
        }
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Processar os dados enviados via POST, se houver.
        pass

    # Para requisições GET, carregue os dados do banco e passe para o template.
    data = get_dados()
    
    if data is None:
        return "Erro ao obter dados do banco de dados."

    # Separando os dados em objetos
    vibration_data = {
        'tempo': data['tempo'],  # tempo dos eixos x
        'values': data['vibracao'],  # Dados de vibração
    }
    
    corrente_data = {
        'tempo': data['tempo'],  # tempo dos eixos x
        'values': data['corrente'],  # Dados de corrente
    }
    
    temperature_data = {
    'tempo': data['tempo'],  # timestamp de temperatura
    'value': data['temperatura'],  # todos os valores de temperatura
    }

    
    # Renderizando a página do dashboard com os dados
    return render_template("dashboard.html", vibration_data=vibration_data, corrente_data=corrente_data, temperature_data=temperature_data,)

@app.route('/api/dados')
def api_dados():
    data = get_dados()
    if data is None:
        return jsonify({'error': 'Erro ao obter dados do banco de dados'}), 500
    return jsonify(data)


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




from AI import AI_request
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import sqlite3

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
    conn = sqlite3.connect('instance/dados.db')
    cursor = conn.cursor()
    cursor.execute("SELECT corrente, vibracao, temperatura FROM dados")
    rows = cursor.fetchall()
    conn.close()
    
    corrente = [row[0] for row in rows]
    vibracao = [row[1] for row in rows]
    temperatura = [row[2] for row in rows]
    labels = [f'Item {i+1}' for i in range(len(rows))]

    return {
        'corrente': corrente,
        'vibracao': vibracao,
        'temperatura': temperatura,
        'labels': labels
    }
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        # Processar os dados enviados via POST, se houver.
        # Por exemplo, você pode capturar dados de um formulário aqui.
        pass

    # Para requisições GET, carregue os dados do banco e passe para o template.
    data = get_dados()
    
    # Separando os dados em objetos
    vibration_data = {
        'labels': data['labels'],  # Labels dos eixos x
        'values': data['vibracao'],  # Dados de vibração
    }
    
    current_data = {
        'labels': data['labels'],  # Labels dos eixos x
        'values': data['corrente'],  # Dados de corrente
    }
    
    temperature_data = {
        'value': sum(data['temperatura']) / len(data['temperatura'])  # Média de temperatura para o gráfico Gauge
    }
    
    # Renderizando a página do dashboard com os dados
    return render_template("dashboard.html", vibration_data=vibration_data, current_data=current_data, temperature_data=temperature_data)

@app.route('/api/dados')
def api_dados():
    data = get_dados()
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

@app.route("/technologies")
def technologies():
    return render_template("technologies.html")

@app.route("/chat")
def index():
    return render_template("chat.html")

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form["msg"]
    response = AI_request(msg)
    return response

if __name__ == "__main__":
    app.run(debug=True)




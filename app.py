import os
from dotenv import load_dotenv

load_dotenv()

from urllib.parse import urlparse
import logging
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer
from AI import AI_request, AI_predict, AI_pdf
import jinja2

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

template_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'templates'))
static_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'static'))

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.join(basedir, 'instance')
os.makedirs(instance_path, exist_ok=True)

database_url = os.getenv('DATABASE_URL')
if database_url and database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua_chave_secreta')

if database_url:
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
else:
    sqlite_path = os.path.join(basedir, 'instance', 'dados.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{sqlite_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# Mapeamento do modelo corrigido para refletir a estrutura real do banco de dados de sensores
class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    temperatura = db.Column(db.Float)
    corrente = db.Column(db.Float)
    vibracao_base = db.Column(db.Float)
    vibracao_braco = db.Column(db.Float)
    data_registro = db.Column(db.String(50))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 


@app.route("/")
def home():
    try:
        return render_template("casa.html")
    except jinja2.exceptions.TemplateNotFound:
        return render_template("500.html"), 500


def mes_para_numero(mes, a=False):
    meses = {
        "janeiro": '01' if a else 1, "fevereiro": '02' if a else 2,
        "março": '03' if a else 3, "abril": '04' if a else 4,
        "maio": '05' if a else 5, "junho": '06' if a else 6,
        "julho": '07' if a else 7, "agosto": '08' if a else 8,
        "setembro": '09' if a else 9, "outubro": '10' if a else 10,
        "novembro": '11' if a else 11, "dezembro": '12' if a else 12
    }
    return meses.get(mes.lower(), "Mês inválido")


def obter_dias_da_semana(mes, numero_semana):
    numero_semana = int(numero_semana)
    if mes < 1 or mes > 12:
        return "Mês inválido."
    ano_atual = datetime.now().year
    primeiro_dia_do_mes = datetime(ano_atual, mes, 1)
    ultimo_dia_do_mes = (primeiro_dia_do_mes + timedelta(days=31)).replace(day=1) - timedelta(days=1)
    inicio_semana = primeiro_dia_do_mes + timedelta(weeks=numero_semana - 1)
    fim_semana = inicio_semana + timedelta(days=6)
    if fim_semana > ultimo_dia_do_mes:
        fim_semana = ultimo_dia_do_mes
    return f"{inicio_semana.day:02}", f"{fim_semana.day:02}"


def get_sensor_data(time_range, day, month, week, year, mesSemana):
    conn = sqlite3.connect('instance/dados.db')
    cursor = conn.cursor()
    match time_range:
        case "day":
            comando_sql = """
            SELECT 
                GROUP_CONCAT(temperatura) AS dados_temperatura,
                GROUP_CONCAT(corrente) AS dados_corrente,
                GROUP_CONCAT(vibracao_base) AS dados_vibracao_base,
                GROUP_CONCAT(vibracao_braco) AS dados_vibracao_braco,
                GROUP_CONCAT(strftime('%H:%M', data_registro)) AS horas
            FROM dados
            WHERE DATE(data_registro) = ?;
            """
            cursor.execute(comando_sql, (day,))
            rows = cursor.fetchall()
            conn.close()

            if not rows or not rows[0][0]:
                return {'temperatura': [], 'corrente': [], 'vibracao_base': [], 'vibracao_braco': [], 'timestamp': []}

            return {
                'temperatura': list(map(float, rows[0][0].split(','))),
                'corrente': list(map(float, rows[0][1].split(','))),
                'vibracao_base': list(map(float, rows[0][2].split(','))),
                'vibracao_braco': list(map(float, rows[0][3].split(','))),
                'timestamp': rows[0][4].split(',')
            }

        case "week":
            mes = mes_para_numero(mesSemana, a=True)
            dias = obter_dias_da_semana(mes_para_numero(mesSemana), week)
            comando_sql = f"""
            SELECT 
                strftime('%Y-%m-%d', data_registro) AS dia,
                AVG(temperatura), AVG(corrente), AVG(vibracao_base), AVG(vibracao_braco)
            FROM dados
            WHERE strftime('%Y', data_registro) = '2024' AND strftime('%m', data_registro) = ?
            AND data_registro >= date('2024-{mes}-{dias[0]}') AND data_registro <= date('2024-{mes}-{dias[1]}')
            GROUP BY dia ORDER BY dia;
            """
            cursor.execute(comando_sql, (mes,))
            resultados = cursor.fetchall()
            conn.close()

            return {
                'temperatura': [r[1] for r in resultados],
                'corrente': [r[2] for r in resultados],
                'vibracao_base': [r[3] for r in resultados],
                'vibracao_braco': [r[4] for r in resultados],
                'timestamp': [r[0] for r in resultados]
            }

        case "month":
            mes = mes_para_numero(month, a=True)
            comando_sql = """
            SELECT 
                strftime('%Y-%m-%W', data_registro) AS semana,
                AVG(temperatura), AVG(corrente), AVG(vibracao_base), AVG(vibracao_braco)
            FROM dados
            WHERE strftime('%Y', data_registro) = '2024' AND strftime('%m', data_registro) = ?
            GROUP BY semana ORDER BY semana;
            """
            cursor.execute(comando_sql, (mes,))
            resultados = cursor.fetchall()
            conn.close()

            return {
                'temperatura': [r[1] for r in resultados],
                'corrente': [r[2] for r in resultados],
                'vibracao_base': [r[3] for r in resultados],
                'vibracao_braco': [r[4] for r in resultados],
                'timestamp': [r[0] for r in resultados]
            }

        case 'year': 
            comando_sql = """
            SELECT 
                strftime('%m', data_registro) AS mes,
                AVG(temperatura), AVG(corrente), AVG(vibracao_base), AVG(vibracao_braco)
            FROM dados
            WHERE strftime('%Y', data_registro) = ?
            GROUP BY mes ORDER BY mes;
            """
            cursor.execute(comando_sql, (year,))
            resultados = cursor.fetchall()
            conn.close()

            return {
                'temperatura': [r[1] for r in resultados],
                'corrente': [r[2] for r in resultados],
                'vibracao_base': [r[3] for r in resultados],
                'vibracao_braco': [r[4] for r in resultados],
                'timestamp': [r[0] for r in resultados]
            }


@app.route('/dados_graficos', methods=['POST'])
def dados_graficos():
    filters = request.json
    data = get_sensor_data(
        filters.get('timeRange'), filters.get('day'), filters.get('month'),
        filters.get('week'), filters.get('year'), filters.get('monthWeek')
    )
    return jsonify(data)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Nome de usuário já existe.', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        db.session.add(User(username=username, password=hashed_password))
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        username = request.form['username']
        if User.query.filter_by(username=username).first():
            token = serializer.dumps(username, salt='senha_reset')
            return jsonify({"redirect": url_for('reset_senha', token=token, _external=True)})
        return jsonify({"error": "Usuário não encontrado"}), 404
    return render_template('esqueci_senha.html')
    

@app.route('/reset_senha/<token>', methods=['GET', 'POST'])
def reset_senha(token):
    try:
        username = serializer.loads(token, salt='senha_reset', max_age=3600)
    except:
        flash('O token expirou.', 'error')
        return redirect(url_for('esqueci_senha'))

    user = User.query.filter_by(username=username).first()
    if request.method == 'POST' and user:
        user.password = generate_password_hash(request.form['nova_senha'], method='pbkdf2:sha256')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('reset_senha.html', token=token)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['is_admin'] = user.is_admin
            return redirect(url_for('dashboard'))
        flash('Login ou senha incorretos.', 'error')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):
        return redirect(url_for('dashboard'))
    return render_template('admin_dashboard.html')


@app.route('/admin/users', methods=['POST'])
def get_users():
    users = User.query.all()
    return jsonify(users=[{'id': u.id, 'username': u.username, 'is_admin': u.is_admin} for u in users])


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/admin/users/<int:user_id>/make-admin', methods=['PATCH'])
def make_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = True
        db.session.commit()
        return jsonify(message='Usuário promovido a admin com sucesso!'), 200
    return jsonify(message='Usuário não encontrado!'), 404


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route("/inserir_dados", methods=["POST"])
def inserir_dados():
    dados = request.get_json()
    temperatura = dados.get("temperatura")
    vibracao_base = dados.get("vibracao_base")
    corrente = dados.get("corrente")
    data_registro = dados.get("data_registro")
    vibracao_braco = dados.get("vibracao_braco")

    with sqlite3.connect('instance/dados.db') as conn:
        cursor = conn.cursor()
        # Garantido a criação da tabela correta chamada 'dados'
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dados (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                temperatura REAL,
                vibracao_base REAL,
                corrente REAL,
                data_registro TEXT,
                vibracao_braco REAL
            )
        ''')
        cursor.execute('''
            INSERT INTO dados (temperatura, vibracao_base, corrente, data_registro, vibracao_braco)
            VALUES (?, ?, ?, ?, ?)
        ''', (temperatura, vibracao_base, corriente, data_registro, vibracao_braco))
        conn.commit()

    return jsonify({"status": "sucesso"}), 200


@app.route("/braco")
def braco(): return render_template("braco.html")

@app.route("/chat")
def index(): return render_template("chat.html")


@app.route("/get", methods=["GET", "POST"])
def chat():
    input_text = request.form.get("msg", "").strip()
    if not input_text:
        return jsonify(resposta="Envie uma mensagem para continuar."), 400

    try:
        # Corrigido: O tratamento de geração de texto de relatório/PDF agora é controlado 
        # organicamente pela própria instrução do sistema (System Instruction da IA).
        resposta = AI_request(input_text)
        return jsonify(resposta=resposta)
    except Exception as e:
        logger.exception("Erro na rota /get")
        return jsonify(resposta="Não foi possível obter resposta da IA. Verifique as chaves."), 500


@app.route("/auto", methods=["GET"])
def automatic_message():
    try:
        return AI_predict()
    except Exception as e:
        logger.exception("Erro na rota /auto")
        return "Previsão indisponível.", 500


@app.route("/pdf", methods=["POST"])
def pdf():
    dados = request.get_json()
    filtros = dados.get('filters')
    leituras = dados.get('data')
    return AI_pdf(filtros, leituras)


@app.errorhandler(404)
def page_not_found(e): return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e): return render_template('500.html'), 500


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0', port=port)
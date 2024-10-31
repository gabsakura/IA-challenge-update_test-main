from AI import AI_request, AI_predict, AI_pdf
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import sqlite3
from datetime import datetime, timedelta
from itsdangerous import URLSafeTimedSerializer


serializer = URLSafeTimedSerializer('sua_chave_secreta')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
# Modelos
class Dados(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    info = db.Column(db.String(150))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False) 

# Rota para a página inicial (Home)
@app.route("/")
def home():
    return render_template("home.html")

def mes_para_numero(mes, a=False):
    
    if a: 
        meses = {
        "janeiro": '01',
        "fevereiro": '02',
        "março": '03',
        "abril": '04',
        "maio": '05',
        "junho": '06',
        "julho": '07',
        "agosto": '08',
        "setembro": '09',
        "outubro": '10',
        "novembro": '11',
        "dezembro": '12'
        }
    else:
        meses = {
        "janeiro": 1,
        "fevereiro": 2,
        "março" : 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12
        }
    mes_lower = mes.lower()
    
    return meses.get(mes_lower, "Mês inválido")

def obter_dias_da_semana(mes, numero_semana):
    # Verifica se o mês e o número da semana são válidos
    numero_semana = int(numero_semana)
    if mes < 1 or mes > 12:
        return "Mês inválido. Deve ser entre 1 e 12."
    if numero_semana < 1 or numero_semana > 4:
        return "Número da semana inválido. Deve ser entre 1 e 4."

    # Obtém o ano atual
    ano_atual = datetime.now().year
    
    # Calcula o primeiro dia do mês
    primeiro_dia_do_mes = datetime(ano_atual, mes, 1)

    # Calcula o último dia do mês
    ultimo_dia_do_mes = (primeiro_dia_do_mes + timedelta(days=31)).replace(day=1) - timedelta(days=1)

    # Calcula o início da semana
    inicio_semana = primeiro_dia_do_mes + timedelta(weeks=numero_semana - 1)

    # Calcula o fim da semana
    fim_semana = inicio_semana + timedelta(days=6)

    # Se o fim da semana ultrapassa o último dia do mês, ajusta
    if fim_semana > ultimo_dia_do_mes:
        fim_semana = ultimo_dia_do_mes
        
    # Retorna os dias como strings com 2 caracteres
    return f"{inicio_semana.day:02}", f"{fim_semana.day:02}"


def get_sensor_data(time_range, day, month, week, year, mesSemana):
    conn = sqlite3.connect('instance/dados.db')
    cursor = conn.cursor()
    match time_range:
        case "day":
            comando_sql = f"""
            SELECT 
                GROUP_CONCAT(temperatura) AS dados_temperatura,
                GROUP_CONCAT(corrente) AS dados_corrente,
                GROUP_CONCAT(vibracao_base) AS dados_vibracao_base,
                GROUP_CONCAT(vibracao_braco) AS dados_vibracao_braco,
                GROUP_CONCAT(strftime('%H:%M', data_registro)) AS horas
            FROM dados
            WHERE DATE(data_registro) = '{day}';
            """
            cursor.execute(comando_sql)
            rows = cursor.fetchall()
            conn.close()
   
            dados_temperatura_str = rows[0][0]  # Ex: "24,25,24"
            dados_corrente_str = rows[0][1]     # Ex: "1,4,2"
            dados_vibracao_base_str = rows[0][2] # Ex: "1.1,2.1,3.5"
            dados_vibracao_braco_str = rows[0][3] # Ex: "2.5,3.2,5.5"
            horas_str = rows[0][4]               # Ex: "08:00:00,08:15:00"

            # Transformar os dados em listas
            dados_temperatura = list(map(float, dados_temperatura_str.split(','))) if dados_temperatura_str else []
            dados_corrente = list(map(float, dados_corrente_str.split(','))) if dados_corrente_str else []
            dados_vibracao_base = list(map(float, dados_vibracao_base_str.split(','))) if dados_vibracao_base_str else []
            dados_vibracao_braco = list(map(float, dados_vibracao_braco_str.split(','))) if dados_vibracao_braco_str else []
            horas = horas_str.split(',') if horas_str else []

            # Combinar todas as listas em uma única lista
            lista_unica = [dados_temperatura, dados_corrente, dados_vibracao_base, dados_vibracao_braco, horas]

            
            print(lista_unica[4])
            # Estruturar os dados em um formato de dicionário
            data = {
                'temperatura': lista_unica[0],
                'corrente': lista_unica[1],
                'vibracao_base': lista_unica[2],
                'vibracao_braco': lista_unica[3],
                'timestamp': lista_unica[4]
            }

            return data
    
        case "week":
            mes = mes_para_numero(mesSemana, a=True)
            dias = obter_dias_da_semana(mes_para_numero(mesSemana), week)
            comando_sql = f"""
            SELECT 
                strftime('%Y-%m-%d', data_registro) AS dia,
                AVG(temperatura) AS media_temperatura,
                AVG(corrente) AS media_corrente,
                AVG(vibracao_base) AS media_vibracao_base,
                AVG(vibracao_braco) AS media_vibracao_braco
            FROM dados
            WHERE 
                strftime('%Y', data_registro) = '2024' AND
                strftime('%m', data_registro) = '{mes}' AND
                data_registro >= date('2024-{mes}-{dias[0]}') AND 
                data_registro <= date('2024-{mes}-{dias[1]}')
            GROUP BY dia  -- Agrupa pelos dias para calcular as médias
            ORDER BY dia;
            """
            cursor.execute(comando_sql)
            resultados = cursor.fetchall()  # Busca todos os resultados
            conn.close()
            
            # Inicializa listas para armazenar os dados
            dias_list = []
            media_temperatura_list = []
            media_corrente_list = []
            media_vibracao_base_list = []
            media_vibracao_braco_list = []

            # Processa os resultados
            for linha in resultados:
                dias_list.append(linha[0])  # Dia
                media_temperatura_list.append(linha[1])  # Média de Temperatura
                media_corrente_list.append(linha[2])  # Média de Corrente
                media_vibracao_base_list.append(linha[3])  # Média de Vibração Base
                media_vibracao_braco_list.append(linha[4])  # Média de Vibração do Braço

            # Junta todas as listas em uma única lista
            dados_combinados = [
                media_temperatura_list,
                media_corrente_list,
                media_vibracao_base_list,
                media_vibracao_braco_list,
                dias_list
            ]

            data = {
                'temperatura': dados_combinados[0],
                'corrente': dados_combinados[1],
                'vibracao_base': dados_combinados[2],
                'vibracao_braco': dados_combinados[3],
                'timestamp': dados_combinados[4]
            }

            return data
                    
        case "month":
            mes = mes_para_numero(month, a=True)
            comando_sql = f"""
            SELECT 
                strftime('%Y-%m-%W', data_registro) AS semana,
                AVG(temperatura) AS media_temperatura,
                AVG(corrente) AS media_corrente,
                AVG(vibracao_base) AS media_vibracao_base,
                AVG(vibracao_braco) AS media_vibracao_braco
            FROM dados
            WHERE 
                strftime('%Y', data_registro) = '2024' AND
                strftime('%m', data_registro) = '{mes}'
            GROUP BY semana
            ORDER BY semana;
            """

            # Executa a consulta SQL
            cursor.execute(comando_sql)
            resultados = cursor.fetchall()  # Busca todos os resultados
            conn.close()

            # Inicializa listas para armazenar os dados
            media_temperatura_list = []
            media_corrente_list = []
            media_vibracao_base_list = []
            media_vibracao_braco_list = []
            semanas_list = []

            # Processa os resultados
            for linha in resultados:
                semanas_list.append(linha[0])  # Semana
                media_temperatura_list.append(linha[1])  # Média de Temperatura
                media_corrente_list.append(linha[2])  # Média de Corrente
                media_vibracao_base_list.append(linha[3])  # Média de Vibração Base
                media_vibracao_braco_list.append(linha[4])  # Média de Vibração do Braço

            # Junta todas as listas em uma única lista
            dados_combinados = [
                media_temperatura_list,
                media_corrente_list,
                media_vibracao_base_list,
                media_vibracao_braco_list,
                semanas_list
            ]

            data = {
                'temperatura': dados_combinados[0],
                'corrente': dados_combinados[1],
                'vibracao_base': dados_combinados[2],
                'vibracao_braco': dados_combinados[3],
                'timestamp': dados_combinados[4]
            }

            return data
            
        case 'year': 
            comando_sql = f"""
                SELECT 
                    strftime('%m', data_registro) AS mes,
                    AVG(temperatura) AS media_temperatura,
                    AVG(corrente) AS media_corrente,
                    AVG(vibracao_base) AS media_vibracao_base,
                    AVG(vibracao_braco) AS media_vibracao_braco
                FROM dados
                WHERE 
                    strftime('%Y', data_registro) = '{year}'
                GROUP BY mes
                ORDER BY mes;
                """

            # Executa a consulta SQL
            cursor.execute(comando_sql)
            resultados = cursor.fetchall()  # Busca todos os resultados
            conn.close()
            
            # Inicializa listas para armazenar os dados
            media_temperatura_list = []
            media_corrente_list = []
            media_vibracao_base_list = []
            media_vibracao_braco_list = []
            meses_list = []

            # Processa os resultados e separa em listas
            for linha in resultados:
                meses_list.append(linha[0])  # Mês
                media_temperatura_list.append(linha[1])  # Média de Temperatura
                media_corrente_list.append(linha[2])  # Média de Corrente
                media_vibracao_base_list.append(linha[3])  # Média de Vibração Base
                media_vibracao_braco_list.append(linha[4])  # Média de Vibração do Braço
            
            # Junta todas as listas em uma única lista
            dados_combinados = [
                media_temperatura_list,
                media_corrente_list,
                media_vibracao_base_list,
                media_vibracao_braco_list,
                meses_list
            ]
            
            print(dados_combinados)
            data = {
                'temperatura': dados_combinados[0],
                'corrente': dados_combinados[1],
                'vibracao_base': dados_combinados[2],
                'vibracao_braco': dados_combinados[3],
                'timestamp': dados_combinados[4]
            }

            return data
                

@app.route('/dados_graficos', methods=['POST'])  # Alterado para aceitar apenas POST
def dados_graficos():
    filters = request.json
    
    time_range = filters.get('timeRange')
    day = filters.get('day')
    month = filters.get('month')
    week = filters.get('week')
    year = filters.get('year')
    mesSemana = filters.get('monthWeek')
    
    data = get_sensor_data(time_range, day, month, week, year, mesSemana)
    
    return jsonify(data)


# Registro de usuário
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['user']
        password = request.form['password']
        user_existente = User.query.filter_by(username=username).first()
        if user_existente:
            flash('Nome de usuário já existe. Tente outro.', 'error')
            return redirect(url_for('register'))
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registro realizado com sucesso! Você pode fazer login agora.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')




# Rota para solicitar redefinição de senha

@app.route('/esqueci_senha', methods=['GET', 'POST'])
def esqueci_senha():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if user:
            token = serializer.dumps(username, salt='senha_reset')
            return jsonify({"redirect": url_for('reset_senha', token=token, _external=True)})
        else:
            return jsonify({"error": "Nome de usuário não encontrado"}), 404
    return render_template('esqueci_senha.html')
    
@app.route('/reset_senha/<token>', methods=['GET', 'POST'])
def reset_senha(token):
    try:
        username = serializer.loads(token, salt='senha_reset', max_age=3600)
    except:
        flash('O token de redefinição de senha expirou.', 'error')
        return redirect(url_for('esqueci_senha'))

    user = User.query.filter_by(username=username).first()
    if request.method == 'POST' and user:
        nova_senha = request.form['nova_senha']
        hashed_password = generate_password_hash(nova_senha)  # Removido o método sha256
        user.password = hashed_password
        db.session.commit()
        flash('Senha atualizada com sucesso!', 'success')
        return redirect(url_for('login'))  # Certifique-se de ter uma rota de login

    return render_template('reset_senha.html', token=token)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('user')  # Use .get() para evitar KeyError
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['username'] = user.username
            session['is_admin'] = user.is_admin  # Armazena o status de admin na sessão
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))  # Redireciona para o painel do usuário
        else:
            flash('Login ou senha incorretos. Tente novamente.', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Você precisa estar logado para acessar o dashboard.', 'error')
        return redirect(url_for('login'))  # Redireciona para a página de login se não estiver logado
    
    return render_template('dashboard.html')  # Renderiza o template do dashboard

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('is_admin'):  # Verifica se o usuário é admin
        flash('Acesso negado. Você não tem permissão para acessar esta página.')
        return redirect(url_for('dashboard'))  # Redireciona para o dashboard normal
    return render_template('admin_dashboard.html')


# Criação da rota para buscar usuários com filtros
# Endpoint para obter usuários
@app.route('/admin/users', methods=['POST'])
def get_users():
    users = User.query.all()
    return jsonify(users=[{'id': user.id, 'username': user.username, 'is_admin': user.is_admin} for user in users])

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/admin/users/<int:user_id>/make-admin', methods=['PATCH'])
def make_admin(user_id):
    user = User.query.get(user_id)
    if user:
        user.is_admin = True  # Promove o usuário a administrador
        db.session.commit()
        return jsonify(message='Usuário promovido a admin com sucesso!'), 200
    else:
        return jsonify(message='Usuário não encontrado!'), 404

# Inicializando o banco de dados
def create_tables():
    with app.app_context():  # Cria um contexto de aplicativo
        db.create_all()

# Chame a função de criação de tabelas apenas uma vez
create_tables()

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso.', 'success')
    return redirect(url_for('login'))


@app.route("/braco")
def braco():
    return render_template("braco.html")
@app.route("/login")
def asd():
    return render_template("login.html")
@app.route("/chat")
def index():
    return render_template("chat.html")

@app.route("/get", methods = ["GET", "POST"])
def chat():
    input = request.form["msg"]
    
    if "pdf" in input.lower():
        AI_pdf(input)
        return jsonify(url=f'relatório.pdf')
    else:
        return AI_request(input)

@app.route("/auto", methods = ["GET"])
def automatic_message():
    return AI_predict()

@app.route("/pdf", methods = ["POST"])
def pdf():
    
    dados = request.get_json()
    filtros = dados.get('filters')
    leituras = dados.get('data')
    
    return AI_pdf(filtros, leituras)
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
 
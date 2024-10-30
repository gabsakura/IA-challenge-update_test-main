from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dados.db'
db = SQLAlchemy(app)
serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@app.route('/esqueci_senha', methods=['GET', 'POST'])
def senha():
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
        return redirect(url_for('senha'))

    user = User.query.filter_by(username=username).first()
    if request.method == 'POST' and user:
        nova_senha = request.form['nova_senha']
        hashed_password = generate_password_hash(nova_senha, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Senha atualizada com sucesso!', 'success')
        return redirect(url_for('login')) # Certifique-se de ter uma rota de login

    return render_template('reset_senha.html', token=token)

if __name__ == '__main__':
    app.run(debug=True)

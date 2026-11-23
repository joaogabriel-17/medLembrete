from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Medicamento, HistoricoDose
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SESSION_SECRET')
if not app.config['SECRET_KEY']:
    raise RuntimeError('Defina a variável de ambiente SESSION_SECRET antes de iniciar o MedLembrete.')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///medlembrete.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        if User.query.filter_by(email=email).first():
            flash('Este e-mail já está registado.', 'danger')
            return redirect(url_for('cadastro'))

        novo_usuario = User(
            nome=nome,
            email=email,
            senha_hash=generate_password_hash(senha)
        )
        db.session.add(novo_usuario)
        db.session.commit()
        flash('Registo concluído! Faça login para continuar.', 'success')
        return redirect(url_for('login'))
    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.senha_hash, senha):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('E-mail ou palavra-passe incorretos.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/dashboard')
@login_required
def dashboard():
    turno_filtro = request.args.get('turno', 'Todos')
    query = Medicamento.query.filter_by(user_id=current_user.id)

    if turno_filtro != 'Todos':
        query = query.filter_by(turno=turno_filtro)

    
    medicamentos = query.order_by(Medicamento.horario.asc()).all()

    
    hoje = datetime.now().date()
    historico_hoje = [
        h for med in current_user.medicamentos 
        for h in med.historico if h.data_hora.date() == hoje
    ]

    return render_template(
        'dashboard.html',
        medicamentos=medicamentos,
        turno_atual=turno_filtro,
        historico_hoje=historico_hoje
    )


@app.route('/medicamento/novo', methods=['GET', 'POST'])
@login_required
def novo_medicamento():
    if request.method == 'POST':
        med = Medicamento(
            user_id=current_user.id,
            nome=request.form.get('nome'),
            dose=request.form.get('dose'),
            horario=request.form.get('horario'),
            turno=request.form.get('turno'),
            estoque_atual=int(request.form.get('estoque_atual'))
        )
        db.session.add(med)
        db.session.commit()
        flash('Medicamento adicionado com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('form_medicamento.html', med=None)

@app.route('/medicamento/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_medicamento(id):
    med = Medicamento.query.get_or_404(id)
    if med.user_id != current_user.id:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        med.nome = request.form.get('nome')
        med.dose = request.form.get('dose')
        med.horario = request.form.get('horario')
        med.turno = request.form.get('turno')
        med.estoque_atual = int(request.form.get('estoque_atual'))
        db.session.commit()
        flash('Medicamento atualizado!', 'success')
        return redirect(url_for('dashboard'))
    return render_template('form_medicamento.html', med=med)

@app.route('/medicamento/excluir/<int:id>', methods=['POST'])
@login_required
def excluir_medicamento(id):
    med = Medicamento.query.get_or_404(id)
    if med.user_id == current_user.id:
        db.session.delete(med)
        db.session.commit()
        flash('Medicamento removido.', 'warning')
    return redirect(url_for('dashboard'))


@app.route('/medicamento/tomar/<int:id>', methods=['POST'])
@login_required
def tomar_medicamento(id):
    med = Medicamento.query.get_or_404(id)
    if med.user_id == current_user.id:
        
        registro = HistoricoDose(medicamento_id=med.id)
        db.session.add(registro)

        if med.estoque_atual > 0:
            med.estoque_atual -= 1

        db.session.commit()
        flash(f'Dose de {med.nome} registada!', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
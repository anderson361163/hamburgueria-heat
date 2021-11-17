from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login.utils import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import db, User
from flask_login import current_user
from app.email.mailer import send_mail
from config import Config
import threading
from requests import api
from config import Config

login_bp = Blueprint(
    'login', __name__, template_folder='templates'
)


@login_bp.route('/login/', methods=['GET'])
def render_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    return render_template('login.j2', recaptcha=Config.RECAPTCHA_SITE_KEY)


@login_bp.route('/login/', methods=['POST'])
def login():
    payload = {
        'secret': Config.RECAPTCHA_VALIDATION_KEY,
        'response': request.form.get('g-recaptcha-response')
    }

    response = api.post(
        'https://www.google.com/recaptcha/api/siteverify',
        params=payload
    )

    if not response.json()['success']:
        flash('Preencha o reCaptcha')
        return redirect(url_for('login.render_login'))

    username = request.form.get('username')
    password = request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        flash('Não foi possível fazer login. Usuário ou senha incorretos')
        return redirect(url_for('login.render_login'))

    login_user(user)
    return redirect(url_for('admin.index'))


@login_bp.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login.login'))


@login_bp.route('/recover_password/', methods=['GET'])
def recover_password():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    return render_template('recover_password.j2')


@login_bp.route('/recover_password/', methods=['POST'])
def recover_password_login():
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('E-mail não cadastrado', 'error')
        return redirect(url_for('login.recover_password'))

    token = user.get_reset_token()
    entity = {}
    entity['name'] = user.name
    entity['url'] = url_for('login.reset_token', token=token, _external=True)

    params_email = {
        'text_type': 'html',
        'sender': Config.EMAIL_USER,
        'to': email,
        'subject': '🍔🔥 Recupere sua senha na Hamburgueria Heat! 🔥🍔',
        'template': 'reset_password_mail',
        'entity': entity,
        'images': ['logo.png']
    }
    th = threading.Thread(target=send_mail, args=[params_email])
    th.start()

    flash('Instruções foram enviadas para seu e-mail!', 'warning')
    return redirect(url_for('login.render_login'))


@login_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))

    user = User.verify_reset_token(token)

    if user is None:
        flash('Token expirado ou inválido', 'warning')
        return redirect(url_for('login.recover_password'))

    if request.method == "GET":
        return render_template('reset_password.j2', token=token)

    senha = request.form.get('password')

    user.password = generate_password_hash(senha)
    db.session.commit()

    flash('Senha foi salva com sucesso', 'success')
    return redirect(url_for('login.render_login'))

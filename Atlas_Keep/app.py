from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///password_manager.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'supersecretkey'  # Alterar para uma chave secreta real
db = SQLAlchemy(app)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website_name = db.Column(db.String(150), nullable=False)
    website_link = db.Column(db.String(200), nullable=False)
    email_login = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    plain_password = db.Column(db.String(200), nullable=False)  # Campo para armazenar a senha normal

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_password', methods=['GET', 'POST'])
def add_password():
    if request.method == 'POST':
        website_name = request.form['website_name']
        website_link = request.form['website_link']
        email_login = request.form['email_login']
        password = request.form['password']

        if not website_name or not website_link or not email_login or not password:
            flash('Por favor, preencha todos os campos.')
            return redirect(url_for('add_password'))  # Redireciona para a página de adição de senhas

        # Criptografar a senha
        hashed_password = generate_password_hash(password)  # Criptografada
        plain_password = password  # Senha em texto plano

        new_password = Password(
            website_name=website_name,
            website_link=website_link,
            email_login=email_login,
            password=hashed_password,
            plain_password=plain_password  # Armazenar a senha normal
        )
        db.session.add(new_password)
        db.session.commit()

        flash('Senha adicionada com sucesso!')
        return redirect(url_for('view_passwords'))

    return render_template('add_password.html')  # Retorna o template para adicionar senhas

@app.route('/view_passwords')
def view_passwords():
    passwords = Password.query.all()
    return render_template('passwords.html', passwords=passwords)

@app.route('/edit_password/<int:id>', methods=['GET', 'POST'])
def edit_password(id):
    password_to_edit = Password.query.get_or_404(id)

    if request.method == 'POST':
        password_to_edit.website_name = request.form['website_name']
        password_to_edit.website_link = request.form['website_link']
        password_to_edit.email_login = request.form['email_login']
        password_to_edit.password = generate_password_hash(request.form['password'])  # Hashing a nova senha

        db.session.commit()
        flash('Senha atualizada com sucesso!')
        return redirect(url_for('view_passwords'))

    return render_template('edit_password.html', password=password_to_edit)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

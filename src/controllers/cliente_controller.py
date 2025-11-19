from flask import Blueprint, render_template, request, redirect, url_for
from db.session import SessionLocal
from repositories.ClienteRepository import ClienteRepository
from model import Cliente

cliente_bp = Blueprint('cliente', __name__, url_prefix='/clientes')

@cliente_bp.route('/')
def index():
    db_session = SessionLocal()
    cliente_repo = ClienteRepository(db_session)
    clientes = cliente_repo.get_all_clientes()
    db_session.close()
    return render_template('clientes/clientes.html', clientes=clientes)

@cliente_bp.route('/novo', methods=['GET', 'POST'])
def novo_cliente():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        cliente = Cliente(nome=nome, telefone=telefone, email=email)
        db_session = SessionLocal()
        cliente_repo = ClienteRepository(db_session)
        cliente_repo.create_cliente(cliente)
        db_session.close()
        return redirect(url_for('cliente.index'))
    return render_template('clientes/novo_cliente.html')

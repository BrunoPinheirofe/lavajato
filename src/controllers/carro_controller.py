from flask import Blueprint, render_template, request, redirect, url_for
from db.session import SessionLocal
from repositories.CarroRepository import CarroRepository
from repositories.ClienteRepository import ClienteRepository
from model import Carro

carro_bp = Blueprint('carro', __name__, url_prefix='/carros')

@carro_bp.route('/')
def index():
    db_session = SessionLocal()
    carro_repo = CarroRepository(db_session)
    carros = carro_repo.get_all_carros()
    db_session.close()
    return render_template('carros.html', carros=carros)

@carro_bp.route('/novo', methods=['GET', 'POST'])
def novo_carro():
    if request.method == 'POST':
        marca = request.form['marca']
        modelo = request.form['modelo']
        ano = request.form['ano']
        placa = request.form['placa']
        cliente_id = request.form['cliente_id']
        carro = Carro(marca=marca, modelo=modelo, ano=ano, placa=placa, cliente_id=cliente_id)
        db_session = SessionLocal()
        carro_repo = CarroRepository(db_session)
        carro_repo.create_carro(carro)
        db_session.close()
        return redirect(url_for('carro.index'))
    
    db_session = SessionLocal()
    cliente_repo = ClienteRepository(db_session)
    clientes = cliente_repo.get_all_clientes()
    db_session.close()
    return render_template('novo_carro.html', clientes=clientes)

from flask import Blueprint, render_template, request, redirect, url_for
from db.session import SessionLocal
from repositories.TipoLavagemRepository import TipoLavagemRepository
from model import TipoLavagem

servico_bp = Blueprint('servico', __name__, url_prefix='/servicos')

@servico_bp.route('/')
def index():
    db_session = SessionLocal()
    tipo_lavagem_repo = TipoLavagemRepository(db_session)
    servicos = tipo_lavagem_repo.get_all_tipos_lavagem()
    db_session.close()
    return render_template('servicos/servicos.html', servicos=servicos)

@servico_bp.route('/novo', methods=['GET', 'POST'])
def novo_servico():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = request.form['preco']
        servico = TipoLavagem(nome=nome, preco=preco)
        db_session = SessionLocal()
        tipo_lavagem_repo = TipoLavagemRepository(db_session)
        tipo_lavagem_repo.create_tipo_lavagem(servico)
        db_session.close()
        return redirect(url_for('servico.index'))
    return render_template('servicos/novo_servico.html')

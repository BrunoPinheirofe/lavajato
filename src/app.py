from flask import Flask, render_template
from db.session import engine
from db.session import SessionLocal
from repositories.ClienteRepository import ClienteRepository
from models.model import Base

app = Flask(__name__)

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)
print(Base.metadata.tables.keys())


@app.route('/clientes', methods=['GET', 'POST'])
def listar_clientes(request):
    if request.method == 'POST':
        # Lógica para adicionar um novo cliente
        nome = request.form['nome']
        email = request.form['email']
        novo_cliente = {'nome': nome, 'email': email}
        db_session = SessionLocal()
        cliente_repo = ClienteRepository(db_session)
        cliente_repo.create_cliente(novo_cliente)
        db_session.close()
    db_session = SessionLocal()
    cliente_repo = ClienteRepository(db_session)
    clientes = cliente_repo.get_all_clientes()
    db_session.close()
    return render_template('clientes.html', clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True)

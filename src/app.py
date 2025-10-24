from flask import Flask, render_template
from db.session import engine
from db.session import SessionLocal
from repositories.ClienteRepository import ClienteRepository
from models.model import Base

app = Flask(__name__)

# Cria as tabelas no banco de dados, se não existirem
Base.metadata.create_all(bind=engine)
print(Base.metadata.tables.keys())


@app.route('/clientes')
def listar_clientes():
    db_session = SessionLocal()
    cliente_repo = ClienteRepository(db_session)
    clientes = cliente_repo.get_all_clientes()
    db_session.close()
    return render_template('clientes.html', clientes=clientes)

if __name__ == '__main__':
    app.run(debug=True)

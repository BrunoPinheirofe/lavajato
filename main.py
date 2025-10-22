# main.py
from database import inicializar_arquivos
from clientes import cadastrar_cliente, listar_clientes
from carros import cadastrar_carro, listar_carros, listar_carros_cliente
from lavagens import cadastrar_tipo_lavagem, listar_tipos_lavagem
from agendamentos import cadastrar_agendamento, listar_agendamentos
from editar import editar_registro
def menu_principal():
    """Menu principal do sistema"""
    
    # Inicializar arquivos do banco de dados
    inicializar_arquivos()
    
    # Criar tipos de lavagem pré-definidos se não existirem
    from lavagens import criar_tipos_predefinidos
    criar_tipos_predefinidos()
    
def menu_principal():
    """Menu principal do sistema"""
    while True:
        print("\n" + "="*50)
        print("SISTEMA LAVA JATO - MENU PRINCIPAL")
        print("="*50)
        print("1. Cadastrar Tipo de Lavagem")
        print("2. Cadastrar Cliente (com opção de cadastrar carro)")
        print("3. Cadastrar Carro (para cliente existente)")
        print("4. Cadastrar Agendamento")
        print("5. Listar Tipos de Lavagem")
        print("6. Listar Clientes")
        print("7. Listar Carros")
        print("8. Listar Carros de um Cliente")
        print("9. Listar Agendamentos")
        print("10. Editar Registro")
        print("11. Sair")
        print("="*50)
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == '1':
            cadastrar_tipo_lavagem()
        elif opcao == '2':
            cadastrar_cliente()
        elif opcao == '3':
            cadastrar_carro()
        elif opcao == '4':
            cadastrar_agendamento()
        elif opcao == '5':
            listar_tipos_lavagem()
        elif opcao == '6':
            listar_clientes()
        elif opcao == '7':
            listar_carros()
        elif opcao == '8':
            listar_carros_cliente()
        elif opcao == '9':
            listar_agendamentos()
        elif opcao == '10':
            editar_registro()
        elif opcao == '10':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida! Tente novamente.")
        
        input("\nPressione Enter para continuar...")

def main():
    """Função principal"""
    inicializar_arquivos()
    print("Sistema Lava Jato inicializado!")
    print("Arquivos de dados preparados.")
    menu_principal()

if __name__ == "__main__":
    main()
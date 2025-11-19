# PROJETO LAVAJATO

Projeto desenvolvido em Python para gerenciar um lavajato

Este repositório contém um sistema simples de gerenciamento de um lava-jato escrito em Python. O objetivo é facilitar o controle de clientes, veículos, agendamentos e tipos de lavagem através de arquivos JSON e scripts organizados em módulos. Funcionalidades principais:

    Cadastro e listagem de clientes
    Cadastro e listagem de veículos
    Criação e edição de agendamentos
    Gestão de tipos de lavagem e preços

Estrutura básica:

    Arquivos principais: main.py, sistema_lava_jato.py e scripts auxiliares
    Dados persistidos em: clientes.json, carros.json, agendamentos.json, tipos_lavagem.json

Como executar:

    Certifique-se de ter Python 3 instalado.
    Execute python3 main.py ou python main.py na raiz do projeto.

O projeto é leve e destinado a estudos e pequenos usos locais. Contribuições são bem-vindas — abra uma issue ou um pull request com melhorias.

Entidades e atributos
---------------------

As entidades principais do sistema e seus atributos (conforme os scripts no projeto) são:

- Cliente (`clientes`)
    - `id` (inteiro): Identificador único do cliente
    - `nome` (string): Nome completo do cliente
    - `telefone` (string): Telefone de contato
    - `email` (string): Endereço de e-mail

- Carro (`carros`)
    - `id` (inteiro): Identificador único do carro
    - `id_cliente` (inteiro): Referência ao `id` do cliente proprietário
    - `modelo` (string): Modelo do veículo
    - `marca` (string): Marca do veículo
    - `placa` (string): Placa do veículo
    - `ano` (string/integer): Ano do veículo
    - `cor` (string): Cor do veículo (usado em listagens; pode não estar presente em todas as entradas)

- Tipo de Lavagem (`tipos_lavagem`)
    - `id` (inteiro): Identificador do tipo de serviço
    - `descricao` (string): Nome/descrição do serviço (ex.: 'Completa')
    - `preco` (float): Preço do serviço
    - `tempo_medio` (string): Duração estimada do serviço (ex.: '30min')

- Agendamento (`agendamentos`)
    - `id` (inteiro): Identificador do agendamento
    - `id_cliente` (inteiro): Referência ao cliente
    - `id_carro` (inteiro): Referência ao carro
    - `id_lavagem` (inteiro): Referência ao tipo de lavagem
    - `data` (string): Data no formato DD/MM/AAAA
    - `hora` (string): Hora no formato HH:MM
    - `status` (string): Estado do agendamento (ex.: 'Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado')

Observações:
- Os dados são atualmente persistidos em JSON e alguns módulos gravam/lerem dados em formatos de texto (por exemplo, linhas com separador `|`), então as estruturas podem variar levemente entre arquivos.
- Recomenda-se padronizar o armazenamento e validar os campos ao ler/escrever para garantir integridade.
# Monitoramento de Sensores com Flask

Este projeto é uma aplicação web desenvolvida com Flask, que permite monitorar e visualizar dados de sensores, como temperatura, corrente e vibração. A aplicação utiliza um banco de dados SQLite para armazenar os dados coletados, além de fornecer uma interface amigável para o usuário.

## Funcionalidades

- **Visualização de Dados**: Permite que os usuários vejam os dados dos sensores em tempo real.
- **Gráficos de Dados**: Os dados são apresentados em gráficos que facilitam a análise visual.
- **Cadastro de Usuários**: Os usuários podem se cadastrar e fazer login para acessar a aplicação.
- **Consultas de Dados**: Permite consultar dados por dia, semana, mês ou ano.

## Tecnologias Utilizadas

- **Flask**: Framework web em Python.
- **Flask-SQLAlchemy**: ORM para manipulação do banco de dados.
- **Flask-Migrate**: Para gerenciamento de migrações do banco de dados.
- **SQLite**: Banco de dados utilizado para armazenamento de dados.
- **Werkzeug**: Para segurança na manipulação de senhas.
- **HTML/CSS**: Para reenderizar e deixar as paginas web bonitas.

## Instalação

1. Clone o repositório:

   ```bash
   git clone https://github.com/gabsakura/IA-challenge-update_test-main.git
   cd IA-challenge-update_test-main
2. Instale as dependências:

  ```bash

    pip install -r requirements.txt

3. Execute a aplicação
    ```bash
    
    python app.py

A aplicação estará disponível em http://127.0.0.1:5001.

## Screenshots do Projeto

Aqui estão algumas capturas de tela do projeto:

| ![Descrição da Imagem 1](caminho/para/screenshot1.png) | ![Descrição da Imagem 2](caminho/para/screenshot2.png) | ![Descrição da Imagem 3](caminho/para/screenshot3.png) |
|:--:|:--:|:--:|
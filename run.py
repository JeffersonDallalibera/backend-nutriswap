from app import create_app

# Criação da instância da aplicação Flask
app = create_app()

if __name__ == "__main__":
    # Inicia o servidor em modo de depuração
    app.run(debug=True, host='0.0.0.0', port=5000)

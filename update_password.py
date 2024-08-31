from app import create_app
from app.extensions import db
from app.models.usuarios import Usuario
from werkzeug.security import generate_password_hash

# Cria a aplicação Flask e empurra o contexto do aplicativo
app = create_app()
app.app_context().push()


def update_password_hashes():
    print('Updating password hashes...')
    # Obtém todos os usuários do banco de dados
    users = Usuario.query.all()

    # Itera sobre cada usuário
    for user in users:
        # Se a senha ainda não está hashada, atualize
        if len(user.senha) < 60:  # Ajuste esse valor conforme necessário
            hashed_password = generate_password_hash(user.senha)
            user.senha = hashed_password
            db.session.commit()
            print(f'Password for user {user.username} updated to hashed version.')


if __name__ == '__main__':

    update_password_hashes()

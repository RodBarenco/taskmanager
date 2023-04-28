import hashlib
from models.db_models import User

def login(session, username, password):
    try:
        user = session.query(User).filter_by(username=username).first()
        if user is not None:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if hashed_password == user.password:
                return {'success': True, 'message': 'Conexão aceita!', 'user_id': user.id}
            else:
                return {'success': False, 'message': 'Senha incorreta.'}
        else:
            return {'success': False, 'message': 'Usuário não encontrado.'}
    except:
        return {'success': False, 'message': 'Erro ao realizar login.'}


def register(session, new_username, new_password):
    try:
        hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
        user = User(username=new_username, password=hashed_new_password)
        session.add(user)
        session.commit()
        return {'success': True, 'message': 'Usuário registrado com sucesso!', 'user_id': user.id}, user
    except:
        session.rollback()
        return {'success': False, 'message': 'Erro ao registrar usuário.'}, None
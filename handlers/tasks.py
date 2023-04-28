from datetime import datetime
from models.db_models import Task
from handlers.session import SESSION
from kivy.uix.label import Label
from sqlalchemy.exc import SQLAlchemyError
       
def add_task(color, deadline, title, text, user_id):
    try:
        SESSION.add(Task(
            title=title,
            date_of_insertion=datetime.now(),
            date_to_conclude=datetime.strptime(deadline, "%d/%m/%Y").date(),
            text=text,
            concluded=False,
            trashed=False,
            user_id=user_id,
            color=color
        ))
        SESSION.commit()
        return {'success': True, 'message': '\n TAREFA SALVA COM SUCESSO! \n \n >>>>>>>>>>>>>>>>> \n \n'}
    except SQLAlchemyError as e:
        print(e)
        SESSION.rollback()
        return {'success': False, 'error': '\n OCORREU UM ERRO - TAREFA NÃO SALVA! \n \n>>>>>>>>>>>>>>\n \n'}

def delete_task(task_id):
    SESSION.query(Task).filter(Task.id == task_id).update({"trashed": True})
    SESSION.commit()

def recover_task(task_id):
    SESSION.query(Task).filter(Task.id == task_id).update({"trashed": False, "concluded": False})
    SESSION.commit()

def conclude_task(task_id):
    SESSION.query(Task).filter(Task.id == task_id).update({"concluded": True})
    SESSION.commit()

def delete_permanently(task_id):
    SESSION.query(Task).filter(Task.id == task_id).delete()
    SESSION.commit()

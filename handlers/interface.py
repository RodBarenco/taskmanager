from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from models.db_models import User
from handlers.login import login, register
from sqlalchemy.exc import IdentifierError as dbError
from assets.kv_classes.kv_commons import Sbutton as RoundedButton
from handlers.tasks import add_task_widget, add_task
import traceback
from datetime import datetime

class LoginInterface(Screen):

    def __init__(self, **kwargs):
        Screen.__init__(self, **kwargs)
        
    def call_login(self, session, username, password, screen_manager):
        try:
            result = login(session, username, password)
            if result['success']:
                print(result['message'])
                
                return result
            else:
                # Exibir mensagem de erro na tela de login
                print(result['message'])
                return result

        except AttributeError as e:
            print(f"Erro de atributo: {e}")
            print(traceback.print_exc())

    def call_register(self, session, new_username, new_password, screen_manager):
        try:            
            result, user = register(session, new_username, new_password)
            if result['success']:
                print(result['message'])
                # Login bem sucedido, navegar para a próxima tela

            else:
                # Exibir mensagem de erro na tela de login
                print(result['message'])
                print(traceback.print_exc())
                session.rollback()
                print(dbError)

        except AttributeError as e:
            print(f"Erro de atributo: {e}")
            print(traceback.print_exc ())

class Tasklist(Screen):
    def __init__(self, session, **kwargs):
        self.session = session

        super(Tasklist, self).__init__(**kwargs)
    
    def call_add_task(self, color, deadline, title, text, user_id):
        deadline_datetime = datetime.strptime(deadline, '%d/%m/%Y').date()
        colors_allowed = ["vermelha", "amarela", "verde"]
        
        if deadline_datetime < datetime.now().date():
            current_date = datetime.now().strftime("%d/%m/%Y")    
            raise ValueError(f"O prazo deve ser no mínimo a data atual ({current_date}).")
        elif color.lower() not in colors_allowed:
            raise ValueError("A cor da tarefa deve ser vermelha, amarela ou verde. Com letras minúsculas.")
        elif not title:
            raise ValueError("O título da tarefa não pode estar vazio.")
        else:
            try:
                result = add_task(color, deadline, title, text, user_id)
                if result['success']:
                    print(result['message'])
                else:
                    print(result['error'])       
            except:
                print(traceback.print_exc ())



 



        

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from models.db_models import User, Task
from handlers.interface import LoginInterface, Tasklist
from handlers.session import SESSION
from handlers.tasks import delete_permanently, delete_task, recover_task, conclude_task
from datetime import datetime
import traceback

# criando telas
Builder.load_file('screens/login.kv')
Builder.load_file('screens/landing_page.kv')
Builder.load_file('screens/newtask.kv')
Builder.load_file('screens/trash.kv')
Builder.load_file('screens/concluded.kv')
Builder.load_file('screens/task_viwe.kv')

# função para buscar a lista de tarefas refente ao usuário logado
def add_list(session, logged_user):
    try:
        user = session.query(User).filter_by(id=logged_user).one()
        tasks = user.tasks
        if not tasks:
            print(f'Nenhuma tarefa encontrada.')
        for t in tasks:
            print(f'task id: {t.id} - task color: {t.color} ')
        return tasks
    except AttributeError as e:
        print(f"Erro de atributo: {e}")

# tela de login e registro
class Login(Screen):
    pass

# página principal após a tela de login
class LandingPage(Screen):
    def __init__(self, tasks, **kwargs):
        super().__init__(**kwargs)
        self.tasks = tasks
        self.selected_id = None

        class Task(BoxLayout):
            def __init__(self, text = '', name = 'oi tudo bem?', **kwargs):
                super().__init__(**kwargs)
                self.ids.taskmodel.text = text
                self.name = name
                self.bind(on_press=self.on_viwe)
                self.bind(on_press=self.on_delete)
                self.bind(on_press=self.on_conclude)
            def on_viwe (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> Id da tarefa visualizada:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id

            def on_delete (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> Id da tarefa deletada:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
            
            def on_conclude (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> Id da tarefa concluída:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
        
        self.tasklabel = Task()

        print(f'tarefas enviadas para landing page: \n --> {tasks} \n \n')

        sorted_tasks = sorted(tasks, key=lambda task: task.date_to_conclude)
        for task in sorted_tasks:
            if not task.concluded and not task.trashed and task.date_to_conclude.date() >= datetime.now().date():   
                try:
                    print('tarefa recebida!')
                    title = task.title
                    task_id = str(task.id)
                    date_to_conclude = task.date_to_conclude.strftime("%d/%m/%Y")
                    textlabel = (f'Tarefa: {title} - previsão para: {date_to_conclude}')
                    print(f'Label a ser adicionado: {textlabel}')
                    if task.color == 'vermelha':
                        self.ids.red.add_widget(Task(text = textlabel, name = task_id), index = 0)
                        print('Tarefa urgente adicionada na tela!')
                    elif task.color == 'amarela':
                        self.ids.yellow.add_widget(Task(text = textlabel, name = task_id), index = 0)
                        print('Tarefa necessária adicionada na tela!')
                    elif task.color == 'verde':
                        self.ids.green.add_widget(Task(text = textlabel, name = task_id), index = 0)
                        print('Tarefa "outras tarefas" adicionada na tela!')
                except:
                    print(traceback.format_exc())
    
    def on_new_task(self):
        self.manager.current = 'newtask'
        
    def on_trash (self):
        self.manager.current = 'trash'
        
    def on_concluded (self):
        self.manager.current = 'concluded'

# tela relativa a visualização de uma tarefa específica    
class TaskViwe(Screen):
    def __init__(self, task, **kwargs):
        super().__init__(**kwargs)
        self.task = task
        self.ids.title_viwe.text = self.task.title
        self.ids.data_in_viwe.text = self.task.date_of_insertion.strftime('%d/%m/%Y')
        self.ids.data_viwe.text = self.task.date_to_conclude.strftime('%d/%m/%Y')
        self.ids.color_viwe.text = self.task.color
        self.ids.task_viwe.text = self.task.text

    def on_viwe_back (self):
        self.manager.current = 'landing'
        self.manager.remove_widget(self)
    
    def on_viwe_delete(self):
        task_id = self.task.id
        print(f'\n id da tarefa a ser deletada: >>>>>>>>>>>>>>>{task_id}\n\n')
        delete_permanently(task_id)
        
    def on_viwe_conclude(self):
        task_id = self.task.id
        print(f'\n id da tarefa a ser concluída: >>>>>>>>>>>>>>>{task_id}\n\n')
        conclude_task(task_id)

# tela relativa a tarefas jogadas no lixo
class Trash(Screen):
    def __init__(self, tasks, **kwargs):
        super().__init__(**kwargs)
        self.tasks = tasks
        self.selected_id = None

        class TrashedTask(BoxLayout):
            def __init__(self, text = '', name = 'oi tudo bem?', **kwargs):
                super().__init__(**kwargs)
                self.ids.taskmodelt.text = text
                self.name = name
                self.bind(on_press=self.on_delete)
                self.bind(on_press=self.on_restore)
            def on_delete (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> TAREFA DELETADA:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
            def on_restore (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> TAREFA RESTAURADA:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
        
        self.tasklabeltrashed = TrashedTask()

        sorted_tasks = sorted(tasks, key=lambda task: task.date_to_conclude)
        for task in sorted_tasks:
            if not task.concluded and task.trashed == True or task.date_to_conclude.date() < datetime.now().date(): 
                try:
                    title = task.title
                    task_id = str(task.id)
                    date_to_conclude = task.date_to_conclude.strftime("%d/%m/%Y")
                    textlabel = (f'Tarefa: {title} - previsão para: {date_to_conclude}')
                    print(f'Label a ser adicionado: {textlabel}')
                    self.ids.trashed_tasks.add_widget(TrashedTask(text = textlabel, name = task_id), index = 0)
                    print('Tarefa adicionada no lixo!')
                except:
                    print(traceback.format_exc())

    def on_task (self):
        self.manager.current = 'landing'
    
    def on_concluded (self):
        self.manager.current = 'concluded'

# tela para as tarefas que foram concluídas        
class Concluded(Screen):
    def __init__(self, tasks, **kwargs):
        super().__init__(**kwargs)
        self.tasks = tasks
        self.selected_id = None

        class ConcludedTask(BoxLayout):
            def __init__(self, text = '', name = 'oi tudo bem?', **kwargs):
                super().__init__(**kwargs)
                self.ids.taskmodelt.text = text
                self.name = name
                self.bind(on_press=self.on_concluded_delete)
                self.bind(on_press=self.on_concluded_viwe)
                self.bind(on_press=self.on_concluded_restore)

            def on_concluded_delete (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> TAREFA DELETADA:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
            def on_concluded_viwe (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> VER TAREFA:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
            def on_concluded_restore (self, *args):
                self.selected_id = self.name
                print(f'\n >>>> RESTAURAR TAREFA:{self.selected_id} \n')
                self.parent.parent.parent.parent.selected_id = self.selected_id
        
        self.tasklabelconcluded = ConcludedTask()

        sorted_tasks = sorted(tasks, key=lambda task: task.date_to_conclude)
        for task in sorted_tasks:
            if task.concluded == True:
                try:
                    title = task.title
                    task_id = str(task.id)
                    date_to_conclude = task.date_to_conclude.strftime("%d/%m/%Y")
                    textlabel = (f'Tarefa: {title} - previsão para: {date_to_conclude}')
                    print(f'Label a ser adicionado: {textlabel}')
                    self.ids.concluded_tasks.add_widget(ConcludedTask(text = textlabel, name = task_id), index = 0)
                    print('Tarefa adicionada em concluídas!')
                except:
                    print(traceback.format_exc())

    def on_task (self):
        self.manager.current = 'landing'
        
    def on_trash (self):
        self.manager.current = 'trash'    

# tela para criação de novas tarefas    
class NewTask(Screen):
    def cancel(self):
        self.manager.current = 'landing'
    def reset(self):
        self.ids.task_title.text = ''
        self.ids.data_input.text = ''
        self.ids.cor_input.text = ''
        self.ids.descricao_input.text = ''
    pass

# transição
class Transition(Screen):
    pass

# O app em sí que instancia todas as classes, e conta com as diversas funções relativas as interações com botões
class TestApp(App):
    session = SESSION
    login_interface = LoginInterface()
    landing_page = LandingPage(name='landing', tasks=[])
    trash = Trash(name = 'trash', tasks=[])
    concluded = Concluded(name = 'concluded', tasks=[])
    newtask = NewTask(name = 'newtask')
    task_list = Tasklist(session)
    
    def __init__(self, **kwargs):
        super(TestApp, self).__init__(**kwargs)
        self.logged_user = None

    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(Login(name='login'))
        return sm
    
    #login and register functions
    def call_login(self, username, password):
        try:
            result = self.login_interface.call_login(self.session, username, password, self.root)
            if result['success']:
                self.logged_user = result['user_id']
                print(result)
                try:
                    tasks = add_list(self.session, self.logged_user)
                    self.landing_page = LandingPage(name='landing', tasks=tasks)
                    self.root.add_widget(self.landing_page)
                    self.root.current = 'landing'
                    self.root.add_widget(self.newtask)
                    self.concluded = Concluded(name = 'concluded', tasks=tasks)
                    self.root.add_widget(self.concluded)
                    self.trash = Trash(name = 'trash', tasks=tasks)
                    self.root.add_widget(self.trash)
                    print(f'widgets adicionados {self.trash} - {self.landing_page} - {self.concluded} - {self.newtask}')
                except:
                    print(traceback.format_exc())
            else:
                print(traceback.format_exc())
        except:
            print(traceback.format_exc())

    def call_register(self, new_username, new_password):
        try:
            self.login_interface.call_register(self.session, new_username, new_password, self.root)
        except AttributeError as e:
            print(f"Erro de atributo: {e}")

    #task related functions
    def call_add_task(self, cor_input, data_input, task_title, descricao_input):
        print(f'\n COR: {cor_input}, CONCLUSÃO: {data_input}, TÍTULO {task_title}, TEXTO: {descricao_input} USUÁRIO: {self.logged_user} \n')
        try:
            self.task_list.call_add_task(cor_input, data_input, task_title, descricao_input, self.logged_user)
            tasks = add_list(self.session, self.logged_user)
            print(f'\n novo conjunto de tarefas: \n \n >>>>>>>>>>>>>>>>>>>>>>>>\n {tasks} \n \n')
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.root.current = 'landing'
            self.newtask.reset()
        except:
            print(traceback.format_exc())

    def call_on_viwe (self):
        task_id = self.landing_page.selected_id
        if task_id is not None:
            task = self.session.query(Task).filter(Task.id == task_id).one()
            self.task_viwe = TaskViwe(name='viwe', task=task)
            self.root.add_widget(self.task_viwe)
            self.root.current = 'viwe' 

    def on_delete_permanently(self):
        task_id = self.trash.selected_id
        print(f'essa tarefa foi passada para ser deletada >>>>>>> {task_id}')
        if task_id is not None:
            delete_permanently(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.trash)
            self.trash = Trash(name='trash', tasks=tasks)
            self.root.add_widget(self.trash)
            self.root.current = 'trash'
            self.root.remove_widget(self.null)
    
    def call_on_delete(self):
        task_id =  self.landing_page.selected_id
        print(f'essa tarefa foi passada para ser mandada para o lixo >>>>>>> {task_id}')
        if task_id is not None:
            delete_task(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.root.remove_widget(self.trash)
            self.trash = Trash(name = 'trash', tasks=tasks)
            self.root.add_widget(self.trash)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.root.current = 'landing'
            self.root.remove_widget(self.null)

    def call_on_restore(self):
        task_id = self.trash.selected_id
        print(f'essa tarefa foi passada para ser restaurada >>>>>>> {task_id}')
        if task_id is not None:
            recover_task(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.trash)
            self.trash = Trash(name = 'trash', tasks=tasks)
            self.root.add_widget(self.trash)
            self.root.current = 'trash'
            self.root.remove_widget(self.null)
    
    def call_on_conclude(self):
        task_id = self.landing_page.selected_id
        print(f'essa tarefa foi passada para ser concluida >>>>>>>> {task_id}')
        if task_id is not None:
            conclude_task(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.root.remove_widget(self.concluded)
            self.concluded = Concluded(name = 'concluded', tasks=tasks)
            self.root.add_widget(self.concluded)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.root.current = 'landing'
            self.root.remove_widget(self.null)
    
    def call_on_concluded_restore(self):
        task_id = self.concluded.selected_id
        print(f'essa tarefa será restaurada >>>>>>>>>>>>>>>>> {task_id}')
        if task_id is not None:
            recover_task(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.concluded)
            self.concluded = Concluded(name = 'concluded', tasks=tasks)
            self.root.add_widget(self.concluded)
            self.root.current = 'concluded'
            self.root.remove_widget(self.null)
    
    def on_concluded_delete_permanently(self):
        task_id = self.concluded.selected_id
        print(f'essa tarefa será deletada permanentemente >>>>>>>>>>>>>>>>> {task_id}')
        if task_id is not None:
            delete_permanently(task_id)
            tasks = add_list(self.session, self.logged_user)
            self.root.remove_widget(self.landing_page)
            self.landing_page = LandingPage(name='landing', tasks=tasks)
            self.root.add_widget(self.landing_page)
            self.null = Transition(name='null')
            self.root.add_widget(self.null)
            self.root.current = 'null'
            self.root.remove_widget(self.concluded)
            self.concluded = Concluded(name = 'concluded', tasks=tasks)
            self.root.add_widget(self.concluded)
            self.root.current = 'concluded'
            self.root.remove_widget(self.null)
    
    def call_on_concluded_viwe (self):
        task_id = self.concluded.selected_id
        if task_id is not None:
            task = self.session.query(Task).filter(Task.id == task_id).one()
            self.task_viwe = TaskViwe(name='viwe', task=task)
            self.root.add_widget(self.task_viwe)
            self.root.current = 'viwe'

    def call_on_viwe_delete(self):
        tasks = add_list(self.session, self.logged_user)  
        self.root.remove_widget(self.landing_page)
        self.landing_page = LandingPage(name='landing', tasks=tasks)
        self.root.add_widget(self.landing_page)
        self.root.current = 'landing'
        self.root.remove_widget(self.task_viwe)

    def call_on_viwe_conclude(self):
        tasks = add_list(self.session, self.logged_user)  
        self.root.remove_widget(self.landing_page)
        self.landing_page = LandingPage(name='landing', tasks=tasks)
        self.root.add_widget(self.landing_page)
        self.root.current = 'landing'
        self.root.remove_widget(self.concluded)
        self.concluded = Concluded(name= 'concluded', tasks=tasks)
        self.root.add_widget(self.concluded)
        self.root.remove_widget(self.task_viwe)    

if __name__ == '__main__':
    TestApp().run()

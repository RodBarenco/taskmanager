1 – Disclaimer: 
    Esse foi o meu primeiro contato com a biblioteca Kivy. Não segui nenhum projeto existente, portanto parti do zero. 
    Se fizesse esse projeto novamente com certeza faria algumas alterações que diminuiriam sua complexidade e trariam as mesmas funcionalidades.
    Quanto ao trabalho com linguagem python, eu ainda estou me desenvolvimento na mesma  portanto as soluções aqui apresentadas não são ótimas.
    Sintam-se confortáveis para colaborar, e dar palpites sobre o que deve ser melhorado nesse pequeno projeto.

2 – Bibliotecas: 
    As bibliotecas externas ao Python 3 que você deverá instalar para que esse projeto funcione são:
    SQLAlchemy 2.0.5.post1 – para manipulação do banco de dados ( no caso o SQLite )
    e Kivy 2.1.0 usado para a interface gráfica.

    SQLAlchemy - The Database Toolkit for Python - https://www.sqlalchemy.org/
    Kivy: Cross-platform Python Framework for GUI apps Development - https://kivy.org/

3 – 
    O App e suas funcionalidades: Nesse app você pode fazer um registro com nome e senha, e efetuar um login através da tela inicial. 
    Após o login você estará na tela inicial onde suas tarefas estarão dividas em 3 áreas roláveis, uma para tarefas urgentes,
    outra para tarefas necessárias e uma para “outras tarefas” nessa tela você ainda tem na parte superior 3 botões, 
    um marcado que indica a página que você está, um para ir até a aba das tarefas concluídas e outro para ir até o lixo onde ficam as tarefas 
    que você tenha jogado fora.
    Na parte inferior você poderá observar um botão que leva o usuário a página de criação de tarefas. 
    As tarefas na página são apresentadas com seu título e a data limite para sua conclusão. 
    Um botão “ver” que leva o usuário a uma tela em que ele consegue observar mais detalhes sobre a tarefa. 
    Ainda conta com um botão para a conclusão e outro para joga-la no lixo.
    Na página de tarefas concluídas o usuário pode excluir as atarefas permanentemente, 
    tem a opção de ver como na página anterior e também pode restaurar a tarefa para página principal ( desde que essa não tenha passada da data de sua conclusão,         nesse caso a tarefa irá para o lixo).
    Na tela relativa as tarefas jogas fora ou que passaram da data de sua conclusão o usuário pode deletar as tarefas permanentemente ou restaura-las.

4 – 
    Estrutura do projeto: Esse projeto conta com os seguintes diretórios:
    - assets, handlers, models, screens que estão dentro do diretório principal TASKMANAGER  onde também estão:
    main.py e onde será gerado o banco de dados tasks.db se ele ainda não existir.
    
    No diretório assets você vai encontrar um arquivo png que corresponde a imagem do fundo da tela de login e também outro diretório chamado kv_classes com um
    arquivo chamado kv_commons.py,
    onde são criadas classes kv personalizadas para serem usadas no restante do projeto.

    No diretório handlers você vai encontrar 4 arquivos python, interface.py ( que eu não criaria novamente pois aumentou a complexidade do projeto sem 
    benefício claro, ele foi uma tentativa ge gerenciar a relação entre as telas e a chamadas de funções referentes aos arquivos .kv), 
    você também vai encontrar o arquivo login.py com as funções referentes ao registro de usuário e login,
    o arquivo session.py que cria o banco de dados e também faz a conexão com o mesmo através de uma sessão e o arquivo tasks.py que contem funções que
    manipulam o banco de dados no que diz respeito as tarefas.
    
    No diretório models está o arquivo db_models.py que tem o modelo do banco de dados com usuário, tarefas e suas relações.
    No diretório screens você vai encontrar uma série de arquivos kv referentes a cada uma das telas do app: concluded.kv para a tela das tarefas concluídas, 
    landin_page.kv para a página principal que aparece logo após o usuário efetuar o login, login.kv referente a tela de login,
    newtask.kv referente a página de criação de tarefas, task_viwe.kv para a visualização das tarefas e trash.kv referente a tela de tarefas jogadas fora.

5 – 
    Futuras melhoras em funcionalidades: 
    Adicionar a possibilidade de edição das tarefas na página de visualização da mesma.
    Na pagina de criação de tarefas modificar o modo de seleção de cor de escrita para um box de escolha.


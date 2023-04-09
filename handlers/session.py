from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.db_models import Base
# criando se não existir e se conectando ao banco de dados
engine = create_engine('sqlite:///tasks.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
SESSION = Session()

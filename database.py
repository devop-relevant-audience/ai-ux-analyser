from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "postgresql+psycopg://postgres:12345@localhost:5432/ai_page_ux_analyzer"

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
  SQLModel.metadata.create_all(engine)

def get_session():
  with Session(engine) as session:
    yield session
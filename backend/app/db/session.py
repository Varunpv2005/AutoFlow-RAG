from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from .models import Base, File as DBFile, ChatHistory
import os

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/chatrag.db"))
CHROMA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/chroma_db"))
os.makedirs(CHROMA_PATH, exist_ok=True)

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def _sqlite_type_name(column) -> str:
    from sqlalchemy import Integer, String, Text, Float, DateTime, Boolean
    if isinstance(column.type, Integer):
        return "INTEGER"
    if isinstance(column.type, String):
        return f"VARCHAR({column.type.length or 255})"
    if isinstance(column.type, Text):
        return "TEXT"
    if isinstance(column.type, Float):
        return "FLOAT"
    if isinstance(column.type, DateTime):
        return "DATETIME"
    if isinstance(column.type, Boolean):
        return "BOOLEAN"
    return "TEXT"


def _ensure_sqlite_columns_for_model(model):
    if engine.dialect.name != "sqlite":
        return

    table_name = model.__tablename__
    with engine.begin() as conn:
        table_exists = conn.execute(text(f'PRAGMA table_info("{table_name}")')).fetchall()
        if not table_exists:
            Base.metadata.create_all(bind=engine, tables=[model.__table__])
            return

        existing_columns = {row[1] for row in table_exists}
        for column in model.__table__.columns:
            if column.name in existing_columns:
                continue

            column_sql = _sqlite_type_name(column)
            if not column.nullable and not column.primary_key:
                column_sql += " NOT NULL"

            default_sql = ""
            if column.default is not None:
                default_value = getattr(column.default, "arg", None)
                if default_value is not None and not callable(default_value):
                    if isinstance(default_value, str):
                        default_sql = f" DEFAULT '{default_value}'"
                    else:
                        default_sql = f" DEFAULT {default_value}"

            conn.execute(text(f'ALTER TABLE "{table_name}" ADD COLUMN "{column.name}" {column_sql}{default_sql}'))


def _ensure_sqlite_schema():
    Base.metadata.create_all(bind=engine)
    _ensure_sqlite_columns_for_model(DBFile)
    _ensure_sqlite_columns_for_model(ChatHistory)


def init_db():
    try:
        _ensure_sqlite_schema()
        try:
            from app.log_utils import safe_log_gotcha
            safe_log_gotcha("[init_db] Database initialized successfully.")
        except ImportError:
            print("[init_db] Database initialized successfully.")
    except Exception as e:
        try:
            from app.log_utils import safe_log_gotcha
            safe_log_gotcha(f"[init_db] Database initialization failed: {e}")
        except ImportError:
            print(f"[init_db] Database initialization failed: {e}")
        raise

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

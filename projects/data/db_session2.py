from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class YourModel(Base):
    __tablename__ = 'your_model'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    created_at = Column(DateTime)


class DatabaseSingleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DatabaseSingleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, db_uri, pool_size=5, max_overflow=10, autocommit=False, autoflush=True):
        if not hasattr(self, "_initialized"):
            self.db_uri = db_uri
            self.pool_size = pool_size
            self.max_overflow = max_overflow
            self.autocommit = autocommit
            self.autoflush = autoflush
            self._engine = None
            self._session_maker = None
            self._initialized = True

    def create_engine(self):
        if self._engine is None:
            self._engine = create_engine(
                self.db_uri,
                pool_size=self.pool_size,
                max_overflow=self.max_overflow,
                echo=False  # Set to True for debugging SQL queries
            )
        return self._engine

    def create_session(self):
        if self._session_maker is None:
            self._session_maker = sessionmaker(
                bind=self.create_engine(),
                autocommit=self.autocommit,
                autoflush=self.autoflush,
                expire_on_commit=False
            )
        return self._session_maker

    def get_session(self):
        return self.create_session()


# Example usage:
if __name__ == "__main__":
    db_uri = "sqlite:///example.db"
    db_singleton = DatabaseSingleton(db_uri)
    session = db_singleton.get_session()

    try:
        # Perform database operations using the session
        # For example:
        # new_object = YourModel(name="example", created_at=datetime.now())
        # session.add(new_object)
        # session.commit()
        pass
    except Exception as e:
        session.rollback()
        print("Error:", e)
    finally:
        session.close()
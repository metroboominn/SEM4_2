from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine  
from sqlalchemy.orm import sessionmaker, declarative_base            
from dotenv import load_dotenv                                        
import os                                                             

load_dotenv()                                                        # Загружаем переменные окружения из файла .env
DATABASE_URL = os.getenv("DATABASE_URL")                            

engine = create_async_engine(DATABASE_URL, echo=False)              # Создаем асинхронный движок SQLAlchemy для БД
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)  # Фабрика сессий БД
Base = declarative_base()                                           # Базовый класс для описания моделей

# Асинхронная функция-зависимость для получения сессии БД в роутерах
async def get_db():
    async with SessionLocal() as session:                          
        yield session                                               

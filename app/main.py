from fastapi import FastAPI                        
from app.db import Base, engine                    
from app.routes import router                       

app = FastAPI()                                    # Создаем экземпляр FastAPI — наше веб-приложение

# Событие при старте приложения — создаем таблицы, если их нет
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:             # Открываем асинхронное соединение с базой
        await conn.run_sync(Base.metadata.create_all)  # Создаем все таблицы, описанные в моделях

app.include_router(router)                         # Подключаем роутер с маршрутизатором к приложению

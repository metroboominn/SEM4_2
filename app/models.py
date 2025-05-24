from sqlalchemy import Column, Integer, String, Boolean, ForeignKey  
from sqlalchemy.orm import relationship                              
from app.db import Base                                             

class TodoList(Base):
    __tablename__ = "todolists"                                     # Название таблицы в базе данных
    id = Column(Integer, primary_key=True, index=True)               # Поле id — первичный ключ с индексом
    name = Column(String, nullable=False)                            # Название списка дел, обязательное поле

    items = relationship("Item", back_populates="todolist", cascade="all, delete-orphan")
    # Связь "один ко многим" с элементами Item, при удалении списка — удаляются и элементы

class Item(Base):
    __tablename__ = "items"                                         # Таблица для элементов списка дел
    id = Column(Integer, primary_key=True, index=True)               # ID элемента — первичный ключ
    name = Column(String, nullable=False)                            # Название элемента обязательно
    text = Column(String, nullable=True)                             
    is_done = Column(Boolean, default=False)                         
    todolist_id = Column(Integer, ForeignKey("todolists.id"))        # Внешний ключ на таблицу todolists

    todolist = relationship("TodoList", back_populates="items")     # Обратная связь с TodoList

from pydantic import BaseModel, Field  
from typing import Optional  


#Схемы для TodoList


class TodoListBase(BaseModel):
    # Базовая схема для списка дел с полем 'name'.
    # Используется как основа для создания и обновления данных.
    name: str = Field(..., example="Мои задачи")
    # Поле 'name' обязательное
    # example — пример значения для документации API.


class TodoListCreate(TodoListBase):
    pass
    # Схема для создания нового списка дел.
    # Наследуется от TodoListBase, ничего не добавляет — просто для семантики.


class TodoListUpdate(BaseModel):
    # Схема для обновления списка дел.
    # Все поля необязательные, так как обновление может быть частичным.
    name: Optional[str] = Field(None, example="Обновленное имя")
    # Поле 'name' опционально (может отсутствовать в запросе).


class TodoListInDB(TodoListBase):
    # Схема, которая возвращается клиенту с данными из базы.
    # Включает обязательное поле 'id' — уникальный идентификатор списка.
    id: int = Field(..., example=1)


#Схемы для Item


class ItemBase(BaseModel):
    # Базовая схема для элемента списка дел.
    name: str = Field(..., example="Купить молоко")
    text: str = Field(..., example="Пойти в магазин и купить молоко")
    is_done: bool = Field(False, example=False)
    # 'is_done' — флаг, выполнено ли задание, по умолчанию False.


class ItemCreate(ItemBase):
    pass
    # Схема для создания нового элемента.
    # Наследуется от ItemBase, не добавляет новых полей.


class ItemUpdate(BaseModel):
    # Схема для частичного обновления элемента.
    # Все поля необязательные, можно обновить любое из них.
    name: Optional[str] = Field(None, example="Обновленное название")
    text: Optional[str] = Field(None, example="Обновленный текст")
    is_done: Optional[bool] = Field(None, example=True)


class ItemInDB(ItemBase):
    # Схема для данных элемента, которые возвращаются клиенту.
    # Добавлено обязательное поле 'id' — идентификатор элемента.
    id: int = Field(..., example=1)

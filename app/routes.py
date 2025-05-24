from fastapi import APIRouter, Depends, HTTPException, status  
from sqlalchemy.ext.asyncio import AsyncSession                 
from sqlalchemy.future import select                             
from app.db import get_db                                         
from app.models import TodoList, Item                             
from app.schemas import (                                        
    TodoListCreate, TodoListUpdate, TodoListInDB,
    ItemCreate, ItemUpdate, ItemInDB
)

router = APIRouter()                                             
#Создаем роутер — контейнер для всех маршрутов API, чтобы структурировать код.


#CRUD операции для TodoList


@router.post("/todolists/", response_model=TodoListInDB, status_code=status.HTTP_201_CREATED)
async def create_todolist(todolist: TodoListCreate, db: AsyncSession = Depends(get_db)):
    # POST-запрос для создания нового списка дел
    
    new_list = TodoList(name=todolist.name)                      
    # Создаем новый объект TodoList с именем из запроса
    
    db.add(new_list)                                             
    # Добавляем этот объект в текущую сессию (подготовка к записи)
    
    await db.commit()                                            
    # Сохраняем изменения в базе данных
    
    await db.refresh(new_list)                                   
    # Обновляем объект, чтобы получить сгенерированный ID
    
    return new_list                                             
    # Возвращаем созданный объект в ответе


@router.get("/todolists/", response_model=list[TodoListInDB])
async def get_todolists(db: AsyncSession = Depends(get_db)):
    # GET-запрос для получения списка всех списков дел
    
    result = await db.execute(select(TodoList))                  
    # Выполняем запрос на выборку всех TodoList
    
    return result.scalars().all()                                
    # Возвращаем все объекты в виде списка


@router.get("/todolists/{todolist_id}", response_model=TodoListInDB)
async def get_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    # GET-запрос для получения одного списка дел по id
    
    todolist = await db.get(TodoList, todolist_id)               
    # Пытаемся получить объект из базы по ключу
    
    if not todolist:                                             
        raise HTTPException(status_code=404, detail="TodoList not found")
        # Если объект не найден, возвращаем ошибку 404
    
    return todolist                                              


@router.patch("/todolists/{todolist_id}", response_model=TodoListInDB)
async def update_todolist(todolist_id: int, update: TodoListUpdate, db: AsyncSession = Depends(get_db)):
    # PATCH-запрос для частичного обновления списка дел
    
    todolist = await db.get(TodoList, todolist_id)               
    # Получаем объект по id
    
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    
    if update.name is not None:
        todolist.name = update.name                              
        # Если в запросе есть новое имя — обновляем поле
    
    await db.commit()                                            
    
    await db.refresh(todolist)                                   

    return todolist                                             


@router.delete("/todolists/{todolist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todolist(todolist_id: int, db: AsyncSession = Depends(get_db)):
    # DELETE-запрос для удаления списка дел
    
    todolist = await db.get(TodoList, todolist_id)
    # Получаем объект по id
    
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")

    
    await db.delete(todolist)                                   
    
    await db.commit()                                            
    
    return                                                      


#CRUD операции для Item


@router.post("/todolists/{todolist_id}/items/", response_model=ItemInDB, status_code=status.HTTP_201_CREATED)
async def create_item(todolist_id: int, item: ItemCreate, db: AsyncSession = Depends(get_db)):
    # POST-запрос для создания нового элемента внутри списка
    
    todolist = await db.get(TodoList, todolist_id)               
    # Проверяем, существует ли родительский список
    
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")
    
    new_item = Item(name=item.name, text=item.text, is_done=item.is_done, todolist_id=todolist_id)
    # Создаем новый элемент с привязкой к todolist_id
    
    db.add(new_item)                                             
    
    await db.commit()
    
    await db.refresh(new_item)                                   
    
    return new_item                                             


@router.get("/todolists/{todolist_id}/items/", response_model=list[ItemInDB])
async def get_items(todolist_id: int, db: AsyncSession = Depends(get_db)):
    # GET-запрос для получения всех элементов в конкретном списке
    
    result = await db.execute(select(Item).where(Item.todolist_id == todolist_id))
    # Выполняем выборку всех элементов с нужным todolist_id
    
    return result.scalars().all()                                
    # Возвращаем список элементов


@router.get("/items/{item_id}", response_model=ItemInDB)
async def get_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # GET-запрос для получения конкретного элемента по id
    
    item = await db.get(Item, item_id)
    # Получаем объект из базы
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return item                                                  


@router.patch("/items/{item_id}", response_model=ItemInDB)
async def update_item(item_id: int, update: ItemUpdate, db: AsyncSession = Depends(get_db)):
    # PATCH-запрос для обновления конкретного элемента
    
    item = await db.get(Item, item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if update.name is not None:
        item.name = update.name
    if update.text is not None:
        item.text = update.text
    if update.is_done is not None:
        item.is_done = update.is_done
    # Обновляем поля, если они пришли в запросе
    
    await db.commit()
    
    await db.refresh(item)
    
    return item                                                  


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, db: AsyncSession = Depends(get_db)):
    # DELETE-запрос для удаления элемента
    
    item = await db.get(Item, item_id)
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    await db.delete(item)
    
    await db.commit()
    
    return                                                      


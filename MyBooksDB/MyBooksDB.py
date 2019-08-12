import pypyodbc
import os
import DBwork

def addbook(mdbcon):
    print("Введите автора.")
    writer=input()
    print("Введите название.")
    name=input()
    print("Введите год издания.")
    year=input()
    print("Введите количество томов.")
    count=input()
    print("Введите жанр.")
    type=input()
    print("Нужна ли вам эта книга? (1-да,0-нет)")
    need=input()
    print("Введите номер шкафа.")
    shelf=input()
    print("Если вы ввели всё правильно просто нажмите Enter, в ном случае - напишите 'нет'")
    if input()=="нет": addbook(mdbcon)
    else: DBwork.add_book(mdbcon,writer,name,year,count,type,need,shelf)
    print("Готово!")

def addcoll(mdbcon):
    print("Введите название.")
    name=input()
    print("Введите год издания.")
    year=input()
    print("Введите количество томов.")
    count=input()
    print("Введите жанр.")
    type=input()
    print("Нужна ли вам эта книга? (1-да,0-нет)")
    need=input()
    print("Введите номер шкафа.")
    shelf=input()
    print("Если вы ввели всё правильно просто нажмите Enter, в ном случае - напишите 'нет'")
    if input()=="нет": addcol(mdbcon)
    else: a=DBwork.add_collection(mdbcon,name,year,count,type,need,shelf)

    print("Хотите ли вы сразу заполнить список частей этого сборника? (да,нет)")
    if input()=="да":
        addpart(mdbcon,a)
    print("Готово!")

def addpart(mdbcon,c_id="kek"):
    if c_id=="kek":
        print("Найти сборник через id или через поиск? (id,поиск)")
        t=input()
        if t=="id":
            print("Введите ID.")
            c_id=input()
        elif t=="поиск":
            show(mdbcon,"col_parts")
            print("Введите ID.")
            c_id=input()
    while 1:
        print("Введите автора.")
        writer=input()
        print("Введите название.")
        name=input()
        print("Если вы ввели всё правильно просто нажмите Enter, в ном случае - напишите 'нет'")
        if input()=="нет": addpart(mdbcon,c_id)
        else:
            DBwork.add_collection_part(mdbcon,c_id,writer,name)
            print("Ввести ещё часть? (да,нет)")
            if input()=="нет":
                break
    print("Готово!")

def delete(mdbcon,table):
    print("Через id или через поиск? (id,поиск)")
    t=input()
    if t=="id":
        print("Введите ID.")
        id=input()
    elif t=="поиск":
        show(mdbcon,table)
        print("Введите ID.")
        id=input()
    DBwork.delete(mdbcon,table,id)
    print("Готово!")
    
def show(mdbcon,table=None):
    ask=DBwork.search(mdbcon)
    if table!=None:
        ask.a_table(table)
    while 1:
        print("Что вы зннаете о этой записи? (тип,автор,название,год издания,количество томов,жанр,необходимость,шкаф)")
        a=input()
        if a=="тип" and table==None:
            print("Варианты: книга,сборник,часть сборника")
            b=input()
            if b=="книга": ask.a_table("books")
            elif b=="сборник": ask.a_table("collections")
            elif b=="часть сборника": ask.a_table("col_parts")
        elif a=="тип":
            print("Тип уже задан.")
        elif a=="автор":
            ask.a_writer(input())
        elif a=="название":
            ask.a_name(input())
        elif a=="год издания":
            ask.a_year(input())
        elif a=="количество томов":
            ask.a_count(input())
        elif a=="жанр":
            ask.a_type(input())
        elif a=="необходимость":
            print("Варианты: 1,0")
            ask.a_need(input())
        elif a=="шкаф":
            ask.a_shelf(input())
        print("Знаете ли вы что-то ещё? (да,нет)")
        if input()=="нет":
            break
    texty(ask.get_result(),mdbcon)
    print("Готово!")

def texty(result,mdbcon):
    if result.get("books")!=None:
        print("Найденные книги:")
        for a in result["books"]:
            print("\tID: "+str(a[0]))
            print("\tАвтор: "+str(a[1]))
            print("\tНазвание: "+str(a[2]))
            print("\tГод издания: "+str(a[3]))
            print("\tЧисло томов: "+str(a[4]))
            print("\tЖанр: "+str(a[5]))
            print("\tНеобходимость: "+str(a[6]))
            print("\tШкаф: "+str(a[7]))
            print("")
    if result.get("collections")!=None:
        print("Найденные сборники:")
        for a in result["collections"]:
           print("\tID: "+str(a[0]))
           print("\tНазвание: "+str(a[1]))
           print("\tГод издания: "+str(a[2]))
           print("\tЧисло томов: "+str(a[3]))
           print("\tЖанр: "+str(a[4]))
           print("\tНеобходимость: "+str(a[5]))
           print("\tШкаф: "+str(a[6]))
           print("")
    if result.get("col_parts")!=None:
        print("Найденные части сборников:")
        for a in result["col_parts"]:
            print("\tID: "+str(a[0]))
            par_col=DBwork.search(mdbcon)
            print("\tНазвание сборника: "+par_col.open_id("collections",str(a[1]))[0][1])
            print("\tАвтор: "+str(a[2]))
            print("\tНазвание: "+str(a[3]))
            print("")

mdbcon=pypyodbc.win_connect_mdb(os.path.abspath("database.MDB"))

while 1:
    print("Какую задачу необходимо выполнить? (добавить,удалить,смотреть)")
    t=input()
    if t=="добавить":
        print("Что вы хотите добавить? (книга,сборник,часть сборника)")
        at=input()
        if at=="книга":
            addbook(mdbcon)
        elif at=="сборник":
            addcoll(mdbcon)
        elif at=="часть сборника":
            addpart(mdbcon)
    elif t=="удалить":
        print("Что вы хотите удалить? (книга,сборник,часть сборника)")
        at=input()
        if at=="книга":
            delete(mdbcon,"books")
        elif at=="сборник":
            delete(mdbcon,"collections")
        elif at=="часть сборника":
            delete(mdbcon,"col_parts")
    elif t=="смотреть":
        show(mdbcon)

mdbcon.close()
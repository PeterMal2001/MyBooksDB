import pypyodbc,os,sys,DBwork
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.sip import delete

class kekapp(QMainWindow):
    def __init__(self,mdbcon):
        super().__init__()
        self.mainwidget=QWidget()
        self.setCentralWidget(self.mainwidget)
        self.setWindowTitle("Книги")
        self.resize(1100,600)
        self.layout=QGridLayout(self.mainwidget)
        self.setFont(QFont("Arial",15))
        self.show()

        self.mdbcon=mdbcon
        self.types=["проза","поэзия","монография","энциклопедия","справочник","словарь","сборник","научно-популярная литература","периодика","учебник","детская литература"]
        self.widgets=[]
        self.windows=[]
        self.phase="start"

        self.phase_menu()
    
    def phase_menu(self):
        if self.phase!="start":
            self.clean_phase()
        self.phase="menu"

        self.create_btn=QPushButton("Создать запись")
        self.create_btn.setFixedHeight(60)
        self.create_btn.clicked.connect(self.phase_create)
        self.widgets.append(self.create_btn)
        self.layout.addWidget(self.create_btn,1,1,2,10)

        self.open_btn=QPushButton("Открыть запись")
        self.open_btn.setFixedHeight(60)
        self.open_btn.clicked.connect(self.phase_search)
        self.widgets.append(self.open_btn)
        self.layout.addWidget(self.open_btn,3,1,2,10)

        self.settings_btn=QPushButton("Настройки")
        self.settings_btn.setFixedHeight(60)
        self.settings_btn.clicked.connect(self.phase_settings)
        self.widgets.append(self.settings_btn)
        self.layout.addWidget(self.settings_btn,5,1,2,10)

        self.sync_btn=QPushButton("Синхронизация и резервное копирование")
        self.sync_btn.setFixedHeight(60)
        self.sync_btn.clicked.connect(self.phase_sync)
        self.widgets.append(self.sync_btn)
        self.layout.addWidget(self.sync_btn,7,1,2,10)

        self.stats=QLabel("Статистика:\n\nВсего:\n"+str(DBwork.stats(self.mdbcon))+"\nКниг:\n"+str(DBwork.stats(self.mdbcon,"books"))+"\nСборников:\n"+str(DBwork.stats(self.mdbcon,"collections"))+"\nЧастей сборников:\n"+str(DBwork.stats(self.mdbcon,"col_parts")))
        self.stats.setAlignment(Qt.AlignCenter)
        self.widgets.append(self.stats)
        self.layout.addWidget(self.stats,1,14,9,6)
    
    def phase_create(self):
        self.clean_phase()
        self.phase="create"
        self.c_id=None

        self.input_table=QComboBox()
        self.input_table.addItems(["Книга","Сборник","Часть сборника"])
        self.input_table.activated[str].connect(self.create_type_changed)
        self.widgets.append(self.input_table)
        self.layout.addWidget(self.input_table,1,3,1,6)

        self.input_type=QLineEdit()
        completer=QCompleter(self.types,self.input_type)
        self.input_type.setCompleter(completer)
        self.widgets.append(self.input_type)
        self.layout.addWidget(self.input_type,6,15,1,6)

        self.input_need=QComboBox()
        self.input_need.addItems(["Да","Нет"])
        self.widgets.append(self.input_need)
        self.layout.addWidget(self.input_need,7,3,1,4)

        self.input_collection=QLineEdit()
        self.input_collection.setDisabled(True)
        self.input_collection.textChanged[str].connect(self.col_check)
        self.widgets.append(self.input_collection)
        self.layout.addWidget(self.input_collection,2,3,1,20)

        self.input_writer=QLineEdit()
        self.widgets.append(self.input_writer)
        self.layout.addWidget(self.input_writer,4,3,1,20)
        
        self.input_name=QLineEdit()
        self.widgets.append(self.input_name)
        self.layout.addWidget(self.input_name,5,3,1,20)

        self.input_year=QLineEdit()
        self.widgets.append(self.input_year)
        self.layout.addWidget(self.input_year,6,3,1,4)

        self.input_count=QLineEdit()
        self.widgets.append(self.input_count)
        self.layout.addWidget(self.input_count,6,10,1,3)

        self.input_shelf=QLineEdit()
        self.widgets.append(self.input_shelf)
        self.layout.addWidget(self.input_shelf,7,10,1,3)

        self.lbl1=QLabel("Тип")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,1,1,1,2)

        self.lbl2=QLabel("Название сборника")
        self.widgets.append(self.lbl2)
        self.layout.addWidget(self.lbl2,2,1,2,2)

        self.lbl3=QLabel("")
        self.lbl3.setAlignment(Qt.AlignCenter)
        self.lbl3.setMaximumHeight(25)
        self.widgets.append(self.lbl3)
        self.layout.addWidget(self.lbl3,3,3,1,10)

        self.lbl4=QLabel("Автор")
        self.widgets.append(self.lbl4)
        self.layout.addWidget(self.lbl4,4,1,1,2)

        self.lbl5=QLabel("Название")
        self.widgets.append(self.lbl5)
        self.layout.addWidget(self.lbl5,5,1,1,2)

        self.lbl6=QLabel("Год издания")
        self.widgets.append(self.lbl6)
        self.layout.addWidget(self.lbl6,6,1,1,2)

        self.lbl7=QLabel("Количество томов")
        self.widgets.append(self.lbl7)
        self.layout.addWidget(self.lbl7,6,7,1,3)

        self.lbl8=QLabel("Жанр")
        self.widgets.append(self.lbl8)
        self.layout.addWidget(self.lbl8,6,13,1,2)

        self.lbl9=QLabel("Необходимость")
        self.widgets.append(self.lbl9)
        self.layout.addWidget(self.lbl9,7,1,1,2)

        self.lbl10=QLabel("Номер шкафа")
        self.widgets.append(self.lbl10)
        self.layout.addWidget(self.lbl10,7,7,1,3)

        self.back_btn=QPushButton("Назад")
        self.back_btn.clicked.connect(self.phase_menu)
        self.widgets.append(self.back_btn)
        self.layout.addWidget(self.back_btn,12,15,1,4)

        self.create_btn=QPushButton("Создать")
        self.create_btn.clicked.connect(self.create)
        self.widgets.append(self.create_btn)
        self.layout.addWidget(self.create_btn,12,19,1,4)

    def create(self):
        if self.input_need.currentText()=="Да":
            need=1
        else:
            need=0
        
        if self.input_table.currentText()=="Книга":
            DBwork.add_book(self.mdbcon,self.input_writer.text(),self.input_name.text(),self.input_year.text(),self.input_count.text(),self.input_type.text(),need,self.input_shelf.text())
            self.statusBar().showMessage("Запись создана")
            self.input_clean()
        elif self.input_table.currentText()=="Сборник":
            DBwork.add_collection(self.mdbcon,self.input_name.text(),self.input_year.text(),self.input_count.text(),self.input_type.text(),need,self.input_shelf.text())
            self.statusBar().showMessage("Запись создана")
            msg=QMessageBox.question(self,"Заполнение сборника","Не хотите ли вы сразу же заполнить созданный сборник?",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            if msg==QMessageBox.Yes:
                self.input_table.setCurrentText("Часть сборника")
                name=self.input_name.text()
                self.create_type_changed("Часть сборника")
                self.input_collection.setText(name)
            else:
                self.input_clean()

        elif self.input_table.currentText()=="Часть сборника" and self.c_id!=None:
            DBwork.add_collection_part(self.mdbcon,self.c_id,self.input_writer.text(),self.input_name.text())
            self.statusBar().showMessage("Запись создана")
            self.input_clean()
        else:
            self.statusBar().showMessage("Ошибка, запись не создана")
        
    def create_type_changed(self,type):
        for widget in self.widgets:
            widget.setDisabled(False)
        self.lbl3.setText("")
        self.input_clean()
        if type=="Книга":
            self.input_collection.setDisabled(True)
        elif type=="Сборник":
            self.input_collection.setDisabled(True)
            self.input_writer.setDisabled(True)
        elif type=="Часть сборника":
            self.input_year.setDisabled(True)
            self.input_count.setDisabled(True)
            self.input_type.setDisabled(True)
            self.input_need.setDisabled(True)
            self.input_shelf.setDisabled(True)
    
    def col_check(self,name):
        ask=DBwork.search(self.mdbcon)
        ask.a_table("collections")
        ask.a_name(name)
        if len(ask.get_result()["collections"])==0:
            self.lbl3.setStyleSheet("color:red;font-family:Arial;font-size:15pt")
            self.lbl3.setText("Такого сборника не существует")
            self.c_id=None
        else:
            self.lbl3.setStyleSheet("color:green;font-family:Arial;font-size:15pt")
            self.lbl3.setText("Сборник найден")
            self.c_id=ask.get_result()["collections"][0][0]

    def input_clean(self):
        self.input_writer.setText("")
        self.input_name.setText("")
        self.input_year.setText("")
        self.input_count.setText("")
        self.input_type.setText("")
        self.input_shelf.setText("")
        if self.phase=="search":
            self.input_need.setCurrentText("Не знаю")
        else:
            self.input_need.setCurrentText("Да")

    def phase_search(self):
        self.clean_phase()
        self.phase="search"
        self.c_id=None

        self.input_table=QComboBox()
        self.input_table.addItems(["Не знаю","Книга","Сборник","Часть сборника"])
        self.input_table.activated[str].connect(self.create_type_changed)
        self.widgets.append(self.input_table)
        self.layout.addWidget(self.input_table,1,3,1,6)

        self.input_type=QLineEdit()
        types=["научная фантастика","поэзия","детская литература"]
        completer=QCompleter(types,self.input_type)
        self.input_type.setCompleter(completer)
        self.widgets.append(self.input_type)
        self.layout.addWidget(self.input_type,6,15,1,6)

        self.input_need=QComboBox()
        self.input_need.addItems(["Не знаю","Да","Нет"])
        self.widgets.append(self.input_need)
        self.layout.addWidget(self.input_need,7,3,1,4)

        self.input_collection=QLineEdit()
        self.input_collection.textChanged[str].connect(self.col_check)
        self.widgets.append(self.input_collection)
        self.layout.addWidget(self.input_collection,2,3,1,20)

        self.input_writer=QLineEdit()
        self.widgets.append(self.input_writer)
        self.layout.addWidget(self.input_writer,4,3,1,20)
        
        self.input_name=QLineEdit()
        self.widgets.append(self.input_name)
        self.layout.addWidget(self.input_name,5,3,1,20)

        self.input_year=QLineEdit()
        self.widgets.append(self.input_year)
        self.layout.addWidget(self.input_year,6,3,1,4)

        self.input_count=QLineEdit()
        self.widgets.append(self.input_count)
        self.layout.addWidget(self.input_count,6,10,1,3)

        self.input_shelf=QLineEdit()
        self.widgets.append(self.input_shelf)
        self.layout.addWidget(self.input_shelf,7,10,1,3)

        self.lbl1=QLabel("Тип")
        self.widgets.append(self.lbl1)
        self.layout.addWidget(self.lbl1,1,1,1,2)

        self.lbl2=QLabel("Название сборника")
        self.widgets.append(self.lbl2)
        self.layout.addWidget(self.lbl2,2,1,2,2)

        self.lbl3=QLabel("")
        self.lbl3.setAlignment(Qt.AlignCenter)
        self.lbl3.setMaximumHeight(25)
        self.widgets.append(self.lbl3)
        self.layout.addWidget(self.lbl3,3,3,1,10)

        self.lbl4=QLabel("Автор")
        self.widgets.append(self.lbl4)
        self.layout.addWidget(self.lbl4,4,1,1,2)

        self.lbl5=QLabel("Название")
        self.widgets.append(self.lbl5)
        self.layout.addWidget(self.lbl5,5,1,1,2)

        self.lbl6=QLabel("Год издания")
        self.widgets.append(self.lbl6)
        self.layout.addWidget(self.lbl6,6,1,1,2)

        self.lbl7=QLabel("Количество томов")
        self.widgets.append(self.lbl7)
        self.layout.addWidget(self.lbl7,6,7,1,3)

        self.lbl8=QLabel("Жанр")
        self.widgets.append(self.lbl8)
        self.layout.addWidget(self.lbl8,6,13,1,2)

        self.lbl9=QLabel("Необходимость")
        self.widgets.append(self.lbl9)
        self.layout.addWidget(self.lbl9,7,1,1,2)

        self.lbl10=QLabel("Номер шкафа")
        self.widgets.append(self.lbl10)
        self.layout.addWidget(self.lbl10,7,7,1,3)

        self.back_btn=QPushButton("Назад")
        self.back_btn.clicked.connect(self.phase_menu)
        self.widgets.append(self.back_btn)
        self.layout.addWidget(self.back_btn,12,15,1,4)

        self.create_btn=QPushButton("Искать")
        self.create_btn.clicked.connect(self.search)
        self.widgets.append(self.create_btn)
        self.layout.addWidget(self.create_btn,12,19,1,4)

    def search(self):
        ask=DBwork.search(self.mdbcon)
        
        if self.input_table.currentText()=="Книга":
            ask.a_table("books")
        if self.input_table.currentText()=="Сборник":
            ask.a_table("collections")
        if self.input_table.currentText()=="Часть сборника":
            ask.a_table("col_parts")
        if self.input_collection.text()!="":
            ask.a_col_id(self.c_id)
        if self.input_writer.text()!="":
            ask.a_writer(self.input_writer.text())
        if self.input_name.text()!="":
            ask.a_name(self.input_name.text())
        if self.input_year.text()!="":
            ask.a_year(self.input_year.text())
        if self.input_count.text()!="":
            ask.a_count(self.input_count.text())
        if self.input_type.text()!="":
            ask.a_type(self.input_type.text())
        if self.input_shelf.text()!="":
            ask.a_shelf(self.input_shelf.text())
        if self.input_need.currentText()=="Да":
            ask.a_need(1)
        elif self.input_need.currentText()=="Нет":
            ask.a_need(2)
        
        self.result=ask.get_result()
        self.phase_results()

    def phase_results(self):
        self.clean_phase()
        self.phase="results"

        self.listwidget=QWidget()
        self.listlayout=QGridLayout()
        self.listlayout.setAlignment(Qt.AlignTop)
        self.listwidget.setLayout(self.listlayout)
        self.scroller=QScrollArea()
        self.scroller.setWidgetResizable(True)
        self.scroller.setWidget(self.listwidget)
        self.widgets.append(self.scroller)
        self.layout.addWidget(self.scroller,1,1,10,22)
        self.rows=[]

        self.back_btn=QPushButton("Назад")
        self.back_btn.clicked.connect(self.phase_search)
        self.widgets.append(self.back_btn)
        self.layout.addWidget(self.back_btn,12,19,1,4)

        i=1
        for item in self.result.items():
            for row in item[1]:
                if item[0]=="books":
                    self.rows.append([str(row[0]),QLabel("К"),QLabel(row[1]),QLabel(row[2]),QPushButton("Подробнее")])
                if item[0]=="collections":
                    self.rows.append([str(row[0]),QLabel("С"),QLabel(""),QLabel(row[1]),QPushButton("Подробнее")])
                if item[0]=="col_parts":
                    self.rows.append([str(row[0]),QLabel("Ч"),QLabel(row[2]),QLabel(row[3]),QPushButton("Подробнее")])
                self.rows[-1][4].clicked.connect(self.passport)
                self.listlayout.addWidget(self.rows[-1][1],i,1)
                self.listlayout.addWidget(self.rows[-1][2],i,2,1,9)
                self.listlayout.addWidget(self.rows[-1][3],i,11,1,10)
                self.listlayout.addWidget(self.rows[-1][4],i,21,1,2)
                i+=1

    def passport(self):
        for row in self.rows:
            if self.sender()==row[4]:
                if row[1].text()=="К": self.passp=kekpassport(DBwork.open_id(self.mdbcon,"books",row[0]),"Книга",self.mdbcon)
                if row[1].text()=="С": self.passp=kekpassport(DBwork.open_id(self.mdbcon,"collections",row[0]),"Сборник",self.mdbcon)
                if row[1].text()=="Ч": self.passp=kekpassport(DBwork.open_id(self.mdbcon,"col_parts",row[0]),"Часть сборника",self.mdbcon)
                self.windows.append(self.passp)

    def phase_settings(self):
        print("settings")

    def phase_sync(self):
        print("sync")

    def clean_phase(self):
        for widget in self.widgets:
            self.layout.removeWidget(widget)
            delete(widget)
        self.widgets=[]

    def closeEvent(self,event):
        mdbcon.close()
        for window in self.windows:
            window.close()
        event.accept()
               
class kekpassport(QWidget):
    def __init__(self,info,table,mdbcon):
        super().__init__()
        self.setWindowTitle("Информация")

        self.layout=QGridLayout()
        self.setLayout(self.layout)

        a=[]
        for i in info:
            a.append(str(i))
        self.id=a[0]
        self.info=info
        self.table=table
        self.widgets=[]
        self.mdbcon=mdbcon
        
        if table=="Книга":
            if a[6]=="True": a[6]="Да"
            else: a[6]="Нет"
            self.heads=QLabel("Тип:\nID:\nАвтор:\nНазвание:\nГод:\nЧисло томов:\nЖанр:\nНеобходимость:\nНомер шкафа:")
            self.values=QLabel(table+"\n"+a[0]+"\n"+a[1]+"\n"+a[2]+"\n"+a[3]+"\n"+a[4]+"\n"+a[5]+"\n"+a[6]+"\n"+a[7])
            self.delete_btn=QPushButton("Удалить")
            self.repair_btn=QPushButton("Изменить")
            self.layout.addWidget(self.heads,1,1,8,2)
            self.layout.addWidget(self.values,1,3,8,6)
            self.layout.addWidget(self.delete_btn,9,5,1,4)
            self.layout.addWidget(self.repair_btn,9,1,1,4)
        if table=="Сборник":
            print(a)
            if a[4]=="True": a[4]="Да"
            else: a[4]="Нет"
            self.heads=QLabel("Тип:\nID:\nНазвание:\nГод:\nЧисло томов:\nЖанр:\nНеобходимость:\nНомер шкафа:")
            self.values=QLabel(table+"\n"+a[0]+"\n"+a[1]+"\n"+a[2]+"\n"+a[3]+"\n"+a[5]+"\n"+a[4]+"\n"+a[6])
            self.delete_btn=QPushButton("Удалить")
            self.repair_btn=QPushButton("Изменить")
            self.layout.addWidget(self.heads,1,1,7,2)
            self.layout.addWidget(self.values,1,3,7,6)
            self.layout.addWidget(self.delete_btn,8,5,1,4)
            self.layout.addWidget(self.repair_btn,8,1,1,4)
        if table=="Часть сборника":
            self.heads=QLabel("Тип:\nID:\nID сборника:\nАвтор:\nНазвание:")
            self.values=QLabel(table+"\n"+a[0]+"\n"+a[1]+"\n"+a[2]+"\n"+a[3])
            self.delete_btn=QPushButton("Удалить")
            self.repair_btn=QPushButton("Изменить")
            self.goto_col_btn=QPushButton("Перейти к сборнику")
            self.layout.addWidget(self.heads,1,1,4,2)
            self.layout.addWidget(self.values,1,3,4,6)
            self.layout.addWidget(self.delete_btn,5,5,1,4)
            self.layout.addWidget(self.repair_btn,5,1,1,4)
            self.layout.addWidget(self.goto_col_btn,6,1,1,8)
        self.repair_btn.clicked.connect(self.repairing)
        self.delete_btn.clicked.connect(self.deleting)
        self.widgets.append(self.heads)
        self.widgets.append(self.values)
        self.widgets.append(self.delete_btn)
        self.widgets.append(self.repair_btn)
        self.heads.setAlignment(Qt.AlignRight)

        self.show()

    def repairing(self):
        self.repair=repairing(self.table,self.id,self.mdbcon)

    def deleting(self):
        DBwork.delete(self.mdbcon,tab_convert(self.table),self.id)

        for res in kek.result[tab_convert(self.table)]:
            if str(res[0])==self.id:
                kek.result[tab_convert(self.table)].remove(res)
        kek.phase_results()

        self.close()

class repairing(QWidget):
    def __init__(self,table,id,mdbcon):
        super().__init__()
        self.setWindowTitle("Редактирование")

        self.table=table
        self.id=id
        self.mdbcon=mdbcon
        if self.table=="Книга":
            self.prefix="b_"
        elif self.table=="Сборник":
            self.prefix="c_"
        elif self.table=="Часть сборника":
            self.prefix="p_"

        self.layout=QGridLayout()
        self.setLayout(self.layout)

        self.type=QComboBox()
        if table=="Книга": items=("Автор","Название","Год издания","Кол-во томов","Жанр","Необходимость","Номер шкафа")
        if table=="Сборник": items=("Название","Год издания","Кол-во томов","Жанр","Необходимость","Номер шкафа")
        if table=="Часть сборника": items=("Автор","Название")
        self.type.addItems((items))
        self.type.activated[str].connect(self.type_changed)
        self.layout.addWidget(self.type,1,1,1,4)
        
        self.value=QLineEdit()
        self.layout.addWidget(self.value,2,1,1,4)
        
        self.cancel_btn=QPushButton("Отмена")
        self.cancel_btn.clicked.connect(self.close)
        self.layout.addWidget(self.cancel_btn,3,1,1,2)

        self.repair_btn=QPushButton("Изменить")
        self.repair_btn.clicked.connect(self.repair)
        self.layout.addWidget(self.repair_btn,3,3,1,2)

        self.show()
        
    def repair(self):
        if self.type.currentText()=="Необходимость" and self.value.currentText()=="Да": val="1"
        elif self.type.currentText()=="Необходимость" and self.value.currentText()=="Нет": val="0"
        else: val=self.value.text()
        for i in {"Автор":"writer","Название":"name","Год издания":"year","Кол-во томов":"count","Жанр":"type","Необходимость":"need","Номер шкафа":"shelf"}.items():
            if self.type.currentText()==i[0]:
                field=self.prefix+i[1]

        DBwork.update(self.mdbcon,tab_convert(self.table),{field:val},self.id)

        for res in kek.result[tab_convert(self.table)]:
            if str(res[0])==self.id:
                kek.result[tab_convert(self.table)].remove(res)
                kek.result[tab_convert(self.table)].append(DBwork.open_id(self.mdbcon,tab_convert(self.table),self.id))
        kek.phase_results()

        kek.passp.close()
        self.close()

    def type_changed(self,new_type):
        self.layout.removeWidget(self.value)
        delete(self.value)
        if new_type=="Необходимость":
            self.value=QComboBox()
            self.value.addItems(("Да","Нет"))
            self.layout.addWidget(self.value,2,1,1,4)
        else:
            self.value=QLineEdit()
            self.layout.addWidget(self.value,2,1,1,4)

def tab_convert(table):
    names={"Книга":"books","Часть сборника":"col_parts","Сборник":"collections"}
    for name in names.items():
        if table==name[0]: return name[1]
        elif table==name[1]: return name[0]
        else: print("convert error")

if __name__=="__main__":
    mdbcon=pypyodbc.win_connect_mdb(os.path.abspath("database.MDB"))
    app=QApplication(sys.argv)
    kek=kekapp(mdbcon)
    sys.exit(app.exec_())
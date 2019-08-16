import pypyodbc
import os
import sys
import DBwork
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from PyQt5.sip import delete

class kekapp(QMainWindow):
    def __init__(self,mdbcon):
        super().__init__()
        self.mainwidget=QWidget()
        self.setCentralWidget(self.mainwidget)
        self.setWindowTitle("Мои книги")
        self.resize(1100,600)
        self.layout=QGridLayout(self.mainwidget)
        self.setFont(QFont("Arial",15))
        self.show()

        self.mdbcon=mdbcon
        self.widgets=[]
        self.first=True

        self.phase_menu()
    
    def phase_menu(self):
        if not self.first:
            self.clean_phase()
        self.first=False

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

        self.stats=QLabel("Статистика:\n\nВсего:\n"+DBwork.stats(self.mdbcon)+"\nКниг:\n"+DBwork.stats(self.mdbcon,"books")+"\nСборников:\n"+DBwork.stats(self.mdbcon,"collections")+"\nЧастей сборников:\n"+DBwork.stats(self.mdbcon,"col_parts"))
        self.stats.setAlignment(Qt.AlignCenter)
        self.widgets.append(self.stats)
        self.layout.addWidget(self.stats,1,14,9,6)
    
    def phase_create(self):
        self.clean_phase()
        self.c_id=None

        self.input_table=QComboBox()
        self.input_table.addItems(["Книга","Сборник","Часть сборника"])
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

        self.lbl6=QLabel("Год")
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

        self.lbl10=QLabel("Номер полки")
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
        self.input_need.setCurrentText("Да")

    def phase_search(self):
        self.clean_phase()

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
        event.accept()
        
if __name__=="__main__":
    mdbcon=pypyodbc.win_connect_mdb(os.path.abspath("database.MDB"))
    app=QApplication(sys.argv)
    kek=kekapp(mdbcon)
    sys.exit(app.exec_())
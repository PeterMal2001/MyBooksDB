import pypyodbc
import os
import DBwork

mdbcon=pypyodbc.win_connect_mdb(os.path.abspath("database.MDB"))



mdbcon.close()
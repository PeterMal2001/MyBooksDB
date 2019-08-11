import pypyodbc

def add_book(mdbcon,writer,name,year,count,type,need,shelf):
    cur=mdbcon.cursor()
    values="'"+writer+"','"+name+"',"+year+","+count+",'"+type+"',"+need+","+shelf
    cur.execute("INSERT INTO books (b_writer,b_name,b_year,b_count,b_type,b_need,b_shelf) VALUES ("+values+")")
    mdbcon.commit()
    cur.close()
    
def add_collection(mdbcon,name,year,count,type,need,shelf):
    cur=mdbcon.cursor()
    
    values="'"+name+"',"+year+","+count+",'"+type+"',"+need+","+shelf
    cur.execute("INSERT INTO collections (c_name,c_year,c_count,c_type,c_need,c_shelf) VALUES ("+values+")")
    mdbcon.commit()
    
    col="(c_name='"+name+"' AND c_year="+year+" AND c_count="+count+" AND c_type='"+type+"' AND c_need="+need+")"
    cur.execute("SELECT id FROM collections WHERE "+col)
    return cur.fetchall()[0][0]
    cur.close()

def add_collection_part(mdbcon,c_id,writer,name):
    cur=mdbcon.cursor()

    values=str(c_id)+",'"+writer+"','"+name+"'"
    cur.execute("INSERT INTO col_parts (col_id,p_writer,p_name) VALUES ("+values+")")
    mdbcon.commit()

    cur.close()

def delete(mdbcon,table,id):
    cur=mdbcon.cursor()

    cur.execute("DELETE FROM "+table+" WHERE id="+str(id))
    if table=="collections":
        cur.execute("DELETE FROM col_parts WHERE col_id="+str(id))
    mdbcon.commit()

    cur.close()

class search():
    def __init__(self,mdbcon):
        self.mdbcon=mdbcon
        self.info={}
        self.table=None
    def a_table(self,table):
        self.table=table
    def a_writer(self,writer):
        self.info["writer"]=writer
    def a_name(self,name):
        self.info["name"]=name
    def a_year(self,year):
        self.info["year"]=year
    def a_count(self,count):
        self.info["count"]=count
    def a_type(self,type):
        self.info["type"]=type
    def a_need(self,need):
        self.info["need"]=need
    def a_shelf(self,shelf):
        self.info["shelf"]=shelf

    def get_result(self):
        result={}
        cur=self.mdbcon.cursor()

        if self.table=="books" or self.table==None:
            first=True
            for i in self.info.items():
                if i[0] in ("writer","name","type"):
                    val="'"+i[1]+"'"
                else:
                    val=i[1]
                if first:
                    ask="b_"+i[0]+"="+val
                    first=False
                else:
                    ask+=" AND b_"+i[0]+"="+val
            
            cur.execute("SELECT * FROM books WHERE "+ask)
            result["books"]=cur.fetchall()

        unp=self.info.get("writer")==None
        if unp and(self.table=="collections" or self.table==None):
            first=True
            for i in self.info.items():
                if i[0] in ("name","type"):
                    val="'"+i[1]+"'"
                else:
                    val=i[1]
                if first:
                    ask="c_"+i[0]+"="+val
                    first=False
                else:
                    ask+=" AND c_"+i[0]+"="+val

            cur.execute("SELECT * FROM collections WHERE "+ask)
            result["collections"]=cur.fetchall()

        unp=True
        for a in ("year","count","type","need","shelf"):
            if self.info.get(a)!=None:
                unp=False
        if unp and(self.table=="col_parts" or self.table==None):
            first=True
            for i in self.info.items():
                val="'"+i[1]+"'"
                if first:
                    ask="p_"+i[0]+"="+val
                    first=False
                else:
                    ask+=" AND p_"+i[0]+"="+val

            cur.execute("SELECT * FROM col_parts WHERE "+ask)
            result["col_parts"]=cur.fetchall()
        
        cur.close()
        return result

    def open_id(self,table,id):
        cur=self.mdbcon.cursor()
        cur.execute("SELECT * FROM "+table+" WHERE id="+id)
        result=cur.fetchall()
        cur.close()
        return result
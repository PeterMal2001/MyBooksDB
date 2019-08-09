import pypyodbc

def add_book(mdbcon,writer,name,year,count,type,need):
    cur=mdbcon.cursor()
    values="'"+writer+"','"+name+"',"+year+","+count+",'"+type+"',"+need
    cur.execute("INSERT INTO books (b_writer,b_name,b_year,b_count,b_type,b_need) VALUES ("+values+")")
    mdbcon.commit()
    cur.close()
    
def add_collection(mdbcon,name,year,count,type,need):
    cur=mdbcon.cursor()
    
    values="'"+name+"',"+year+","+count+",'"+type+"',"+need
    cur.execute("INSERT INTO collections (c_name,c_year,c_count,c_type,c_need) VALUES ("+values+")")
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
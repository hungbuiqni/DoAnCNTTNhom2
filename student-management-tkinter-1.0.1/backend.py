# import sqlite3
from logging import exception
import os
import random
import mysql.connector

DB_USER = "root"
DB_PASSWORD = "123456"

def connect():
    ''' Create a database if not existed and make a connection to it.
    
    '''

    
    try:
        conn = mysql.connector.connect(
            host = "localhost",
            user = DB_USER, 
            password = DB_PASSWORD
        )
        cur = conn.cursor()
      
        conn.close()
    except Exception as e:
        print(e)
    
    conn = mysql.connector.connect(
        host = "localhost",
        user = DB_USER,
        password = DB_PASSWORD,
        database = "students_quochung"
    )
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS DanhSach (MaHS TEXT NOT NULL, Ho TEXT, Ten TEXT, Phai BOOLEAN, NgaySinh DATE, MaTruong TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Diem (MaHS TEXT NOT NULL, Mon TEXT, Diem FLOAT)")
    cur.execute("CREATE TABLE IF NOT EXISTS Truong (MaTruong TEXT NOT NULL, TenTruong TEXT)")
    conn.commit()
    conn.close()

def view_ds():
    ''' view 
    '''
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung"
        )
    cur = conn.cursor()
    cur.execute("SELECT * FROM danhsach")
    rows = cur.fetchall()   
    conn.close()
    return rows

def view_diem():
    ''' view 
    '''
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute("SELECT * FROM diem")
    rows = cur.fetchall()
    conn.close()
    return rows

def view_truong():
    ''' view 
    '''
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute("SELECT * FROM truong")
    rows = cur.fetchall()
    conn.close()
    return rows

def insert_ds(index,mahs,ho,ten,phai,ngaysinh,matruong,vitri="truoc"):
    ''' insertion function to insert a new record to the database.
    
        Arguments
        ---------
    '''
    phai
    startEffectedRow = index
    if vitri == "sau":
        startEffectedRow += 1
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS tempDanhSach")
    cur.execute("CREATE TABLE tempdanhsach AS SELECT * from DanhSach limit %s,1000" % (startEffectedRow,))
    
    cur.execute("DELETE FROM DanhSach where MaHS in (SELECT MaHS from tempDanhSach)")

    cur.execute("INSERT INTO DanhSach (MaHS, Ho, Ten, Phai, NgaySinh, MaTruong) VALUES (%s,%s,%s,%s,%s,%s)", (mahs,ho,ten,phai,ngaysinh,matruong))
    

    cur.execute("INSERT INTO DanhSach (MaHS, Ho, Ten, Phai, NgaySinh, MaTruong) SELECT MaHS, Ho, Ten, Phai, NgaySinh, MaTruong FROM tempDanhSach")
    
    cur.execute("DROP TABLE IF EXISTS tempDanhSach")

    conn.commit()
    conn.close()

def insert_diem(index,mahs,mon,diem,vitri="truoc"):
    ''' insertion function to insert a new record to the database.
    
        Arguments
        ---------
    '''
    startEffectedRow = index
    if vitri == "sau":
        startEffectedRow += 1
    tmpTable = "tempDiem"
    table = "Diem"
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS %s" % (tmpTable,))
    cur.execute("CREATE TABLE %s AS SELECT * from %s limit %s,1000" % (tmpTable, table, startEffectedRow,))
    
    cur.execute("DELETE FROM %s where MaHS in (SELECT MaHS from %s)" % (table, tmpTable,))

    cur.execute("INSERT INTO Diem (MaHS, Mon, Diem) Values (%s,%s,%s)", (mahs,mon,diem,))

    cur.execute("INSERT INTO %s (MaHS, Mon, Diem) SELECT MaHS, Mon, Diem FROM %s" % (table, tmpTable))
    
    cur.execute("DROP TABLE IF EXISTS %s" % (tmpTable,))

    conn.commit()
    conn.close()

def insert_truong(index,matruong,tentruong,vitri="truoc"):
    ''' insertion function to insert a new record to the database.
    
        Arguments
        ---------
    '''
    startEffectedRow = index
    if vitri == "sau":
        startEffectedRow += 1
    tmpTable = "tempTruong"
    table = "Truong"
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS %s" % (tmpTable,))
    cur.execute("CREATE TABLE %s AS SELECT * from %s limit %s,1000" % (tmpTable, table, startEffectedRow,))
    
    cur.execute("DELETE FROM %s where MaTruong in (SELECT MaTruong from %s)" % (table, tmpTable,))

    cur.execute("INSERT INTO Truong (MaTruong, TenTruong) Values (%s,%s)",(matruong,tentruong))

    cur.execute("INSERT INTO %s (MaTruong, TenTruong) SELECT MaTruong, TenTruong FROM %s" % (table, tmpTable))
    
    cur.execute("DROP TABLE IF EXISTS %s" % (tmpTable,))

    conn.commit()
    conn.close()

def view_item5():
    ''' truy xu???t theo y??u c???u s??? 5. 
        K???t qu??? file: item5.txt
    '''

    danh_sach = execute_sql("select * from DanhSach")
    diem = execute_sql("select * from Diem")

    list_result = []
    for ds in danh_sach:
        data = {}
        data["SDB"] = ds[0]
        data["Ho"] = ds[1]
        data["Ten"] = ds[2]
        data["Phai"] = ds[3]
        data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        data["TongDiem"] = 0
        data["DTN"] = 0
        data["XepLoai"] = None
        data["MaTruong"] = ds[5]
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                data["TongDiem"] = data["Toan"] + data["Van"]
                data["DTN"] = min(data["Toan"],data["Van"])
                data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
        list_result.append(data)
    mylist = sorted(list_result, key=lambda k: (k['MaTruong'].lower(), k['Ten'].lower(), k['Ho'].lower()))
    header = "SBD,  Ho, Ten,  Phai, NgaySinh, Toan,  Van, TongDiem, DTN, XepLoai, MaTruong"
    file_name = "item5.txt"
    write_to_file(file_name, mylist, header)
    return file_name

def view_item6():
    ''' truy xu???t theo y??u c???u s??? 6. 
        K???t qu??? file: item6.txt
    '''

    danh_sach = execute_sql("select * from DanhSach")
    diem = execute_sql("select * from Diem")

    list_result = []
    for ds in danh_sach:
        data = {}
        data["SDB"] = ds[0]
        data["Ho"] = ds[1]
        data["Ten"] = ds[2]
        data["Phai"] = ds[3]
        data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        # data["TongDiem"] = 0
        # data["DTN"] = 0
        # data["XepLoai"] = None
        data["MaTruong"] = ds[5]
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                if data["Toan"] != 0 and data["Van"] != 0:
                    break
                # data["TongDiem"] = data["Toan"] + data["Van"]
                # data["DTN"] = min(data["Toan"],data["Van"])
                # data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
        if data["Toan"] > data["Van"]:       
            list_result.append(data)
    mylist = sorted(list_result, key=lambda k: (k['MaTruong'].lower(), k['Ten'].lower(), k['Ho'].lower()))
    header = "SBD,  Ho, Ten,  Phai, NgaySinh, Toan,  Van, MaTruong"
    file_name = "item6.txt"
    write_to_file(file_name, mylist, header)
    return file_name

def view_item7():
    ''' truy xu???t theo y??u c???u s??? 7. 
        K???t qu??? file: item7.txt
    '''

    danh_sach = execute_sql("select * from DanhSach")
    diem = execute_sql("select * from Diem")

    list_result = []
    for ds in danh_sach:
        data = {}
        data["SDB"] = ds[0]
        data["Ho"] = ds[1]
        data["Ten"] = ds[2]
        data["Phai"] = ds[3]
        data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        data["TongDiem"] = 0
        data["XepLoai"] = None
        data["MaTruong"] = ds[5]
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                data["TongDiem"] = data["Toan"] + data["Van"]
                data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
                if data["Toan"] != 0 and data["Van"] != 0:
                    break
        if data["XepLoai"] == "Kem":
            list_result.append(data)
    mylist = sorted(list_result, key=lambda k: (k['MaTruong'].lower(), k['Ten'].lower(), k['Ho'].lower()))
    header = "SBD,  Ho, Ten,  Phai, NgaySinh, Toan,  Van, TongDiem, XepLoai, MaTruong"
    file_name = "item7.txt"
    write_to_file(file_name, mylist, header)
    return file_name

def view_item8():
    ''' truy xu???t theo y??u c???u s??? 8. 
        K???t qu??? file: item8.txt
    '''

    danh_sach = execute_sql("select * from DanhSach")
    diem = execute_sql("select * from Diem")

    list_result = []
    #Tao set data type ????? ch???a c??c m?? tr?????ng kh??ng tr??ng l???p trong db
    schoolSet = set()
    for ds in danh_sach:
        data = {}
        data["SDB"] = ds[0]
        data["Ho"] = ds[1]
        data["Ten"] = ds[2]
        data["Phai"] = ds[3]
        data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        data["TongDiem"] = 0
        data["XepLoai"] = None
        data["MaTruong"] = ds[5]
        schoolSet.add(ds[5])
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                data["TongDiem"] = data["Toan"] + data["Van"]
                data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
                if data["Toan"] != 0 and data["Van"] != 0:
                    break
        list_result.append(data)
    #chuy???n l???i v??? d???ng list ????? c?? th??? b??? d???u kho???ng tr???ng
    schoolList = list(schoolSet)
    newList = []
    for i in range(len(schoolList)):
        newList.append(schoolList[i].strip())
    #X??a m?? tr?????ng ?????c bi???t: ""
    # newList.remove("")
    #Chuy???n l???i v??? d???ng set ????? lo???i b??? nh???ng m?? tr?????ng gi???ng nhau sau khi lo???i kho???ng tr???ng
    newList1 = set(newList)
    #T???o list cho m???i m??, t??m ph???n t??? c?? t???ng ??i???m max (th??? khoa) v?? th??m v??o list cu???i c??ng: list_mark
    list_mark = []
    for i in newList1:
        list_new = []
        for data in list_result:
            if data["MaTruong"].strip() == i:
                list_new.append(data)
                list_result.remove(data)
        max = int(list_new[0]["TongDiem"])
        i = 0
        for addr in range(len(list_new)):
            if int(list_new[addr]["TongDiem"]) > max:
                max = int(list_new[addr]["TongDiem"])
                i = addr
        list_mark.append(list_new[i])    
    mylist = sorted(list_mark, key=lambda k: (k['MaTruong'].lower(), k['Ten'].lower(), k['Ho'].lower()))
    header = "SBD,  Ho, Ten,  Phai, NgaySinh, Toan,  Van, TongDiem, XepLoai, MaTruong"
    file_name = "item8.txt"
    write_to_file(file_name, mylist, header)
    return file_name

def view_item9(nameSchool):
    ''' view function to show the content of the database
        returns the content of the database with filter.
    '''
    danh_sach = execute_sql("select * from DanhSach where trim(MaTruong) = '%s'" % (nameSchool.strip(),))
    diem = execute_sql("select * from Diem")

    list_result = []
    for ds in danh_sach:
        data = {}
        data["SDB"] = ds[0]
        data["Ho"] = ds[1]
        data["Ten"] = ds[2]
        data["Phai"] = ds[3]
        data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        data["TongDiem"] = 0
        data["DTN"] = 0
        data["XepLoai"] = None
        data["MaTruong"] = ds[5]
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                data["TongDiem"] = data["Toan"] + data["Van"]
                data["DTN"] = min(data["Toan"],data["Van"])
                data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
        # if data["MaTruong"].strip() == nameSchool.strip():
        list_result.append(data)
    mylist = sorted(list_result, key=lambda k: (k['MaTruong'].lower(), k['Ten'].lower(), k['Ho'].lower()))
    #print(mylist)
    header = "SBD,  Ho, Ten,  Phai, NgaySinh, Toan,  Van, TongDiem, DTN, XepLoai, MaTruong"
    file_name = "item9.txt"
    write_to_file(file_name, mylist, header)
    return file_name

def view_item10():
    ''' truy xu???t theo y??u c???u s??? 10.
        l???y random 3 h???c sinh t??? DanhSach 
        K???t qu??? file: item5.txt
    '''

    danh_sach = execute_sql("select * from DanhSach")
    diem = execute_sql("select * from Diem")

    num_to_select = 3 # set the number to select here.
    list_of_random_items = random.sample(danh_sach, num_to_select)

    list_result = []
    for ds in list_of_random_items:
        data = {}
        data["SDB"] = ds[0]
        # data["Ho"] = ds[1]
        # data["Ten"] = ds[2]
        data["HoTen"] = ds[1].strip() + ' ' + ds[2].strip()
        #data["Phai"] = ds[3]
        #data["NgaySinh"] = ds[4]
        data["Toan"] = 0
        data["Van"] = 0
        data["TongDiem"] = 0
        #data["DTN"] = 0
        data["XepLoai"] = None
        #data["MaTruong"] = ds[5]
        for d in diem:
            if data["SDB"] == d[0]:
                if d[1].strip()=="Toan":
                    data["Toan"] = d[2]
                if d[1].strip()=="Van":
                    data["Van"] = d[2]
                data["TongDiem"] = data["Toan"] + data["Van"]
                #data["DTN"] = min(data["Toan"],data["Van"])
                data["XepLoai"] = get_xeploai(data["Toan"], data["Van"])
        
        # Convert data cho d??? ?????c
        data["SDB"] = "So Bao Danh: " + data["SDB"]
        data["HoTen"] = "Anh: " + data["HoTen"] if ds[3] is 0 else "Chi: " + data["HoTen"]
        data["Toan"] = "Diem Toan: " + str(data["Toan"])
        data["Van"] = "Diem Van: " + str(data["Van"])
        data["TongDiem"] = "Tong Diem: " + str(data["TongDiem"])
        data["XepLoai"] = "Xep Loai: " + str(data["XepLoai"])
        
        list_result.append(data)
    mylist = list_result
    file_name = "item10.txt"
    write_to_file_no_h(file_name, mylist)
    return file_name

def delete(id, table, option_val=""):
    ''' delete function to delete a specific record from the database.
    
        Arguments
        ---------
        id: int, id of the record in the database.
    '''
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur  = conn.cursor()
    if table == 1:
        cur.execute("DELETE FROM DanhSach WHERE MaHS='%s'" % (id.strip(),))
    elif table == 2:
        cur.execute("DELETE FROM Diem WHERE MaHS='%s' AND Mon='%s'" % (id.strip(),option_val.strip(),))
    elif table == 3:
        cur.execute("DELETE FROM Truong WHERE MaTruong='%s'" % (id.strip(),))
    conn.commit()
    conn.close()

def delete_data():
    ''' delete_data function is to delete the database.
    
    '''
    if os.path.exists("Students.db"):
        os.remove("Students.db")
    connect()

# Cac ham util
def execute_sql(query):
    conn = mysql.connector.connect(host = "localhost",
        user = DB_USER, password = DB_PASSWORD,
        database="students_quochung")
    cur = conn.cursor()
    cur.execute(query)
    rows = cur.fetchall()
    return rows

#xu???t ra file txt c?? header
def write_to_file(filename, a_list, header):
    textfile = open(filename, "w")
    textfile.write(header + "\n")
    for element in a_list:
        line = ""
        for key,value in element.items():
            line += str(value) + ","
        textfile.write(line + "\n")
    textfile.close()

#xu???t ra file txt khong c???n header
def write_to_file_no_h(filename, a_list):
    textfile = open(filename, "w")
    for element in a_list:
        line = ""
        for key,value in element.items():
            line += str(value) + ","
        textfile.write(line + "\n")
    textfile.close()

# ?????c n???i dung file txt
def read_file_data(file_name):
    #Read file and add all line to a list variable
    with open(file_name, 'r')as f:
        a = f.readlines()
    lst = []
    for i in a:
        lst.append(i.replace(',0,',',Nam,').replace(',1,',',Nu,').replace("\n",""))
    return lst

# t??nh xep lo???i
def get_xeploai(toan, van):
    xeploai = ""
    if (toan + van) >=16 and toan >=7 and van >=7:
        xeploai = "Gioi"
    elif (toan + van) >=14 and toan >=6 and van >=6:
        xeploai = "Kha"
    elif (toan + van) >=10 and toan >=4 and van >=4:
        xeploai = "Trung Binh"
    else:
        xeploai = "Kem"
    return xeploai

connect()

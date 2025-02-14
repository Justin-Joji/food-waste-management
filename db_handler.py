
'''
WORK IN PROGRESS: CHANGES ARE BEING MADE
'''

# Program to handle MySQL database using python
import mysql.connector as sql

class MySQLDB:
    def __init__(self):
        # Initial connection
        self.db = sql.connect(
            user = 'root',
            password = 'mythical',
            host = 'localhost')
        self.cursor = self.db.cursor()

        # Setting database
        query = 'create database if not exists waste'
        self.cursor.execute(query)
        self.cursor.execute('use waste')

        # Setting tables
        query = 'create table if not exists accounts(AccID varchar(5) primary key, Name varchar(30) unique, Email varchar(30) unique, Password varchar(30), Role varchar(5))'
        self.cursor.execute(query)
        query = 'create table if not exists requests(ReqID varchar(7) primary key, Name varchar(30), Email varchar(30), Phone bigint, Address varchar(30), Category varchar(30), Quantity int, Preparation date)'
        self.cursor.execute(query)
        
    def add_account(self, name, email, pwd, role):
        query = 'select count(*) from accounts'
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        
        query = 'insert into accounts values(%s, %s, %s, %s, %s)'
        accid = role[1].upper() + str(300+count+1);
        self.cursor.execute(query, (accid, name, email, pwd, role))
        self.db.commit()
        
    def add_request(self, name, email, phone, addr, categ, quant, prepdate):
        query = 'select count(*) from requests'
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        
        reqid = 'R' + str(100000+count+1)
        query = 'insert into requests values(%s, %s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(query, (reqid, name, email, phone, addr, categ, quant, prepdate))
        self.db.commit()
        
    def check_account(self, email, pwd):
        query = 'select * from accounts where email=%s'
        self.cursor.execute(query, (email,))
        record = self.cursor.fetchone()
        if record is None:
            # Email is wrong
            return 'E101'
            
        query = 'select * from accounts where email=%s and password=%s'
        self.cursor.execute(query, (email, pwd))
        record = self.cursor.fetchone()
        if record is None:
            # Email is right, but password is wrong
            return 'E210'
        
        return record[0]
     
    def get_account(self, id):    
        query = 'select * from accounts where accid=%s'
        self.cursor.execute(query, (id,))
        record = self.cursor.fetchone()
        return record
        
    def get_accounts(self):
        query = 'select * from accounts'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        return records
        
    def get_requests(self):
        query = 'select * from requests'
        self.cursor.execute(query)
        requests = self.cursor.fetchall()
        return requests
        
    def del_account(self, name):
        query = 'delete from accounts where Name=%s'
        self.cursor.execute(query, (name,))
        self.db.commit()
        
    def del_request(self, name):
        query = 'delete from requests where Name=%s'
        self.cursor.execute(query, (name,))
        self.db.commit()

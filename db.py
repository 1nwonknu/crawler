import sqlite3
import re

class DB():

    def __init__(self, dbName, writeTriple=()):

        self.conn=sqlite3.connect(dbName)
        self.writeTriple=writeTriple
        self.cursor = self.conn.cursor()
        self.tblName = re.sub('\.\d\b', '', dbName)

    def __del__(self):

        self.conn.close()


    def record_exists(self):

        self.cursor.execute("SELECT count(*) FROM crawler WHERE URL = ?", (self.currentURL,))
        data = self.cursor.fetchone()[0]
        if data == 0:
            return False
        else:
            return True


    def insert(self):
        #print(self.writeTriple)
        try:
            self.conn.execute("INSERT INTO CRAWLER (URL, Date, Words) \
            VALUES " + str(self.writeTriple)) ;
        except sqlite3.IntegrityError:
            print("webpage %s already in database!" %self.writeTriple[0])
        self.conn.commit()
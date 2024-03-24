import psycopg2

class Db:
    def __init__(self, database: str, host: str, port: int, user:str, password:str) -> None:
        self.database = database
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.conn = None
        
    def connect(self):
        self.conn = psycopg2.connect(database=self.database, user=self.user, 
                        password=self.password, host=self.host, port=self.port)
        
    def disconnect(self):
        self.conn.close()
        
    def request(self, sql_command: str):
        self.connect()
        cur = self.conn.cursor() 
        cur.execute(sql_command)
        self.conn.commit()  
        cur.close()
        self.disconnect()
    
    def response(self, sql_command: str):
        self.connect()
        cur = self.conn.cursor() 
        cur.execute(sql_command)
        self.conn.commit()
        data = cur.fetchall()
        cur.close()
        self.disconnect()
        return data  
        
        
    def bool2str(self, digit: bool) -> str:
        return "TRUE" if digit else "FALSE"
        
    
class ProgrammDB(Db):
    def __init__(self, database: str, host: str, port: int, user: str, password: str) -> None:
        super().__init__(database, host, port, user, password)
        
    def create_table(self):
        self.request(f"CREATE TABLE IF NOT EXISTS programm ( id SERIAL PRIMARY KEY,  programm_id varchar(100), step_id varchar(100));")
        self.request(f"CREATE TABLE IF NOT EXISTS step ( id SERIAL PRIMARY KEY, step_id varchar(100), value varchar(100), time integer);")
    
    def add_programm(self, programm: dict):    
        for step in programm["steps"]:
            self.request(f"INSERT INTO programm (programm_id, step_id) VALUES  ('{str(programm['id'])}', '{str(step['name'])}')")
            self.request(f"INSERT INTO step (step_id, value, time) VALUES  ('{str(step['name'])}', '{str(step['value'])}', {str(step['time'])})")
            
    def get_steps_ids(self, programm_id):
        res = self.response(f"SELECT step_id FROM programm WHERE programm_id='{programm_id}'")
        return res
        
    def get_steps_details(self, step_id):
        res = self.response(f"SELECT value, time FROM step WHERE step_id='{step_id}'")
        if not res:
            return res
        return res[0]
    
    def clear_tables(self) -> list:
        return self.request(f"DROP TABLE programm") or self.request(f"DROP TABLE step")
    
    def delete_step(self, step_id):
        self.request(f"DELETE FROM step WHERE step_id='{str(step_id)}'")
        
    def delete_programm(self, programm_id):
        self.request(f"DELETE FROM programm WHERE programm_id='{str(programm_id)}'")
    
class CounterDB(Db):
    def __init__(self, database: str, host: str, port: int, user: str, password: str) -> None:
        super().__init__(database, host, port, user, password)
        
    def create_table(self):
         self.request(f"CREATE TABLE IF NOT EXISTS counter ( name varchar(100) PRIMARY KEY,  time integer );")
         
    def add_clock(self, name, time):
        self.request(f"INSERT INTO counter (name, time) VALUES  ( '{str(name)}', {str(time)} )")
        
    def update_clock(self, name, time):
        self.request(f"UPDATE counter SET time={str(time)} WHERE name='{str(name)}'")
        
    def get_clock(self, name):
        res = self.response(f"SELECT time from counter WHERE name='{str(name)}'")
        if not res:
            return res
        return res[0][0]
        
    def delete_clock(self, name):
        self.request(f"DELETE FROM counter WHERE name='{str(name)}'")
        
    def clear_tables(self) -> list:
        return self.request(f"DROP TABLE counter")
    
    
# db = Watering_db('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')
# db.create_state_table()
# db.add_state_element("pole3")
# print(db.get_state_of_element("pole3"))
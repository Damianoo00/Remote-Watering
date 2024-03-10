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
        
class Watering_db(Db):
    def __init__(self, database: str, host: str, port: int, user: str, password: str) -> None:
        super().__init__(database, host, port, user, password)
        
    def create_state_table(self):
        self.request(f"CREATE TABLE IF NOT EXISTS watering (name varchar(100) PRIMARY KEY, state boolean);")
            
        
    def add_state_element(self, name:str, initial_state: bool=False):
       self.request(f"INSERT INTO watering (name, state) VALUES  ('{name}', {self.bool2str(initial_state)})")
        
    def update_state_element(self, name:str, state:bool):
        self.request(f"UPDATE watering SET state={self.bool2str(state)} WHERE name='{name}'")
        
    def get_state_of_element(self, name:str) -> bool:
        return self.response(f"SELECT name,state FROM watering WHERE name='{name}'")[0][1]
        
        
    def get_states_list(self) -> list:
        return self.response(f"SELECT name,state FROM watering")
    
    def clear_states(self) -> list:
        return self.request(f"DROP TABLE watering")
    
# db = Watering_db('watering', 'localhost', 5432, 'gardener', 'kap_kap_kap')
# db.create_state_table()
# db.add_state_element("pole3")
# print(db.get_state_of_element("pole3"))
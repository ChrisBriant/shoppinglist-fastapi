import psycopg2, os



class Database:
    def __init__(self):
        # create a database connection
        self.conn = self.create_connection()

        # create tables
        if self.conn is not None:
            # create projects table
            self.create_list_table()
        else:
            print("Error! cannot create the database connection.")

    # Connect to the PostgreSQL database
    def create_connection(self):
        #Connection parameters dependent on production or test, sent ENVIRONMENT to "PROD" if in prod
        if os.environ.get("ENVIRONMENT") == "PROD":
            HOST=os.environ.get('PROD_HOST')
            PORT=os.environ.get('PROD_PORT')
            DATABASE=os.environ.get('PROD_DATABASE')
            USER=os.environ.get("PROD_USER")
            PASSWORD=os.environ.get('PROD_PASSWORD')
        else: 
            HOST=os.environ.get('DEV_HOST')
            PORT=os.environ.get('DEV_PORT')
            DATABASE=os.environ.get('DEV_DATABASE')
            USER=os.environ.get("DEV_USER")
            PASSWORD=os.environ.get('DEV_PASSWORD')

        conn = psycopg2.connect(
            host=HOST,
            port=PORT,
            database=DATABASE,
            user=USER,
            password=PASSWORD
        )
        return conn

    # Create a table if it doesn't exist
    def create_list_table(self):
        cursor = self.conn.cursor()
        table_query = """
            CREATE TABLE IF NOT EXISTS item (
                id SERIAL PRIMARY KEY,
                name VARCHAR(100),
                qty INTEGER
            )
        """
        cursor.execute(table_query)
        self.conn.commit()
        cursor.close()

    def add_item(self,item):
        sql = f'''INSERT INTO item(name, qty)
                VALUES('{item.name}', '{item.qty}')
                RETURNING id'''
        cur = self.conn.cursor()
        cur.execute(sql)
        inserted_id = cur.fetchone()[0]
        self.conn.commit()
        return inserted_id
    
    def get_list(self):
        sql = ''' SELECT * FROM item '''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        #Convert to dictionaries
        rows_dict = [{ 'id' : row[0], 'name' : row[1], 'qty' : row[2] } for row in rows]
        return rows_dict
    
    def delete_item(self,id):
        sql = f'''DELETE FROM ITEM WHERE id={id}'''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows_deleted = cur.rowcount
        self.conn.commit()
        return rows_deleted
    
    def update_item(self,item):
        sql = f'''UPDATE item SET name='{item.name}', qty={item.qty}
                WHERE id={item.id}'''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows_modified = cur.rowcount
        self.conn.commit()
        return rows_modified


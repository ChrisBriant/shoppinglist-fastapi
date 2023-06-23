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
            host="23634c388c2e",
            port="5432",
            database="postgres",
            user="postgres",
            password="BojoB0j0%"
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
        #TEST
        sql = ''' SELECT * FROM item '''
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print(rows)
        ####
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
        print(rows_dict)
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
        print(sql)
        cur = self.conn.cursor()
        cur.execute(sql)
        rows_modified = cur.rowcount
        self.conn.commit()
        return rows_modified

    # def create_connection(self,db_file):
    #     self.conn = None
    #     try:
    #         self.conn = sqlite3.connect(db_file)
    #         return self.conn
    #     except Error as e:
    #         print(e)

    #     return self.conn


    # def create_table(self, create_table_sql):
    #     try:
    #         c = self.conn.cursor()
    #         c.execute(create_table_sql)
    #     except Error as e:
    #         print(e)

    # def create_ingredient(self,item):
    #     sql = f''' UPDATE ingredient SET 
    #                 name = '{item['ingredient']}'
    #             WHERE id = {item['id']} '''
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     self.conn.commit()
    #     return cur.lastrowid




    # def add_cocktail(self,item):
    #     sql = f''' INSERT INTO cocktail(name,price,imagename)
    #             VALUES('{item['name']}', {item['price']},'{item['imagename']}') '''
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     self.conn.commit()
    #     cocktail_id = cur.lastrowid
    #     for ingredient in item['ingredients']:
    #         sql = f''' INSERT INTO cocktail_ingredient(cocktail_id,ingredient_id,amount)
    #             VALUES({cocktail_id}, {ingredient.ingredient_id}, {ingredient.amount}) '''
    #         cur = self.conn.cursor()
    #         cur.execute(sql)
    #         self.conn.commit()
    #     return cocktail_id

    # def all_ingredients(self):
    #     sql = ''' SELECT * FROM ingredient '''
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     rows = cur.fetchall()
    #     ingredients = [{
    #         'id' : r[0],
    #         'ingredient' : r[1],
    #     } for r in rows]
    #     return ingredients

    # def all_cocktails(self):
    #     sql = ''' SELECT * FROM cocktail
    #             INNER JOIN cocktail_ingredient
    #             ON cocktail_ingredient.cocktail_id = cocktail.id
    #             INNER JOIN ingredient
    #             ON cocktail_ingredient.ingredient_id = ingredient.id
    #      '''
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     rows = cur.fetchall()
    #     cocktails = {}
    #     for r in rows:
    #         cocktails[r[0]] = {
    #             'name' : r[2],
    #             'price': r[1],
    #             'imagename' : r[3],
    #             'ingredients' : []
    #         }
    #     for r in rows:
    #         cocktails[r[0]]['ingredients'].append({
    #             'id' : r[7],
    #             'ingredient' : r[8],
    #             'amount' : r[6]
    #         })
    #     return cocktails

    # def cocktails_with_ingredients(self,cocktail_ids):
    #     id_list_query = '('
    #     for i in range(0,len(cocktail_ids)):
    #         id_list_query += f'{cocktail_ids[i]})' if i == len(cocktail_ids)-1 else f'{cocktail_ids[i]},'
    #     sql = f'''select c.name,c.price,c.imagename, ci.amount, i.ingredient from cocktail as c inner join cocktail_ingredient as ci on ci.cocktail_id = c.id inner join ingredient as i on ci.ingredient_id = i.id  where c.id in {id_list_query} order by c.name;'''
    #     cur = self.conn.cursor()
    #     cur.execute(sql)
    #     rows = cur.fetchall()
    #     cocktails_obj = {}
    #     for r in rows:
    #         with open(f'assets/{r[2]}', "rb") as img_file:
    #             image_base64 = base64.b64encode(img_file.read())
    #         cocktails_obj[r[0]] = {
    #             'name' : r[0],
    #             'price': r[1],
    #             'imagename' : r[2],
    #             'ingredients' : [],
    #             'image_base64' : image_base64.decode(),
    #         }
    #     for r in rows:
    #         cocktails_obj[r[0]]['ingredients'].append({
    #             'amount' : r[3],
    #             'ingredient' : r[4],
    #         })
    #     cocktails_as_list = [ cocktails_obj[key] for key in cocktails_obj.keys()]
    #     return cocktails_as_list

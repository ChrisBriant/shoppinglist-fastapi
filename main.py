from typing import Union, List

from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app_database import Database
import os, dotenv

app = FastAPI()
basedir = os.path.abspath(os.path.dirname(__file__))




# origins = [
#     "http://localhost:3000",
# ]

origins=['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


dotenv_file = os.path.join(basedir, ".env")
if os.path.isfile(dotenv_file):
    dotenv.load_dotenv(dotenv_file)

print('HELLO',os.environ)

# LINODE_BUCKET=os.environ.get('LINODE_BUCKET')
# LINODE_BUCKET_REGION=os.environ.get('LINODE_BUCKET_REGION')
# LINODE_BUCKET_ACCESS_KEY=os.environ.get('LINODE_BUCKET_ACCESS_KEY') 
# LINODE_BUCKET_SECRET_KEY=os.environ.get('LINODE_BUCKET_SECRET_KEY') 
# LINODE_CLUSTER_URL='https://eu-central-1.linodeobjects.com'


#Database
#DATABASE_PATH = r"./cocktails.db"

#Models

class Item(BaseModel):
    name: str
    qty: int

class DBItem(BaseModel):
    id : int
    name: str
    qty: int

class ShoppingList(BaseModel):
    items: List[DBItem]

class ItemResponse(BaseModel):
    success: bool
    item: DBItem



@app.get("/shopping/getlist",response_model=ShoppingList)
def get_shopping_list():
    db_conn = Database()
    items = db_conn.get_list()
    shopping_list = {'items':items}
    return shopping_list

#DELETE
@app.delete("/shopping/deleteitem")
def delete_item(id: int, response: Response):
    db_conn = Database()
    rows_deleted = db_conn.delete_item(id)
    if rows_deleted > 0:
        response.status_code = 200
    else:
        response.status_code = 204
    return

#UPDATE METHODS

@app.put("/shopping/updateitem", response_model=ItemResponse)
def update_item(item: DBItem):
    db_conn = Database()
    rows_changed = db_conn.update_item(item)
    print('ROWS CHANGED', rows_changed)
    if rows_changed < 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"success": True, "item": item}

#CREATE METHODS
@app.post("/shopping/additem", response_model=ItemResponse)
def add_item(item: Item):
    db_conn = Database()

    id = db_conn.add_item(item)
    added_item = {
        'id' : id,
        'name' : item.name,
        'qty' : item.qty
    }
    return {"success": True, "item": added_item}

# @app.post('/cocktails/createpdf/',response_model=PDFDownloadResponse)
# def create_pdf(cocktail_ids: List[int]):
#     #Get the cocktails from the database
#     db_conn = Database(DATABASE_PATH)
#     #success= 1
#     context = {
#         'cocktail_list' : db_conn.cocktails_with_ingredients(cocktail_ids)
#     }
#     #Code below will generate the PDF
#     template_loader =  jinja2.FileSystemLoader('./')
#     template_env = jinja2.Environment(loader=template_loader)
    
#     template = template_env.get_template('pdf_template.html')
#     output_text = template.render(context)
#     f = open("htmltest.html", "w")
#     f.write(output_text)
#     f.close()

#     #Create the file name
#     filename = hex(random.getrandbits(128)) + '.pdf'

#     #UNCOMMENT TO CREATE PDF
#     config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')
#     pdfkit.from_string(output_text,filename,configuration=config,css='style.css',options={"enable-local-file-access": ""})

#     #TRANSFER TO STORAGE
#     linode_obj_config = {
#         "aws_access_key_id":AWS_ACCESS_KEY_ID,
#         "aws_secret_access_key": AWS_SECRET_ACCESS_KEY,
#         "endpoint_url": LINODE_CLUSTER_URL,
#     }
#     client = boto3.client("s3", **linode_obj_config)

#     data = open(filename, 'rb')
#     response = client.put_object(Body=data,  
#                                     Bucket=AWS_STORAGE_BUCKET_NAME,
#                                     Key=filename,
#                                     ACL='public-read')
#     print(response)
#     os.remove(filename) 
#     return { 'download_url' : f'{AWS_S3_ENDPOINT_URL}/{filename}' }
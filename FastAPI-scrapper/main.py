from fastapi import FastAPI
from fastapi.responses import JSONResponse
from bggranks import process_boardgame_data, process_csv_file
import csv
import os
from models import SessionLocal, Base, Item, Product

app = FastAPI()


@app.get("/")
async def root():   
        result = "hello world"      
        return {"message": result}
   

    
@app.get("/fetch")
async def fetch():
        await process_boardgame_data()
        result = "completed"
        return {"message": result}
  

@app.get("/display")
async def display():
        file_path = os.path.join(os.path.dirname(__file__), "RelevantParsedData.csv")
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)  # Assuming the first row is the header
            data = [dict(zip(header, row)) for row in reader]
        return JSONResponse(content=data)

# @app.get("/database")
# async def database():
#     db = SessionLocal()
#     products = db.query(Product).all()
#     db.close()

# # Convert the list of items to a list of dictionaries
#     product_dict_list = [{"id": product.id, "name": product.name, "image1": product.image1} for product in products]

#     return {"items": product_dict_list}



@app.get("/insert")
async def insert():
        process_csv_file()
        result = "completed"
        return {"message": result}



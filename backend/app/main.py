from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import pandas as pd
from io import BytesIO
from app.db.dependencies import get_db
from sqlalchemy.orm import Session
from app.schemas import DatasetResponse
from .models.Dataset import Dataset
import uuid
import os


app = FastAPI()

@app.get('/inico')
def inicio():
    return 'Inicio'


ALLOWED_EXTENSION = '.csv'

@app.post('/datasets/', response_model=DatasetResponse)
async def upload_file(file: UploadFile = File(),db: Session = Depends(get_db)) -> dict:
    content = await file.read()
    if not file.filename.lower().endswith(ALLOWED_EXTENSION):
        raise HTTPException(status_code=400, detail="Debe ser un archivo .csv")
    
    try:
        df = pd.read_csv(BytesIO(content))
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file")
    
    file_id = uuid.uuid4()
    file_path = f"uploads/{file_id}_{file.filename}" 
    new_file = Dataset( filename=file.filename,
                        file_path=file_path,
                        rows=df.shape[0],
                        columns=df.shape[1],)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    os.makedirs("uploads", exist_ok=True)
    with open(file_path, 'wb') as content_binary:
        content_binary.write(content)
    return {'id': new_file.id, 'filename': new_file.filename,'file_path': new_file.file_path, 'rows': new_file.rows,  'columns': new_file.columns, 'created_at': new_file.created_at}


@app.get('/datasets', response_model=DatasetResponse)
def get_datasets(db:Session= Depends(get_db)):
    datasets = db.query(Session).all()
    if not datasets:
        raise HTTPException(status_code=404, detail='No datasets')
    return datasets


@app.get('/dataset/{id}', response_model=DatasetResponse)
def get_dataset_by_id(id:int, db:Session= Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Dataset not found')
    return dataset



@app.get('/dataset/{id}/statics')
def get_statics(id:int, db:Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not dataset:
        raise HTTPException(status_code=400, detail='Dataset no encontrado')
    try:
        df = pd.read_csv(dataset.file_path)
    except pd.errors.ParserError:
        raise HTTPException(status_code=404, detail="Invalid CSV file")
    return {'Rows':df.shape[0], 'colums':df.shape[1],'statistics':df.describe().to_dict()}



@app.get('/datasets/{id}/missing-values')
def missing_values(id:int, db : Session = Depends(get_db)):
    dataset = db.query(Dataset).filter(Dataset.id == id).first()
    if not dataset:
        raise HTTPException(status_code=404, detail='Da6aset not found')
    try:
        df = pd.read_csv(dataset.file_path)
    except pd.errors.ParserError:
        raise  HTTPException(status_code=404, detail="Invalid CSV file")
    return  df.isnull().sum().to_dict()


'''
Dataset ID
    ↓
Buscar Dataset en PostgreSQL
    ↓
Obtener file_path
    ↓
pd.read_csv(...)
    ↓
df.isnull().sum()
    ↓
Convertir a diccionario
    ↓
JSON
'''

    
    

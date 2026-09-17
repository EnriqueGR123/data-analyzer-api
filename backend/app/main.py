from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
app = FastAPI()

@app.get('/inico')
def inicio():
    return 'Inicio'


ALLOWED_EXTENSION = '.csv'

@app.post('/datasets/')
async def upload_file(file: UploadFile = File()) -> dict:
    content = await file.read()
    if not file.filename.lower().endswith(ALLOWED_EXTENSION):
        raise HTTPException(status_code=400, detail="debe ser un archivo .csv",)
    try:
        df = pd.read_csv(BytesIO(content))
    except  pd.errors.ParserError:
        raise HTTPException(status_code=400, detail='Invalid CSV file')
    return {'Name': file.filename, 
            'Filas': df.shape[0],
            'Columnas': df.shape[1],
            'Nombres_columnas': df.columns.to_list(),
            'Detalles': df.head().to_json()}



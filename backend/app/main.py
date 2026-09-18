from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
import pandas as pd
from io import BytesIO
from app.db.dependencies import get_db
from sqlalchemy.orm import Session
from .models.Dataset import Dataset
app = FastAPI()

@app.get('/inico')
def inicio():
    return 'Inicio'


ALLOWED_EXTENSION = '.csv'



@app.post('/datasets/')
async def upload_file(file: UploadFile = File(), db: Session = Depends(get_db)) -> dict:
    content = await file.read()
    if not file.filename.lower().endswith(ALLOWED_EXTENSION):
        raise HTTPException(status_code=400, detail="debe ser un archivo .csv",)
    try:
        df = pd.read_csv(BytesIO(content))
    except  pd.errors.ParserError:
        raise HTTPException(status_code=400, detail='Invalid CSV file')
    new_file = Dataset(filename = file.filename, 
                        rows = df.shape[0],
                        columns= df.shape[1],)
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    file_path = 'uploads/' + str(new_file.id) +'_'+ new_file.filename
    with open (file_path, 'wb') as content_binary:
        content_binary.write(content)
    new_file.file_path = file_path
    db.commit()
    
    return {'id':new_file.id,'filename': new_file.filename, 'rows': new_file.rows, 'columns': new_file.columns, 'created_at': new_file.created_at}


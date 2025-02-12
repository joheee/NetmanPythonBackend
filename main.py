from typing import Union
from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def read_root():
    psexec_command = r'start explorer'
    process = subprocess.Popen(psexec_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    return {"result": process.returncode}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
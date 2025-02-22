from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import uvicorn
from pypsexec.client import Client

app = FastAPI()

class CommandRequest(BaseModel):
    command:str


@app.post("/")
def execute_command(request: CommandRequest):

    client = Client("10.21.45.187", username=".\\adminHD1", password="HD1intelsp")
    client.connect()
    client.create_service()
    stdout, stderr, rc = client.run_executable("cmd.exe", arguments=f"/c {request.command}")
    client.remove_service()
    client.disconnect()

    return {
        "return_code":rc,
        "command":request,
        "output":stdout.decode(),
        "error":stderr.decode()
    }

@app.post("/psexec")
def execute_command(request: CommandRequest):

    command_bind = f"C:\Windows\System32\PsExec.exe -h \\10.21.45.187 -u testuser -p testuser -i 1 cmd /c {request.command}"

    process = subprocess.Popen(command_bind, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return {
        "return_code":process.returncode,
        "command":command_bind,
        "output":stdout.decode(),
        "error":stderr.decode(),
    }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="localhost", port=8000)

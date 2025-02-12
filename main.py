from typing import Union
from fastapi import FastAPI, Query, HTTPException
import subprocess
import uvicorn

app = FastAPI()

ALLOWED_COMMANDS = {
    "explorer": "start explorer",
    "ping": "ping 127.0.0.1",
    "ipconfig": "ipconfig",
    "shutdown": "shutdown -r -t 0",
}

@app.get("/")
def execute_command(cmd: str = Query("explorer", description="Allowed commands: explorer, ping, ipconfig")):
    if cmd not in ALLOWED_COMMANDS:
        raise HTTPException(status_code=400, detail="Invalid command")

    process = subprocess.Popen(ALLOWED_COMMANDS[cmd], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    return {
        "command": cmd,
        "return_code": process.returncode,
        "stdout": stdout.decode(),
        "stderr": stderr.decode() if stderr else None
    }

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="localhost", port=8000)

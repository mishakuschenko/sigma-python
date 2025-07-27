from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import subprocess

app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")
templates = Jinja2Templates(directory="../frontend/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/run")
async def run_code(request: Request):
    data = await request.json()
    code = data.get("code", "")

    try:
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=30  # Защита от бесконечных циклов
        )
        output = result.stdout or result.stderr
        return {"output": output}
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=400, detail="Timeout: код выполняется слишком долго")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

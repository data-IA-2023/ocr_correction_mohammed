from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")



@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
    

if __name__ == "__main__":
    import uvicorn
    from controler import app  # Importez l'instance de l'application FastAPI depuis controler.py
    uvicorn.run(app, host="127.0.0.1", port=8000)  # Exécutez l'application FastAPI avec uvicorn

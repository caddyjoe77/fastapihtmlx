from typing import Optional
from fastapi import FastAPI, Request, Header
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from .database import SessionLocal, engine
from . import models

#note: normally you'd want to use migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="sql_app/templates")

@app.get("/index/", response_class=HTMLResponse)
async def movielist(request: Request, hx_request: Optional[str] = Header(None)): #hx-request
    films = [
        {'name': 'Blade Runner', 'director': 'Ridley Scott'},
        {'name': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
        {'name': 'Mulholland Drive', 'director': 'David Lynch'},
    ]
    context = {'request': request, 'films': films}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)
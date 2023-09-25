from typing import Optional
from fastapi import FastAPI, Request, Header, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models

#note: normally you'd want to use migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="sql_app/templates")

# Dependency for SQL Sessions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
def startup_populate_db():
    db = SessionLocal()
    num_films = db.query(models.Film).count()
    if num_films == 0:
        films = [
            {'name': 'Blade Runner', 'director': 'Ridley Scott'},
            {'name': 'Pulp Fiction', 'director': 'Quentin Tarantino'},
            {'name': 'Mulholland Drive', 'director': 'David Lynch'},
            {'name': 'Jurassic Park', 'director': 'Steven Spielberg'},
            {'name': 'Tokyo Story', 'director': 'Yasujiro Ozu'},
            {'name': 'Chunking Express', 'director': 'Kar-Wai Wong'},
        ]
        for film in films:
            db.add(models.Film(**film))
        db.commit()
        db.close()
    else:
        print(f"{num_films} already in DB!")



@app.get("/index/", response_class=HTMLResponse)
async def movielist(
        request: Request,
        hx_request: Optional[str] = Header(None),
        db: Session = Depends(get_db),page: int = 1): #hx-request

    N = 2
    OFFSET = (page -1) * N  #for the pagination
    films = db.query(models.Film).offset(OFFSET).limit(N)
    context = {'request': request, 'films': films, 'page': page}
    if hx_request:
        return templates.TemplateResponse("table.html", context)
    return templates.TemplateResponse("index.html", context)
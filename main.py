from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # return {"message": "Hello World"}
    return templates.TemplateResponse(
        request=request, name="index.html", context={"id": id}
    )

@app.get("/albums/{album_uuid}", response_class=HTMLResponse)
async def root(request: Request, album_uuid:str):
    # return {"message": "Hello World"}
    return templates.TemplateResponse(
        request=request, name="edit-metadata.html", context={"album_uuid": album_uuid}
    )

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

templates = Jinja2Templates(directory="templates")

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str):
    return templates.TemplateResponse(
        request=request, name="item.html",  context={"id": id}
    )

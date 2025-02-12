from fastapi import FastAPI, Request, Response, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import uuid

from immich.ImmichClient import ImmichClient

# FastAPI app
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# SQLite Database Setup
DATABASE_URL = "sqlite:///./db.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Database Model
class Album(Base):
    __tablename__ = "albums"
    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, index=True)

# Create the database tables
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@app.get("/", response_class=HTMLResponse)
async def root(request: Request, db: Session = Depends(get_db)):
    # albums = db.query(Album).all()
    c = ImmichClient('http://localhost:2283/', "xnFmvnF4E2ijDXZPbCL8LjJm8kbdSwe85EvzD5VZA")
    all_albums = c.list_albums()
    a = all_albums[0]

    thumb = f"/asset/{a['albumThumbnailAssetId']}/thumb"
    print(a)
    return templates.TemplateResponse(
        request=request, name="index.html", context={
            "albums": [],
            "album_thumbnail": thumb,
            "album_name": a['albumName'],
            "album_uuid": a['id']
        }
    )

@app.get("/asset/{asset_uuid}/thumb")
async def root(request: Request, asset_uuid: str, db: Session = Depends(get_db)):
    c = ImmichClient('http://localhost:2283/', "xnFmvnF4E2ijDXZPbCL8LjJm8kbdSwe85EvzD5VZA")
    r = c.get_thumbnail(asset_uuid)
    return Response(content=r.content)


@app.get("/albums/{album_uuid}", response_class=HTMLResponse)
async def get_album(request: Request, album_uuid: str, db: Session = Depends(get_db)):
    album = db.query(Album).filter(Album.id == album_uuid).first()
    # if not album:
    #     raise HTTPException(status_code=404, detail="Album not found")

    c = ImmichClient('http://localhost:2283/', "xnFmvnF4E2ijDXZPbCL8LjJm8kbdSwe85EvzD5VZA")
    all_albums = c.list_albums()
    a = all_albums[0]

    thumb = f"/asset/{a['albumThumbnailAssetId']}/thumb"

    return templates.TemplateResponse(
        request=request, name="edit-metadata.html", context={
            "albums": [],
            "album_thumbnail": thumb,
            "album_uuid": a['id']
        }
    )

@app.post("/albums/", response_model=dict)
async def create_album(title: str, db: Session = Depends(get_db)):
    new_album = Album(title=title)
    db.add(new_album)
    db.commit()
    db.refresh(new_album)
    return {"id": new_album.id, "title": new_album.title}

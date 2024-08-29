from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request

app = FastAPI()

# Mount the static directory to serve CSS, JS, images, etc.
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Set up the Jinja2 template directory
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("dash.html", {"request": request})

@app.get("/secondary", response_class=HTMLResponse)
async def display_secondary(request: Request):
    return templates.TemplateResponse("secondary.html", {"request": request})

@app.get("/test")
async def test():
    return {"message": "Test route works!"}

from .routes import users, tasks

app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

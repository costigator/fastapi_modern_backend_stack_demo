from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

webapp_router = APIRouter(include_in_schema=False)

templates = Jinja2Templates(directory="templates")

@webapp_router.get("/")
def home(request: Request):
    print(dir(request))
    return templates.TemplateResponse("homepage.html", {"request": request})
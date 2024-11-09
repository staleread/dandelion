from fastapi.templating import Jinja2Templates


directory = "templates/web"

TemplateResponse = Jinja2Templates(directory=directory).TemplateResponse

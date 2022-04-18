import panel as pn
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from bokeh.embed import server_session, server_document
from bokeh.util.token import generate_session_id
import logging
import uvicorn

from panelApps.pn_app import createApp

app = FastAPI()

#setup for static resources
app.mount("/static",StaticFiles(directory='static'),name='static')
templates = Jinja2Templates(directory="static/templates")

SECRET_KEY = '{{cookiecutter.SECRET_KEY}}' #in a real system; swap this with a secret key outside of your source code
HOST_IP = '{{cookiecutter.HOST_IP}}'
PANEL_PORT = {{cookiecutter.PANEL_PORT}}
FASTAPI_PORT = {{cookiecutter.FASTAPI_PORT}}
PROJECT_NAME = '{{cookiecutter.PROJECT_NAME}}'

logger = logging.getLogger('uvicorn.error')

@app.on_event("startup")
async def startup_event():
    '''
    add handler to the base uvicorn logger
    '''
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)
    logger.info("Started Logger")


@app.get("/")
async def bokeh_app_page(request: Request):
    '''
    Landing page template
    '''
    url = f'http://{HOST_IP}:{PANEL_PORT}/app'
    script = server_session(
        session_id=generate_session_id(SECRET_KEY, signed=True), url=url
    )

    return templates.TemplateResponse("base.html", {"request": request,"script":script,"PROJECT_NAME":PROJECT_NAME})

#launch bokeh server
panel_app = pn.serve({'/app': lambda :createApp().layout},
                        port=PANEL_PORT, 
                        address=f"{HOST_IP}",
                        allow_websocket_origin=[f"{HOST_IP}:{PANEL_PORT}"],
                        show=False,
                        secret_key = SECRET_KEY,
                        sign_sessions = True,
                        generate_session_ids=True,
                        num_process = 3)

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST_IP, port=FASTAPI_PORT, log_level="info")
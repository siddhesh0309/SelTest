from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from seleniums_auto import start_selenium_automation
from fastapi.responses import FileResponse
from fastapi import HTTPException

app = FastAPI()

# Serve the "static" directory where your HTML file resides
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=FileResponse)
def get_form_page():
    # Serve the HTML file when hitting the root URL
    return FileResponse("static/index.html")


@app.get("/start-automation")
def start_automation(from_date: str = None, to_date: str = None):
    try:
        message = start_selenium_automation(from_date, to_date)
        return {"message": message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

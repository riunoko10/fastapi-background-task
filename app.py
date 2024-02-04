from fastapi import FastAPI, Request, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import uvicorn
from typing import Annotated


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/files/")
async def create_files(files: Annotated[list[bytes], File()]):
    return {"file_sizes": [len(file) for file in files]}



@app.post("/uploadfiles/")
async def create_upload_files(file: UploadFile, background_tasks: BackgroundTasks):
    if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    with open(file.filename, "wb") as buffer:
        buffer.write(file.file.read())
        buffer.close()
    
    background_tasks.add_task(write_notification, file.filename, message="some notification")
    return {"message": "Notification sent in the background"}


@app.get("/")
async def main():
    content = """
<body>
<form action="/uploadfiles/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)




if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
from fastapi import FastAPI
from api.routes import users,auth,password_reset,blog_content,user_detail
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
template=Path(__file__).parent / 'templates'


app=FastAPI()
app.mount("/templates", StaticFiles(directory="api/templates"), name="templates")
@app.get("/")
async def root():

    return FileResponse(f'{template}/index.html')


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(password_reset.router)
app.include_router(blog_content.router)
app.include_router(user_detail.router)

from fastapi import FastAPI

from app.books.routes import router_books
from app.users.routes import router as router_users


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "It's me, Mario!"
        }


app.include_router(router_books)
app.include_router(router_users)

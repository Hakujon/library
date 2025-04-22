from fastapi import FastAPI

from app.books.routes import router_books


app = FastAPI()


@app.get("/")
async def root():
    return {
        "message": "It's me, Mario!"
        }


app.include_router(router_books)



from fastapi import FastAPI
from routes import router

app = FastAPI(
    title="Trading App"
)


app.include_router(router)



from fastapi import FastAPI
from authroutes import authrouter
from interfacerouts import interfacerouter, reload_book_bd_id

app = FastAPI(
    title="Trading App"
)

@app.on_event("startup")
def startup_event():
    reload_book_bd_id()


app.include_router(authrouter)
app.include_router(interfacerouter)
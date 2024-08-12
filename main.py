from fastapi import FastAPI

from auth.views import router as auth_router
from user.views import router as users_router
from wallet.views import router as wallet_router

app = FastAPI()


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
app.include_router(users_router, prefix="/users", tags=["users"])


# for development purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

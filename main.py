from fastapi import FastAPI

from auth.containers import UserContainer
from auth.views import router as auth_router
from user.views import router as users_router
from wallet.views import router as wallet_router

app = FastAPI()
container = UserContainer()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(wallet_router, prefix="/wallet", tags=["wallet"])
app.include_router(users_router, prefix="/users", tags=["users"])
app.container = container


# for development purposes
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

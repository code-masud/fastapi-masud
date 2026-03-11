from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth_router, post_router, user_router, like_router

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/')
def root():
    return {'message': 'hello world!'}


app.include_router(user_router.router)
app.include_router(auth_router.router)
app.include_router(post_router.router)
app.include_router(like_router.router)

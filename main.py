import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from login_router import auth_api_router


app = FastAPI(debug=True)

origins = [
    "http://localhost.proxyman.io:8002/",
    "http://localhost:5173",
    "http://localhost",
    "http://localhost:3000",
    "http://10.9.2.96",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_api_router)


if __name__ == '__main__':
    uvicorn.run(app,host="0.0.0.0", port=80)
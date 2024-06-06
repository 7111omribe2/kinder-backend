from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from login_router import auth_api_router


app = FastAPI(debug=True)
FastAPIInstrumentor.instrument_app(app)

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



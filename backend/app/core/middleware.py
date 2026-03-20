import time
import uuid
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

BLACK_LIST = {""}

def register_middelware(app: FastAPI):

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    
    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start= time.perf_counter()
        response= await call_next(request)
        process_time= time.perf_counter() - start
        response.headers["X-Process-Time"] = f"{process_time:.4f} s"
        return response

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        print(f"**Entrada: {request.method} {request.url}")
        response = await call_next(request)
        print(f"**Salida: {response.status_code} **")
        return response

    @app.middleware("http")
    async def add_request_id_header(request: Request, call_next):
        request_id = str(uuid.uuid4())
        response = await call_next(request)
        response.headers["x-Request-ID"] = request_id
        return response

    @app.middleware("http")
    async def block_ip__middleware(request: Request, call_next):
        client_ip = request.client.host
        if client_ip in BLACK_LIST:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado a esta IP"
            )
        return await call_next(request)

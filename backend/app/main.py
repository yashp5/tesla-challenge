import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import metrics_router, data_router, site_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(metrics_router, prefix="/metrics", tags=["metrics"])
app.include_router(data_router, prefix="/data", tags=["data"])
app.include_router(site_router, prefix="/site", tags=["site"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.trips import router as trips_router

app = FastAPI(title="TripSplit")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trips_router)


@app.get("/")
def root():
    return {"message": "TripSplit API"}

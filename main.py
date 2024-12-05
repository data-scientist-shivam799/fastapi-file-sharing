import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from app.database import Base, engine
from app.routes import ops_user, client_user

# Initialize the FastAPI application
app = FastAPI()

# Bind the database models
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(ops_user.router, prefix="/ops", tags=["Ops User"])
app.include_router(client_user.router, prefix="/client", tags=["Client User"])

@app.get("/")
async def root():
    return JSONResponse(content={
        "message": "Welcome to the Secure File Sharing System"
    }, status_code=status.HTTP_200_OK)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

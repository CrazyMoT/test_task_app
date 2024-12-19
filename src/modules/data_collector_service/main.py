from fastapi import FastAPI
from routes import sales
import uvicorn

app = FastAPI()

app.include_router(sales.router, prefix="/sales", tags=["sales"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5001)
from fastapi import FastAPI
from schemas import TaxPayer
from service import run_workflow
import uvicorn

app = FastAPI()

@app.get("/health")
async def ping():
    return {"status": "ok"}

@app.post("/taxpayer")
async def register_taxpayer(taxpayer: TaxPayer) :
    print(taxpayer.model_dump())
    await run_workflow(taxpayer)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

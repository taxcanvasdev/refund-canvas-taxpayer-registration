from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/hello")
async def hello():
    return "hello"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

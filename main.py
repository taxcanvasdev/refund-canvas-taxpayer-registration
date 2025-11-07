from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
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
    
    message = await run_workflow(taxpayer)
    status_code = 200
    
    # already_registered_phrases = ("해임일자는 신고기간 이내에만 가능합니다.", "수임일자는 이전해임일 이후 이여야 합니다.")
    # is_already_registered = isinstance(message, str) and any(phrase in message for phrase in already_registered_phrases)
    # if is_already_registered :
    #     status_code = 400
    #     message = "이미 등록되어있는 신고대리납세자 입니다."
    
    error_phrases = ("올바르지 않습니다.", "입력해야합니다.")
    has_error = isinstance(message, str) and any(phrase in message for phrase in error_phrases)
    if has_error :
        status_code = 400
        message = "주민등록번호 또는 사업자등록번호가 옳지 않습니다."
    
    if status_code == 200 :
        message = "등록되었습니다."
        
    return PlainTextResponse(status_code=status_code, content=message or "")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5100)

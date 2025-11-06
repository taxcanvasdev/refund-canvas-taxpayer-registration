from service.hometax_login import login_hometax_with_certificate
from service.taxpayer_registration import register_taxpayer
from schemas import TaxPayer
import time

async def safe_goto(page, context, url):
    """홈택스 팝업 감지 후 닫고, 지정 URL로 이동"""
    # 팝업 감시 이벤트 핸들러
    popup_pages = []

    async def on_popup(popup):
        popup_pages.append(popup)
        popup_url = popup.url
        if "websquare" in popup_url:
            print(f"팝업 감지됨: {popup_url}, 닫습니다.")
            await popup.close()

    # 팝업 감시 등록
    context.on("page", on_popup)

    # 이미 열린 팝업이 있는 경우 닫기
    for p in context.pages:
        if "websquare" in p.url and p != page:
            print(f"기존 팝업 닫기: {p.url}")
            await p.close()

    # 페이지 이동 시도
    try:
        await page.goto(url, wait_until="networkidle")
    except Exception as e:
        print("이동 중 오류 발생:", e)

    print("✅ 팝업 처리 후 정상 이동 완료")

async def run_workflow(taxpayer : TaxPayer) :
    
    p, browser, context, page = await login_hometax_with_certificate()

    # 팝업 차단 포함 이동
    await safe_goto(page, context, "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&tmIdx=48&tm2lIdx=4804000000&tm3lIdx=4804050000")

    # 혹시 남은 팝업이 있으면 닫기
    page.on("popup", lambda popup: popup.close())

    # ✅ register_taxpayer 내부에서 페이지 안정화까지 기다림
    await register_taxpayer(page, taxpayer)
    
    print("\n브라우저가 열려 있습니다. Ctrl+C를 눌러 종료하세요.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n종료 중...")
        await browser.close()
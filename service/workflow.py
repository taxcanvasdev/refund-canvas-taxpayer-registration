from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page
from service.hometax_login import login_hometax_with_certificate
from service.taxpayer_registration import register_taxpayer
from utils.close_popup import close_popup
from schemas import TaxPayer
import time

async def init_resources() -> tuple[Playwright, Browser, BrowserContext, Page]:
    # playwright 실행 컨텍스트
    playwright : Playwright = await async_playwright().start()
    # 하나의 브라우저 인스턴스
    browser : Browser = await playwright.chromium.launch(headless=True)
    # 브라우저 세션 컨텍스트 (다운로드 허용)
    context : BrowserContext = await browser.new_context(accept_downloads=True,  downloads_path="/home/taxcanvasdev")
    # 단일 탭(세션, 쿠키, DOM 포함)
    page : Page = await browser.new_page()

    return playwright, browser, context, page

async def clean_resources(playwright: Playwright, browser: Browser, context: BrowserContext, page: Page):
    try: 
        await page.close()
        await context.close()
        await browser.close()
        await playwright.stop()
    except Exception as e:
        print(f"clean resources 중 오류: {e}")

async def run_workflow(taxpayer : TaxPayer) :

    playwright, browser, context, page = await init_resources()
    
    page = await login_hometax_with_certificate(page)

    # 팝업 차단 포함 이동
    await close_popup(page, context, "https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&tmIdx=48&tm2lIdx=4804000000&tm3lIdx=4804050000")
    # 혹시 남은 팝업이 있으면 닫기
    page.on("popup", lambda popup: popup.close())

    await register_taxpayer(page, taxpayer)
    
    print("\n브라우저가 열려 있습니다. Ctrl+C를 눌러 종료하세요.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        await clean_resources(playwright, browser, context, page)
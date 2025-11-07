from playwright.async_api import async_playwright, Playwright, Browser, BrowserContext, Page
from service.hometax_login import login_hometax_with_certificate
from service.taxpayer_registration import register_taxpayer
from schemas import TaxPayer
import time
import asyncio

async def init_resources() -> tuple[Playwright, Browser, BrowserContext, Page, list[str]]:
    # Playwright 실행 컨텍스트
    playwright: Playwright = await async_playwright().start()
    # Chrome 브라우저 인스턴스 실행 (시스템 Chrome 사용)
    browser: Browser = await playwright.chromium.launch(
        channel="chrome",  # 시스템에 설치된 Chrome 사용
        headless=False,
        args=[
            '--disable-features=PrivacySandboxSettings4',  # 권한 프롬프트 비활성화
            '--disable-blink-features=AutomationControlled',  # 자동화 감지 방지
            '--use-fake-ui-for-media-stream',  # 미디어 스트림 UI 자동 허용
            '--disable-web-security',  # 웹 보안 비활성화 (로컬 네트워크 접근)
            '--allow-running-insecure-content',  # 안전하지 않은 콘텐츠 허용
            '--disable-features=IsolateOrigins,site-per-process',  # 오리진 격리 비활성화
            '--disable-site-isolation-trials',  # 사이트 격리 시험 비활성화
            '--unsafely-treat-insecure-origin-as-secure=https://hometax.go.kr',  # 홈택스를 안전한 오리진으로 처리
        ]
    )
    # 브라우저 세션 컨텍스트
    context: BrowserContext = await browser.new_context(
        permissions=['notifications', 'geolocation', 'camera', 'microphone'],  # 권한 자동 허용
        bypass_csp=True,  # Content Security Policy 우회
    )
    # 로컬 네트워크 권한 부여
    await context.grant_permissions(['notifications', 'geolocation'])
    
    # 단일 탭 (세션, 쿠키, DOM 포함)
    page: Page = await context.new_page()
    
    dialog_messages: list[str] = []

    # 권한 요청 다이얼로그 자동 허용 처리
    async def handle_permission_dialog(dialog):
        print("============== [ DIALOG POPUP ] ==============")
        print(f"MESSAGE: {dialog.message}")
        await dialog.accept()
        dialog_messages.append(dialog.message) # 다이얼로그 메시지 누적 저장
        print("자동 수락 버튼 클릭 완료!")
    
    # 다이얼로그 이벤트 리스너 등록
    page.on("dialog", lambda dialog: asyncio.create_task(handle_permission_dialog(dialog)))

    return playwright, browser, context, page, dialog_messages

async def clean_resources(playwright: Playwright, browser: Browser, context: BrowserContext, page: Page):
    try: 
        await page.close()
        await context.close()
        await browser.close()
        await playwright.stop()
    except Exception as e:
        print(f"clean resources 중 오류: {e}")

async def run_workflow(taxpayer : TaxPayer) -> str | None :

    playwright, browser, context, page, dialog_messages = await init_resources()
    
    await login_hometax_with_certificate(page)
    await register_taxpayer(page, taxpayer)
    
    print("============= 누적된 메시지 =============")
    for m in dialog_messages:
        print(m)
        print()
    print("================ END ================")

    await clean_resources(playwright, browser, context, page)

    return dialog_messages[-1] if dialog_messages else None

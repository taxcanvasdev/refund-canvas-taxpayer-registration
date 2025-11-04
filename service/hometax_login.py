from playwright.async_api import async_playwright, Playwright, Browser, Page
from dotenv import load_dotenv
import asyncio
import os

# .env 파일에서 공동인증서 비밀번호 로드
load_dotenv()
CERTIFICATE_PW = os.getenv("CERTIFICATE_PW")
TAX_AGENT_ID = os.getenv("TAX_AGENT_ID")
TAX_AGENT_PW = os.getenv("TAX_AGENT_PW")

async def login_hometax_with_certificate() -> tuple[Playwright, Browser, Page]:
    """
    홈택스 공인인증서 페이지에 접근합니다.
    """

    # 공동인증서 비번 없다면 실행 X
    if not CERTIFICATE_PW:
        raise Exception("공동인증서 비밀번호 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.")

    if not TAX_AGENT_ID or not TAX_AGENT_PW :
        raise Exception("세무대리인 관리번호 및 비밀번호 관련 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.")
    
    # playwright 실행 컨텍스트
    p : Playwright = await async_playwright().start()
    # 하나의 브라우저 인스턴스
    browser : Browser = await p.chromium.launch(headless=False)
    # 단일 탭(세션, 쿠키, DOM 포함)
    page : Page = await browser.new_page()
        
    # 페이지로 이동
    print("페이지로 이동 중...")
    await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=index3", wait_until="domcontentloaded")
        
    # 페이지 로딩 대기
    print("페이지 로딩 대기 중...")
    await page.wait_for_load_state("networkidle", timeout=10000)
            
    # 로그인 버튼 클릭
    print("로그인 버튼 찾는 중...")
    login_button = page.locator("#mf_wfHeader_group1503")
    await login_button.wait_for(state="visible", timeout=10000)
    print("로그인 버튼 찾음. 클릭 중...")
    await login_button.click()
    print("로그인 버튼 클릭 완료!")
    # 로그인 버튼 클릭 후 다음 요소가 나타날 때까지 대기
    await page.wait_for_load_state("networkidle", timeout=5000)
        
    # 공인인증서 버튼 클릭
    print("공인인증서 버튼 찾는 중...")
    cert_button = page.locator("#mf_txppWframe_anchor22")
    await cert_button.wait_for(state="visible", timeout=10000)
    print("공인인증서 버튼 찾음. 클릭 중...")
    await cert_button.click()
    print("공인인증서 버튼 클릭 완료!")
    await page.wait_for_selector("#dscert", timeout=10000)
        
    # dscert iframe 찾기 및 접근
    print("공인인증서 iframe(#dscert) 찾는 중...")
    # frame_locator 사용 - iframe 내부 요소 접근에 최적화
    iframe_frame = page.frame_locator("#dscert")
    print("iframe 접근 완료!")  
    await asyncio.sleep(2)
        
    # 비밀번호 입력 필드 존재 확인 (iframe 내부에서)
    print("비밀번호 입력 필드(#input_cert_pw) 존재 확인 중...")

    try:
        # frame_locator로 요소가 존재하는지 확인
        input_field = iframe_frame.locator("#input_cert_pw")
        await input_field.wait_for(state="attached", timeout=5000)
        print("비밀번호 입력 필드 찾음!")
    except:
        print("오류: input_cert_pw 요소를 찾을 수 없습니다!")
        raise Exception("input_cert_pw 요소가 iframe 내부에 존재하지 않습니다.")
    
    print("비밀번호 입력 필드(#input_cert_pw)에 값 설정 중...")
    # name 속성을 사용하여 프레임 접근
    cert_frame = page.frame(name="dscert")
    if cert_frame:
        await cert_frame.evaluate('document.getElementById("input_cert_pw").value = "kalmasi908!+"')
        print("비밀번호 값 설정 완료!")
    else:
        raise Exception("iframe 프레임에 접근할 수 없습니다.")
    await asyncio.sleep(1)

    # 확인 버튼 클릭 (iframe 내부에서)
    print("확인 버튼(#btn_confirm_iframe) 찾는 중...")
    try:
        confirm_button = iframe_frame.locator("#btn_confirm_iframe")
        await confirm_button.wait_for(state="visible", timeout=10000)
        print("확인 버튼 찾음. 클릭 중...")
        await confirm_button.click()
        print("확인 버튼 클릭 완료!")
    except Exception as e:
        print(f"확인 버튼을 찾을 수 없습니다: {e}")
        raise
        
    # 팝업 확인 버튼 클릭 (세무대리인 확인 팝업)
    print("팝업 확인 버튼 찾는 중...")
    popup_confirm_button = page.locator('input[id^="mf_txppWframe_confirm"][id$="_wframe_btn_confirm"]')
    await popup_confirm_button.wait_for(state="visible", timeout=10000)
    print("팝업 확인 버튼 찾음. 클릭 중...")
    await popup_confirm_button.click()
    print("팝업 확인 버튼 클릭 완료!")
    # 팝업 확인 후 페이지가 로드될 때까지 대기
    await page.wait_for_load_state("networkidle", timeout=5000)
    
    id_input_box = page.locator("mf_txppWframe_input1")
    await id_input_box.wait_for(state="visible", timeout=10000)
    await id_input_box.fill(TAX_AGENT_ID)

    pw_input_box = page.locator("mf_txppWframe_input2")
    await pw_input_box.wait_for(state="visible", timeout=10000)
    await pw_input_box.fill(TAX_AGENT_PW)

    login_button = page.locator("mf_txppWframe_trigger41")
    await login_button.wait_for(state="visible", timeout=10000)
    await login_button.click()
 
    return p, browser, page
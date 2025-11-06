from playwright.async_api import Page
from dotenv import load_dotenv
import asyncio
import os

# .env 파일에서 공동인증서 비밀번호 로드
load_dotenv()
CERTIFICATE_PW = os.getenv("CERTIFICATE_PW")
TAX_AGENT_ID = os.getenv("TAX_AGENT_ID")
TAX_AGENT_PW = os.getenv("TAX_AGENT_PW")

async def login_hometax_with_certificate(page: Page) -> Page:
    """
    홈택스 공인인증서 페이지에 접근합니다.
    """
    # 공동인증서 비번 없다면 실행 X
    if not CERTIFICATE_PW:
        raise Exception("공동인증서 비밀번호 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.")

    if not TAX_AGENT_ID or not TAX_AGENT_PW :
        raise Exception("세무대리인 관리번호 및 비밀번호 관련 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.")

    # 페이지로 이동
    print("페이지로 이동 중...")
    await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&menuCd=index3", wait_until="domcontentloaded")
        
    # 페이지 로딩 대기
    print("페이지 로딩 대기 중...")
    await page.wait_for_load_state("networkidle", timeout=5000)
            
    # 로그인 버튼 클릭
    print("로그인 버튼 찾는 중...")
    login_button = page.locator("#mf_wfHeader_group1503")
    await login_button.wait_for(state="attached", timeout=3000)
    print("로그인 버튼 찾음. 클릭 중...")
    await login_button.click()
    print("로그인 버튼 클릭 완료!")
    # 로그인 버튼 클릭 후 다음 요소가 나타날 때까지 대기
    await page.wait_for_load_state("networkidle", timeout=5000)
        
    # 공인인증서 버튼 클릭
    print("공인인증서 버튼 찾는 중...")
    cert_button = page.locator("#mf_txppWframe_anchor22")
    await cert_button.wait_for(state="attached", timeout=3000)
    print("공인인증서 버튼 찾음. 클릭 중...")
    await cert_button.click()
    print("공인인증서 버튼 클릭 완료!")
    await page.wait_for_selector("#dscert", timeout=3000)
        
    # dscert iframe 찾기 및 접근
    print("공인인증서 iframe(#dscert) 찾는 중...")
    # frame_locator 사용 - iframe 내부 요소 접근에 최적화
    iframe_frame = page.frame_locator("#dscert")
    print("iframe 접근 완료!")  
    await asyncio.sleep(2)
    
    # iframe HTML 저장
    print("iframe HTML을 저장 중...")
    cert_frame = page.frame(name="dscert")
    if cert_frame:
        iframe_html = await cert_frame.content()
        iframe_html_path = "/home/taxcanvasdev/debug_iframe_dscert.html"
        with open(iframe_html_path, "w", encoding="utf-8") as f:
            f.write(iframe_html)
        print(f"iframe HTML 저장 완료: {iframe_html_path}")
    else:
        print("iframe에 접근할 수 없습니다.")
    
    # 스크린샷 저장 - iframe이 열린 상태
    screenshot_path = "/home/taxcanvasdev/screenshot_01_iframe_opened.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"스크린샷 저장 완료: {screenshot_path}")
        
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

    # table_element_locator = iframe_frame.locator("#row0dataTable > td > a > span")
    # html = await table_element_locator.evaluate("(el) => el.innerHTML")
    # print("공동인증서 이름:\n", html)
    
    # MSG_TS703 스팬 클릭 (공동인증서 선택)
    print("MSG_TS703 스팬 찾는 중...")
    msg_span = iframe_frame.locator("#MSG_TS703")
    await msg_span.wait_for(state="attached", timeout=3000)
    
    # 스크린샷 저장 - MSG_TS703 클릭 전
    screenshot_path = "/home/taxcanvasdev/screenshot_02_before_msg_ts703_click.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"스크린샷 저장 완료: {screenshot_path}")
    
    print("MSG_TS703 스팬 찾음. 클릭 중...")
    await msg_span.click()
    print("MSG_TS703 스팬 클릭 완료!")
    
    # 스크린샷 저장 - MSG_TS703 클릭 후
    await asyncio.sleep(10)
    screenshot_path = "/home/taxcanvasdev/screenshot_03_after_msg_ts703_click.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"스크린샷 저장 완료: {screenshot_path}")
    
    # 로딩이 완료될 때까지 충분히 대기
    print("팝업 로딩 대기 중...")
    await asyncio.sleep(3)  # 초기 로딩 대기
    
    # 페이지 HTML 전체 저장
    print("현재 페이지의 HTML을 저장 중...")
    html_content = await page.content()
    html_file_path = "/home/taxcanvasdev/debug_page.html"
    
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"HTML 파일 저장 완료: {html_file_path}")

    # iframe HTML 전체 저장
    print("현재 iframe의 HTML을 저장 중...")
    cert_frame = page.frame(name="dscert")
    if cert_frame:
        iframe_html_content = await cert_frame.content()
        iframe_html_file_path = "/home/taxcanvasdev/debug_iframe.html"
        with open(iframe_html_file_path, "w", encoding="utf-8") as f:
            f.write(iframe_html_content)
        print(f"iframe HTML 파일 저장 완료: {iframe_html_file_path}")
    else:
        print("iframe에 접근할 수 없습니다.")

    # Ubuntu 설치 팝업 처리 - 설치 스킵하고 진행
    print("Ubuntu 설치 팝업 처리 중...")
    
    if cert_frame:
        try:
            # 설치 플래그를 직접 false로 설정하여 설치 과정 스킵
            await cert_frame.evaluate("""
                () => {
                    // 설치 플래그를 false로 설정
                    if (typeof ML4WebApi !== 'undefined') {
                        ML4WebApi.setProperty("is_cs_install", false);
                        console.log("설치 플래그를 false로 설정 완료");
                    }
                    
                    // 설치 다이얼로그가 열려있으면 닫기
                    if ($("#ML_install").length > 0) {
                        $('#ML_install').MLjquiWindow('destroy');
                        console.log("설치 다이얼로그 닫기 완료");
                    }
                    
                    // 브라우저 스토리지 선택 (stg_web_kftc 클릭)
                    if ($("#stg_web_kftc").length > 0) {
                        $("#stg_web_kftc").click();
                        console.log("브라우저 스토리지 선택 완료");
                    }
                }
            """)
            print("설치 스킵 및 브라우저 스토리지 선택 완료!")
            
            # 스크린샷 저장 - 설치 스킵 후
            await asyncio.sleep(2)
            screenshot_path = "/home/taxcanvasdev/screenshot_04_after_install_skip.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            print(f"스크린샷 저장 완료: {screenshot_path}")
            
        except Exception as e:
            print(f"설치 스킵 실패: {e}, 계속 진행...")
    
    await asyncio.sleep(1)

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
        await confirm_button.wait_for(state="attached", timeout=3000)
        print("확인 버튼 찾음. 클릭 중...")
        await confirm_button.click()
        print("확인 버튼 클릭 완료!")
        
        # 스크린샷 저장 - 확인 버튼 클릭 직후
        screenshot_path = "/home/taxcanvasdev/screenshot_02_after_confirm_click.png"
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"스크린샷 저장 완료: {screenshot_path}")
        
        # 팝업이 나타날 때까지 대기
        await asyncio.sleep(2)
        
    except Exception as e:
        print(f"확인 버튼을 찾을 수 없습니다: {e}")
        raise
        
    # 팝업 확인 버튼 클릭 (세무대리인 확인 팝업)
    print("팝업 확인 버튼 찾는 중...")
    
    # 스크린샷 저장 - 팝업 버튼 찾기 전
    screenshot_path = "/home/taxcanvasdev/screenshot_03_before_popup_button.png"
    await page.screenshot(path=screenshot_path, full_page=True)
    print(f"스크린샷 저장 완료: {screenshot_path}")
    # await page.evaluate("""
    #     () => {
    #         const btn = document.querySelector('input[id^="mf_txppWframe_confirm"][id$="_wframe_btn_confirm"]');
    #         if (btn) btn.click();
    #     }
    # """)
    # popup_confirm_button = page.locator('input[id^="mf_txppWframe_confirm"][id$="_wframe_btn_confirm"]')
    popup_confirm_button = page.locator(".w2trigger.btn_cm.crud")
    await popup_confirm_button.wait_for(state="attached", timeout=3000)
    print("팝업 확인 버튼 찾음. 클릭 중...")
    await popup_confirm_button.click()
    print("팝업 확인 버튼 클릭 완료!")

    # 팝업 확인 후 페이지가 로드될 때까지 대기
    await page.wait_for_selector("#mf_txppWframe_input1", timeout= 5000)
    
    id_input_box = page.locator("#mf_txppWframe_input1")
    await id_input_box.wait_for(state="attached", timeout=3000)
    await id_input_box.fill(TAX_AGENT_ID)

    pw_input_box = page.locator("#mf_txppWframe_input2")
    await pw_input_box.wait_for(state="attached", timeout=3000)
    await pw_input_box.fill(TAX_AGENT_PW)

    login_button = page.locator("#mf_txppWframe_trigger41")
    await login_button.wait_for(state="attached", timeout=3000)
    await login_button.click()
 
    return page
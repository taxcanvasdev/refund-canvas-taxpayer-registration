from playwright.async_api import Page
from schemas import TaxPayer
import asyncio

async def register_taxpayer(page: Page, taxpayer: TaxPayer):
    print("register_taxpayer 실행!!!")

    await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&tmIdx=48&tm2lIdx=4804000000&tm3lIdx=4804050000", wait_until="domcontentloaded")
    
    # 페이지 로딩 대기
    print("페이지 로딩 대기 중...")
    await page.wait_for_load_state("networkidle", timeout=5000)

    client_type = taxpayer.client_type

    # ✅ 사업자 유형 구분 클릭
    if client_type == "individual_business":
        btn1 = page.locator("label[for='mf_txppWframe_taPrxClntClCd_input_0']")
        await btn1.wait_for(state="attached", timeout=3000)
        await btn1.click()
    elif client_type == "corporate_business":
        btn2 = page.locator("label[for='mf_txppWframe_taPrxClntClCd_input_1']")
        await btn2.wait_for(state="attached", timeout=3000)
        await btn2.click()
    else:  # 비사업자
        btn3 = page.locator("label[for='mf_txppWframe_taPrxClntClCd_input_2']")
        await btn3.wait_for(state="attached", timeout=3000)
        await btn3.click()

    # ✅ 사업자등록번호 입력
    if client_type in ("individual_business", "corporate_business"):
        parts = taxpayer.business_registration_number.split("-")

        front3 = page.locator("#mf_txppWframe_bsno1")
        await front3.wait_for(state="attached", timeout=3000)
        await front3.fill(parts[0])

        mid2 = page.locator("#mf_txppWframe_bsno2")
        await mid2.wait_for(state="attached", timeout=3000)
        await mid2.fill(parts[1])

        last5 = page.locator("#mf_txppWframe_bsno3")
        await last5.wait_for(state="attached", timeout=3000)
        await last5.fill(parts[2])
    else:
        name = page.locator("#mf_txppWframe_fnm")
        await name.wait_for(state="attached", timeout=3000)
        await name.fill(taxpayer.name)

    # ✅ 주민등록번호
    resno_input = page.locator("#mf_txppWframe_resno")
    await resno_input.wait_for(state="attached", timeout=3000)
    await resno_input.fill(taxpayer.resident_registration_number)

    # ✅ 전화번호
    parts = taxpayer.phone_number.split("-")
    mp_front = page.locator("#mf_txppWframe_telno1")
    await mp_front.wait_for(state="attached", timeout=3000)
    await mp_front.fill(parts[0])

    mp_mid = page.locator("#mf_txppWframe_telno2")
    await mp_mid.wait_for(state="attached", timeout=3000)
    await mp_mid.fill(parts[1])

    mp_last = page.locator("#mf_txppWframe_telno3")
    await mp_last.wait_for(state="attached", timeout=3000)
    await mp_last.fill(parts[2])

    # ✅ 휴대전화번호
    parts = taxpayer.phone_number.split("-")

    select_box = page.locator("#mf_txppWframe_mp1")
    await select_box.wait_for(state="attached", timeout=3000)
    options = await select_box.locator("option").all_text_contents()

    phone_prefix = parts[0]
    if phone_prefix in options:
        await select_box.select_option(label=phone_prefix)
    else:
        await select_box.select_option("010")

    tel_mid = page.locator("#mf_txppWframe_mp2")
    await tel_mid.wait_for(state="attached", timeout=3000)
    await tel_mid.fill(parts[1])

    tel_last = page.locator("#mf_txppWframe_mp3")
    await tel_last.wait_for(state="attached", timeout=3000)
    await tel_last.fill(parts[2])

    # ✅ 이메일
    parts = taxpayer.email.split("@")
    email_front = page.locator("#mf_txppWframe_eml")
    await email_front.wait_for(state="attached", timeout=3000)
    await email_front.fill(parts[0])

    email_back = page.locator("#mf_txppWframe_dman")
    await email_back.wait_for(state="attached", timeout=3000)
    await email_back.fill(parts[1])

    # ✅ 세목
    select_box = page.locator("#mf_txppWframe_itrfCd")
    await select_box.wait_for(state="attached", timeout=3000)
    options = await select_box.locator("option").all_text_contents()

    tax_type = taxpayer.tax_type
    if tax_type=="gift_tax" :
        await select_box.select_option(label="증여세")
    else :
        await select_box.select_option(label="양도소득세")

    # ✅ 수임 일자
    contract_date_input = page.locator("#mf_txppWframe_afaDt_input")
    await contract_date_input.wait_for(state="attached", timeout=3000)
    await contract_date_input.fill(taxpayer.contract_date)

    # ✅ 해임 일자
    dismissal_date_input = page.locator("#mf_txppWframe_dsmsDt_input")
    await dismissal_date_input.wait_for(state="attached", timeout=3000)
    await dismissal_date_input.fill(taxpayer.dismissal_date)

    # ✅ 등록 버튼 클릭
    register_btn = page.locator("#mf_txppWframe_trigger85")
    await register_btn.wait_for(state="attached", timeout=3000)
    await register_btn.click()

    # 두번 열린 다이얼로그 창 끌때까지 기다려주기
    await page.wait_for_timeout(2000)
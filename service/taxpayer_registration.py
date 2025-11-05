from playwright.async_api import Page
from schemas import TaxPayer

async def register_taxpayer(page : Page, taxpayer: TaxPayer) :
    await page.goto("https://hometax.go.kr/websquare/websquare.html?w2xPath=/ui/pp/index_pp.xml&tmIdx=48&tm2lIdx=4804000000&tm3lIdx=4804010000", wait_until="domcontentloaded")
    
    client_type = taxpayer.client_type

    # 개인사업자
    if client_type=="individual_business" :
        await page.click("#mf_txppWframe_taPrxClntClCd_input_0")
    # 법인사업자
    elif client_type=="corporate_business":
        await page.click("#mf_txppWframe_taPrxClntClCd_input_1")
    # 비사업자
    else:
        await page.click("#mf_txppWframe_taPrxClntClCd_input_2")

    # 개인사업자 또는 법인사업자라면 사업자번호 채우기
    if client_type=='individual_business' or client_type=='corporate_business':
        parts = taxpayer.business_registration_number.split("-")
        
        front3 = page.locator("#mf_txppWframe_bsno1")
        await front3.fill(parts[0])
        mid2 = page.locator("#mf_txppWframe_bsno2")
        await mid2.fill(parts[1])
        last5 = page.locator("#mf_txppWframe_bsno3")
        await last5.fill(parts[2])
    # 비사업자라면 성명만 채우기
    else:
        name = page.locator("#mf_txppWframe_fnm")
        await name.fill(taxpayer.name)

    # 대표자 주민등록번호 채우기
    resno_input = page.locator("#mf_txppWframe_resno")
    await resno_input.fill(taxpayer.resident_registration_number)

    # 전화번호 채우기
    select_box = page.locator("#mf_txppWframe_mp1")
    options = await select_box.locator("option").all_text_contents()

    parts = taxpayer.phone_number.split("-")

    phone_prefix = parts[0]
    if phone_prefix in options:
        await select_box.select_option(phone_prefix)
    else:
        await select_box.select_option('010')

    front3 = page.locator("#mf_txppWframe_telno1")
    await front3.fill(parts[0])
    mid2 = page.locator("#mf_txppWframe_telno2")
    await mid2.fill(parts[1])
    last5 = page.locator("#mf_txppWframe_telno3")
    await last5.fill(parts[2])
    
    # 휴대전화번호 채우기
    parts = taxpayer.mobile_number.split("-")
    front3 = page.locator("#mf_txppWframe_mp1")
    await front3.fill(parts[0])
    mid4 = page.locator("#mf_txppWframe_mp2")
    await mid4.fill(parts[1])
    last4 = page.locator("#mf_txppWframe_mp3")
    await last4.fill(parts[2])
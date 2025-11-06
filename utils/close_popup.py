async def close_popup(page, context, url):
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
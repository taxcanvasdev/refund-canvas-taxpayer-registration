from service.hometax_login import login_hometax_with_certificate
from service.taxpayer_registration import register_taxpayer
from schemas import TaxPayer
import time

async def run_workflow(taxpayer : TaxPayer) :
    p, browser, page = await login_hometax_with_certificate()
    try :
        await register_taxpayer(page, taxpayer)
    finally:
        print("\n브라우저가 열려 있습니다. Ctrl+C를 눌러 종료하세요.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n종료 중...")
            await browser.close()
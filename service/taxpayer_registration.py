from playwright.async_api import Page
from schemas import TaxPayer

async def register_taxpayer(page : Page, taxpayer: TaxPayer) :
    print("register_taxpayer 잘 넘어옴")
    print(f"[{page.title()}]\n")
    print(taxpayer)
    return True
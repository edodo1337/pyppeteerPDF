import asyncio
from pyppeteer import launch
from flask import flash


async def html_to_pdf(path):
    browser = await launch(
    #headless=False,
    handleSIGINT=False,
    handleSIGTERM=False,
    handleSIGHUP=False
    )

    page = await browser.newPage()
    await page.goto(path, waitUntil='networkidle2')

    filename = path[path.find('/') + 2 : path.rfind('.')]+'.pdf'
    print(filename)

    # await page.evaluate("""
    #     () =>{
    #         Object.defineProperties(navigator,{
    #             webdriver:{
    #             get: () => false
    #             }
    #         })
    #     }
    # """)

    await page.emulateMedia("screen")
    await page.reload(option={"waitUntil":"domcontentloaded"})
    print('waiting')
    await page.waitFor(10000)
    await page.pdf({'path': filename}, displayHeaderFooter=True, printBackground=True)
    await page.pdf({'path': filename}, displayHeaderFooter=True, printBackground=True)
    #await page.pdf({'path': filename}, displayHeaderFooter=True, printBackground=True)

    #await page.screenshot({'path': 'example.png'})
    await browser.close()


#asyncio.get_event_loop().run_until_complete(html_to_pdf('https://yandex.ru'))
import sys, asyncio
from playwright.async_api import async_playwright
pages = sys.argv[2:] or ["/"]
width = int(sys.argv[1])
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={"width": width, "height": 900})
        for u in pages:
            await pg.goto("http://localhost:8765" + u, wait_until="networkidle")
            name = (u.strip("/") or "home").replace("/", "_")
            await pg.screenshot(path=f"/tmp/shot_{name}_{width}.png", full_page=True)
            print(name, await pg.evaluate("document.documentElement.scrollWidth"), await pg.evaluate("document.documentElement.scrollHeight"))
        await b.close()
asyncio.run(main())

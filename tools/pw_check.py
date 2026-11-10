import re,glob,os,sys
from playwright.sync_api import sync_playwright
paths=['/']+['/'+os.path.relpath(f,'site').replace('index.html','') for f in sorted(glob.glob('site/*/index.html'))]
bad=[];n=0
with sync_playwright() as p:
    b=p.chromium.launch()
    for w in (320,390,768,1280):
        pg=b.new_page(viewport={'width':w,'height':900})
        fails=[]
        pg.on('response',lambda r: fails.append((r.url,r.status)) if r.status>=400 and 'fonts.g' not in r.url else None)
        for u in paths:
            pg.goto('http://localhost:8765'+u,wait_until='load'); n+=1
            ov=pg.evaluate('document.documentElement.scrollWidth-document.documentElement.clientWidth')
            bi=pg.evaluate('[...document.images].filter(i=>i.complete&&i.naturalWidth==0).map(i=>i.src)')
            if ov>0 or bi: bad.append((w,u,ov,bi))
        if w==1280:
            pg.goto('http://localhost:8765/drain-cleaning/'); y0=pg.evaluate("document.querySelector('.sidecard').getBoundingClientRect().top")
            pg.evaluate('window.scrollTo(0,1400)'); pg.wait_for_timeout(200)
            print('sidecard top after scroll',y0,pg.evaluate("document.querySelector('.sidecard').getBoundingClientRect().top"))
        if w==390:
            pg.goto('http://localhost:8765/'); pg.click('.hamburger'); pg.wait_for_timeout(300)
            print('drawer open:',pg.evaluate("document.documentElement.className+' | '+(document.querySelector('.mob-drawer,.drawer')||{className:'?'}).className"))
            pg.screenshot(path='/tmp/drawer390.png')
        print(w,'responses>=400:',fails[:5])
    b.close()
print('checked',n,'page loads; problems:',bad[:10])

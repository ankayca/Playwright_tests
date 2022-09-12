import re
from tracemalloc import get_object_traceback
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False,slow_mo=1000)
        page = browser.new_page()
        page.goto('https://www.amazon.com.tr/ref=nav_logo')  

        page.locator("[id=\"nav-hamburger-menu\"]").click()
        #page.wait_for_timeout(2000)
        # Click a:has-text("tümünü görüntüle")
        page.locator(".hmenu-compressed-btn").click()

        #page.wait_for_timeout(2000)
        all_categories = page.query_selector_all('.hmenu-arrow-next')
        for t in all_categories:
            #page.wait_for_timeout(2000)
            t.click()
            print("hello pappa")

            # Click h1:has-text("Kadın Sneaker")
            #hmenu-content > ul.hmenu.hmenu-visible.hmenu-translateX > li:nth-child(3) > a
            html = page.inner_html("#hmenu-content > ul.hmenu.hmenu-visible.hmenu-translateX ")
            
            soup = BeautifulSoup(html,'html.parser')
            #print(soup.findAll('a', {"class":"hmenu-item"}))
            for x in soup.findAll('a', {"class":"hmenu-item"}):
                xx = x.get("href") 
                if xx != "/":
                    print(xx)
                    page.goto("https://www.amazon.com.tr"+xx)
                    page.mouse.wheel(0, 15000)
                    #page.wait_for_timeout(2000)
                    #***************************************************************
                    # Tüm sonuçları gör yazısı olmadan açılırsa ne yapacağız ?
                    # Örnek düz ayakkabı linki 
                    #***************************************************************
                    try:
                        page.locator("text=Tüm sonuçları gör").click()
                    except:
                        continue
                    print("hellooo")
                    print("girmedimmm")
                    #page.wait_for_timeout(2000)
                    
                    


            page.locator("[id=\"nav-hamburger-menu\"]").click()
            #page.wait_for_timeout(2000)
            # Click a:has-text("tümünü görüntüle")
            page.locator(".hmenu-compressed-btn").click()

            #page.wait_for_timeout(2000)
                    

            print("maraba------------------------------------------------")
            page.locator("#hmenu-content > ul.hmenu.hmenu-visible.hmenu-translateX > li:nth-child(1)").click()
            #page.wait_for_timeout(2000)
        #page.wait_for_timeout(2000)

        browser.close()
main()
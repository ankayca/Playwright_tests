



from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json
import sqlite3
def main():
    with sync_playwright() as p:
        connection = sqlite3.connect("gfg.db")
 
        # cursor
        crsr = connection.cursor()
        crsr.execute('''
		CREATE TABLE IF NOT EXISTS emp (
			product_title  ,
			product_link ,
			price x
			)
               ''')
        category_tags = ["garden","baby","computers","electronics","home","kitchen","pets","grocery","gift-cards","stripbooks","beauty","fashion","mi","office-products","automotive","toys","videogames","instant-video","hpc","sports","diy"]
        category_list = ["1.Bahçe","2.Bebek","3.Bilgisayarlar","4.Elektronik","5.Ev","6.Ev ve Mutfak","7.Evcil Hayvan Malzemeleri","8.Gıda ve içecek","9.Hediye Kartları","10.Kitaplar","11.Kişisel Bakım ve Kozmetik","12.Moda","13.Müzik aletleri","14.Ofis ürünleri","15.Otomotiv","16.Oyuncaklar ve Oyunlar","17.Pc ve Video Oyunları","18.Prime Video","19.Sağlık ve Bakım","20.Spor","21.Yapı Market"]
        print("Aşağıdaki kategorilerden birinin numarasını tuşlayınız.")
        # for t in category_list:
        #     print(t)
        # tag_number=int(input())
        # keyword = input("Aramak istediğiniz kelimeyi giriniz")
        keyword = "kürek"
        tag_number = 1
        browser = p.firefox.launch(headless=False)
        page = browser.new_page()
        page.set_default_timeout(30000)
         
        page.goto('https://www.amazon.com.tr/ref=nav_logo')
        page.locator("select[name=\"url\"]").select_option("search-alias=" + category_tags[tag_number-1])
        page.locator("[name=\"field-keywords\"]").fill(keyword)
        
        page.locator("id=nav-search-submit-text").click()

        count=0
        counter =0
        page.mouse.wheel(0, 15000)
        page.wait_for_timeout(500)
        total_page = int(page.query_selector(".s-pagination-ellipsis+ .s-pagination-disabled").inner_text())
        with open("sample.json", "w") as outfile:
            for c in range(0,total_page-1):
                page.mouse.wheel(0, 15000)
                #page.wait_for_timeout(2000)
                #page.wait_for_selector("#search > div.s-desktop-width-max.s-desktop-content.s-opposite-dir.sg-row > div.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16 > div > span:nth-child(4) > div.s-main-slot.s-result-list.s-search-results.sg-row > div:nth-child(37) > div > div > span > a.s-pagination-item.s-pagination-next.s-pagination-button.s-pagination-separator")
                #page.locator("class='s-pagination-item s-pagination-next s-pagination-button s-pagination-separator'").click()
                next_page=page.query_selector("""//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[@class="a-section a-spacing-none s-result-item s-flex-full-width s-widget s-widget-spacing-large"]/div/div/span/a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]""")
                if next_page is None:                      # if there are no nex page button
                    page.reload()
                    print("hellooo")
                    count=count +1
                    if count :                              # if same page is reload 
                        url=page.url
                        print(page.url)
                        page_str_cnt = url.find("page")
                        
                        url_int=""
                        while (url[page_str_cnt] != "&" ):
                            
                            url_int +=url[page_str_cnt] 
                            page_str_cnt = page_str_cnt +1
                            print(url[page_str_cnt])
                        url_int=url_int.replace("page=","")
                        page.goto(url.replace(url_int,str(int(url_int)+1)))
                        count = 0

                else:
                    next_page= next_page.get_attribute("href")
                    for t in page.query_selector_all("""//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[@class="sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]/div/div/div/div"""):
                        name = t.query_selector("""//*[@class="a-section a-spacing-none a-spacing-top-small s-title-instructions-style"]/h2/a""").inner_text()
                        link = t.query_selector("""//*[@class="a-section a-spacing-none a-spacing-top-small s-title-instructions-style"]/h2/a""").get_attribute("href")
                        price = t.query_selector("""//*[@class="a-section a-spacing-small puis-padding-left-small puis-padding-right-small"]/div[@class="a-section a-spacing-none a-spacing-top-small s-price-instructions-style"]/div[@class="a-row a-size-base a-color-base"]/a/span[1]/span[2]/span[1]""")
                        if price is None:
                            price= "-"
                        else:
                            price=price.inner_text()
                        json.dump({
                            "name"  : name,
                            "link"  : link,
                            "price" : price
                        }, outfile)
                        crsr.execute("""INSERT INTO emp VALUES (?, ?, ?)""",(name,price,link))
                        counter = counter +1
                        print(counter )
                        #print(name)
                        #print(link)
                        #print(price)
                        #print("hello")
                        # Collect infos and prepare page crawling algorithm
                        ################################################
                        #
                        ################################################
                
                    print(next_page)
                    page.goto("https://www.amazon.com.tr"+next_page)
                    if int(next_page[-1]) % 5 == 0:
                        print("mother fucker this is it")  
            connection.commit()
            
            # close the connection
            connection.close()                          
            #page.wait_for_timeout(2000)
            browser.close()
main()
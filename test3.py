
url = "https://www.amazon.com.tr/s?k=k%C3%BCrek&i=garden&page=12&__mk_tr_TR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1663100800&ref=sr_pg_12"


page_str_cnt = url.find("page")
count =0
url_int=""
while (url[page_str_cnt] != "&" ):
    
    url_int +=url[page_str_cnt] 
    page_str_cnt = page_str_cnt +1
    print(url[page_str_cnt])
url_int=url_int.replace("page=","")
print(url.replace(url_int,str(int(url_int)+1)))
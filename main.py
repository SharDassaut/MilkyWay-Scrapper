import httpx
import time
from selectolax.parser import HTMLParser 


############################################################################################
################################   Obtener html    #########################################
############################################################################################

def getHTML(baseURL):
    headears = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    }   
    try:
        r = httpx.get(baseURL, headers=headears)
        r.raise_for_status()
    except httpx.HTTPError as err:
        print(f"No se pudo pedir {err.request.url!r}")
        return False
    return HTMLParser(r.text)
             
############################################################################################
################################ Obtener novedades #########################################
############################################################################################

def getNewProducts(html):
    return html.css("div.section.section-recent-products div div div.product-card")

def getNewProductsInfo(products):
    for product in products:
        item={
        "titulo":product.css_first("h3").text().strip(),
        "precio":product.css_first(".product-card__price").text().strip(),
        "portada":"https:"+product.css_first("img").attrs['src']
        }
        yield item


def downloadPortada(product):
    with open(product ['titulo'],"wb+") as f:
        with httpx.stream("GET", product['portada']) as r:
            for data in r.iter_bytes():
                f.write(data)


def newProducts():
    html = getHTML('https://www.milkywayediciones.com/')
    products = getNewProducts(html)
    newProductsInfo = getNewProductsInfo(products)
    for product in newProductsInfo:
        downloadPortada(product)

############################################################################################
################################## Datos del catálogo ######################################
############################################################################################

def getProdutcs(html):
    return html.css(".product-card-list .product-card")

def getProductsInfo(products):
    for product in products:
        item={
            "titulo":product.css_first("h3 a").text().strip(),
            "precio":product.css_first(".product-card__price").text().strip(),
            "portada":"https:"+product.css_first("img").attrs['src']
        }
        print(item)


def checkIfEmpty(html):
    return html.css_matches("h2.title.title--primary")

def scrapProducts():
    url = "https://www.milkywayediciones.com/collections/all?page="
    for x in range(1, 100):
        print(x)
        html = getHTML(url+str(x))
        if html is False or checkIfEmpty(html) :
            print(f"No se pudo pedir la página {x}")
            break
        products = getProdutcs(html)
        getProductsInfo(products)
        time.sleep(1)

############################################################################################
########################################## MAIN ###########################################
############################################################################################

def main():
    scrapProducts()
        
    
if __name__ == "__main__":
    main()

import httpx
import time
import random
from product import Product
from selectolax.parser import HTMLParser


######################################################
# Dado un url devuelve un objeto html de selectolax  #
#   sobre el cúal se pueden aplicar los filtrados    #
######################################################

def getHTML(url):
    flag = True
    count =0
    while(flag):
        header={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        }

        try:
            r = httpx.get(url, headers=header)
            r.raise_for_status()
            return HTMLParser(r.text)
        except httpx.HTTPStatusError as err:
            print("Occurio este error al pedir el url ,error: ", r.status_code)
            return -1
        except TimeoutError:
            print("TimeOut error: ",count)
            if(count == 3):
                flag = False
                print("No se pudo conectar al servidor")
                return -2
        except httpx.RequestError as e:
            print(f"Error de conexión: {e}")
            return -3
        except Exception as e:
            print(f"Error inesperado: {e}")
            return -4
        
        time.sleep(random.randint(1,3))

######################################################
############## Utilidades de arreglo #################
######################################################

def urlFixer(url,baseUrl):
    if(url.startswith("://")):
        return "https"+url
    elif(url.startswith("//")):
        return "https:"+url
    elif(url.startswith("/")):
        return baseUrl+url
    else:
        return url

#################################################################
# receives selectolax html of the catalogue page and retreives  #
#              all the products of the object                   #
#################################################################

def getProductsUrlFromCataloguePage(html, baseUrl):
    html = (html.css(".product-card-list .product-card"))
    for node in html:
        yield urlFixer(baseUrl+node.css_first('a').attributes['href'],baseUrl)
        
########################################
# Receives the url of the product
#
########################################

def cssSelector(html, selector):
    try:
        return html.css_first(selector).text().strip()
    except AttributeError as err:
        return "None"


# For all the data that can be scraped keep it 
# I will implement it later

def getProductInfo(j):
    pass

def main():
    
    url = "://www.milkywayediciones.com/collections/all?page="
    html = getHTML(urlFixer(url,"https://www.milkywayediciones.com/collections/all?page="))
    if (not (isinstance(html,int))):
        getProductInfo(getProductsUrlFromCataloguePage(html,"https://www.milkywayediciones.com"))
        
    else:
        if html == -1:
            pass
        elif html == -2:
            pass
        elif html == -3:
            pass
        else:
            pass


if __name__ == "__main__":
    main()
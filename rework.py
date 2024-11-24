import httpx
import time
import random
from product import Product
from urllib.parse import urljoin
from selectolax.parser import HTMLParser

DOMAIN_URL = "https://www.milkywayediciones.com"

#######################################################
# Given an url it returns the selectolax html object #
#######################################################

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
        count += 1
        time.sleep(2**count)

######################################################
#################### Utilities #######################
######################################################

########################################
#       Receives url to fix them       #
########################################

def urlFixer(url):
    return urljoin(DOMAIN_URL,url)

##################################
# Better css selection handeling #
##################################

def cssFirstTextSelector(html, selector):
    try:
        return html.css_first(selector).text().strip()
    except AttributeError as err:
        return "None"
    
def cssTextSelector(html,selector):
    try:
        return html.css(selector)
    except AttributeError as err:
        return "None"
    
def cssFirstAtributeSelector(html, selector,attr):
    try:
        return html.css_first(selector).attributes[attr]
    except AttributeError as err:
        return "None"

# Get the title and volume of the product
# if it is a oneshot volume will be none

def getProductTitleAndVolume(url):
    url = url.split("/")[-1].split("-")
    if url[-2] == "vol":
        return(" ".join(url[:-2]),".".join(url[-2:]))
    else:
        return (" ".join(url),"oneshot")

def getProductAuthors(html):
    strs = cssTextSelector(html,"div.product-main__author a h3")
    authors=[]
    for i in strs:
       authors.append(i.text().lower())
    return authors

def getExtraInfo(html):
    extra_info = cssTextSelector(html,"div.product-main__description p")
    extra_info = extra_info[-1].text(deep=True, separator =":", strip=True)
    extra_info = extra_info.split(":")
    while extra_info.count(""):
        extra_info.remove("")
    def_extra_info = []
    for i in range(1,len(extra_info),2):
        def_extra_info.append(extra_info[i])
    return def_extra_info

def getTags(html):
    tagsNode = cssTextSelector(html,"div.product-main__tags a")
    if not(tagsNode == "None"):
        tags =[]
        for tagNode in tagsNode:
            tags.append(tagNode.text(strip = True)) 
        return tags 
    else:
        return tagsNode


def filterTags(tags, title, author):
    for tag in tags:
        if tag.lower() == title.lower() or tag.lower() in author:
            tags.remove(tag)
    return tags

# For all the data that can be scraped keep it 
# ¿tags?

def getProductInfo(url):
    html = getHTML(url)
    if(not (isinstance(html,int))):
        html = html.css_first("section.section.section-product")

        title,volume = getProductTitleAndVolume(url)
        author = getProductAuthors(html)
        price = cssFirstTextSelector(html,"div.product-main__price")
        coverUrl = urlFixer(cssFirstAtributeSelector(html,"img.product-main--img","src"))
        originalTitle, format, size, pageNumber, color, isbn = getExtraInfo(html)
        tags = filterTags(getTags(html),title,author)


    else:
        print("No se ha podido recoger los datos del url:",url)

#################################################################
# receives selectolax html of the catalogue page and retreives  #
#              all the products of the object                   #
#################################################################

def getProductsUrlFromCataloguePage(html, baseUrl):
    html = (html.css(".product-card-list .product-card"))
    for node in html:
        url= cssFirstAtributeSelector(node, 'a', "href")
        if url != "None":
            yield urlFixer(url)
        else:
            yield url


def test():
    getProductInfo("https://www.milkywayediciones.com/products/tatsuyuki-ooyamato-lider-de-la-cuarta-generacion")

def main():

    url = "https://www.milkywayediciones.com/collections/all?page="
    html = getHTML(url)
    if (not (isinstance(html,int))):
        # implement checking if url in None
        urlGenerator = getProductsUrlFromCataloguePage(html,"https://www.milkywayediciones.com")
        for productUrl in urlGenerator:
          getProductInfo(productUrl)
        
    else:
        print("Programa cerrado")
        exit()
    
    

if __name__ == "__main__":
    #main()
    test()
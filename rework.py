# This file is part of the "MilkyWay Ediciones Scraper" project.

import httpx
import asyncio
import json
from typing import Generator
from product import Product
from urllib.parse import urljoin
from selectolax.parser import HTMLParser,Node
from dataclasses import asdict

DOMAIN_URL = "https://www.milkywayediciones.com"

######################################################
###################### Network #######################
######################################################

#######################################################
# Given an url it returns the selectolax html object #
#######################################################

async def getHTML(url: str, retries=3) -> HTMLParser | None:

    header={'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:132.0) Gecko/20100101 Firefox/132.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            }

    async with httpx.AsyncClient() as client:
        for i in range(1,retries):
            try:
                r = await client.get(url, headers=header, timeout=10.0)
                r.raise_for_status()
                return HTMLParser(r.text) # Return parser HTML
            except httpx.HTTPStatusError as err:
                print("Occurio este error al pedir el url ,error: ", r.status_code)
                if(r.status_code == 404):
                    return False
                return None
            except httpx.TimeoutException:
                print("TimeOut error: ",i)
                if(i == 3):
                    flag = False
                    print("No se pudo conectar al servidor")
                    return None
            except httpx.RequestError as e:
                print(f"Error de conexión: {e}")
                return None
            except Exception as e:
                print(f"Error inesperado: {e}")
                return None
            
            await asyncio.sleep(2**i)
            i +=1

######################################################
#################### Utilities #######################
######################################################

########################################
#       Receives url to fix them       #
########################################

def urlFixer(url: str)-> str:
    return urljoin(DOMAIN_URL,url)

##################################
# Better css selection handeling #
##################################

def cssFirstTextSelector(html: HTMLParser, selector: str)-> str:
    try:
        return html.css_first(selector).text().strip()
    except AttributeError as err:
        return None
    
def cssSelector(html: HTMLParser, selector: str) -> Node | None:
    try:
        return html.css(selector)
    except AttributeError as err:
        return None
    
def cssFirstAtributeSelector(html: HTMLParser, selector: str,attr: str)->str:
    try:
        return html.css_first(selector).attributes[attr]
    except AttributeError as err:
        return None

######################################################
##################### Scraping #######################
######################################################

def getProductTitleAndVolume(url: str) -> tuple:
    url = url.split("/")[-1].split("-")
    if "vol" in url:
        return(" ".join(url[:-2]),".".join(url[-2:]))
    else:
        return (" ".join(url),"oneshot")

def getProductAuthors(html: HTMLParser) -> list:
    strs = cssSelector(html,"div.product-main__author a h3")
    authors=[]
    for i in strs:
       authors.append(i.text().lower())
    return authors

def getExtraInfo(html: HTMLParser) -> dict[str:str]:
    extra_info = cssSelector(html,"div.product-main__description p")
    
    extra_info = (extra_info[-1].text(deep=True, separator =":", strip=True)).split(":")
    
    while extra_info.count(""):
        extra_info.remove("")

    if "Booktrailer" in extra_info:
        i = extra_info.index("Booktrailer")+1
        extra_info[i]= "https:"+extra_info[i+1]
        extra_info.pop(i+1)

    if "/N" in extra_info:
        extra_info[extra_info.index('B')] = "B/N con págs. a color"
        extra_info.remove('/N')
        extra_info.remove('con págs. a color')

    extracted_data = {}
    for i in range(0,len(extra_info),2):
        data = extra_info[i+1].lower()
        key = extra_info[i].lower()
        extracted_data[key] = data

    return extracted_data

def getTags(html: HTMLParser) -> list:
    tags_node = cssSelector(html,"div.product-main__tags a")
    if not(tags_node == None):
        tags =[]
        for tag_node in tags_node:
            tags.append(tag_node.text(strip = True)) 
        return tags 
    else:
        return tags_node


def filterTags(tags: list, title: str, author: str) -> list:
    for tag in tags:
        if tag.lower() == title.lower() or tag.lower() in author:
            tags.remove(tag)
    return tags

##################################
#     Main scraping function     #
##################################

async def getProductInfo(url: str) -> Product | None:
    html = await getHTML(url,3)
    if html != None:
        html = html.css_first("section.section.section-product")

        title,volume = getProductTitleAndVolume(url)
        authors = getProductAuthors(html)
        price = cssFirstTextSelector(html,"div.product-main__price")
        cover_url = urlFixer(cssFirstAtributeSelector(html,"img.product-main--img","src"))
        tags = filterTags(getTags(html),title,authors)

        extra_info = getExtraInfo(html)

        booktrailer = extra_info.get("booktrailer")
        original_title = extra_info.get("título original")
        format = extra_info.get("formato")
        size = extra_info.get("tamaño")
        page_number = extra_info.get("páginas")
        color = extra_info.get("color")
        isbn = extra_info.get("isbn")

        return Product(title=title, volume=volume ,authors=authors, price=price, cover_url=cover_url, tags=tags, booktrailer=booktrailer, original_title=original_title, format=format, size=size, page_number=page_number, color=color, isbn=isbn)
    else:
        print("No se ha podido recoger los datos del url:",url)
        return None

#################################################################
# receives selectolax html of the catalogue page and retreives  #
#              all the products of the object                   #
#################################################################

def getProductsUrlFromCataloguePage(html: HTMLParser) -> Generator:
    html = (html.css(".product-card-list .product-card"))
    for node in html:
        url= cssFirstAtributeSelector(node, 'a', "href")
        if url != None:
            yield urlFixer(url)
        else:
            yield None


######################################################
###################### Saving ########################
######################################################

def export_to_json(products: list[Product], filename: str)-> None:
    with open(filename, mode='w') as file:
        json_data = [product.__dict__ for product in products]  # Convert Product objects to dictionaries
        file.write(json.dumps(json_data, indent=4, ensure_ascii=False))
        print(f"Data saved to {filename}")

######################################################
################### MAIN + DEBUG #####################
######################################################

async def main() -> None:
    product_list = []
    for i in range(1,100):
        url = f"https://www.milkywayediciones.com/collections/all?page={i}"
        html = await getHTML(url,3)
        
        if html != None:
            urlGenerator = getProductsUrlFromCataloguePage(html)
            tasks = [getProductInfo(productUrl) for productUrl in urlGenerator if productUrl is not None]
            
            results = await asyncio.gather(*tasks)
            products_on_page = [product for product in results if isinstance(product, Product)]
            product_list.extend(products_on_page)
            
            if not products_on_page:
                print("No hay más urls en el catalogo")
                break
            
        else:
            print("Programa cerrado")
            exit()

    if product_list:
        export_to_json(product_list,"products.json")
        print("Scarpping acabado")
    else:
        print("0 productos fueron scrapeados")
    
async def test():
    a = await getProductInfo("https://www.milkywayediciones.com/products/de-fran-a-ilutv")
    print(a)
    print("\n\n")
    print(await getProductInfo("https://www.milkywayediciones.com/products/golden-kamuy-vol-31"))
if __name__ == "__main__":
    #asyncio.run(main())
    asyncio.run(test())
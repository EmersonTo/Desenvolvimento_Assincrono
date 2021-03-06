from urllib import response
from bs4 import BeautifulSoup
from requests import get
from time import time
from asyncio import ensure_future, gather, get_event_loop, new_event_loop, set_event_loop
from aiohttp import ClientSession

all_data  = []
master_dict = {}
inicio = time()
resposta = get('https://pt.wikipedia.org/wiki/Sociedade_Esportiva_Palmeiras#Hist%C3%B3rico_Categoria_Master')
tags = BeautifulSoup(resposta.text,'html5lib')
nome_pagina = tags.find("h1",attrs={"class" : "firstHeading mw-first-heading"})
print(f"Página principal: {nome_pagina.text}")
paginas =  tags.find_all("a",href = True)

visitar = []
for pagina in paginas:
    visitar.append(pagina.get('href'))

comeca_com = "/wiki/"
links =list(filter(lambda x: x.startswith(comeca_com), visitar))

print(f"Total de Páginas a Visitar: {len(visitar)}")


async def fetch(session,url):
    async with session.get(url) as resp:
        return await resp.text()

async def run():
    tasks = []
    async with ClientSession() as session:
        for link in links:
            task = ensure_future(
                            fetch(
                                session,
                                f"https://pt.wikipedia.org/{link}"
                            ))                    
            tasks.append(task)
        
        
        responses = await gather(*tasks)
        for resp in responses:
            tags_sec = BeautifulSoup(resp,'html5lib')
            nome_pagina_sec = tags_sec.find("h1",attrs={"class" : "firstHeading mw-first-heading"})
            print(f"Página secundária:  {nome_pagina_sec.text}")

        

loop = get_event_loop()
future = ensure_future(run())
loop.run_until_complete(future)  

termino = time()
print(f"Tempo total da execução:{abs(int(termino - inicio))} segundos")
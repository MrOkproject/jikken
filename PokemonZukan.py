import requests,sys,webbrowser,bs4,os,re

 #Return Poke Name and URL
def Page(Name,Url):
    res_page=requests.get(Url)
    soup_page=bs4.BeautifulSoup(res_page.content,"html.parser")
    table_page = soup_page.select('th[colspan="2"]')
    num_poke=soup_page.select('tr[class="center"] > td')
    if len(num_poke)>0:
        FileName=num_poke[2].text+"-"+num_poke[-1].text

    try:
        if Name !=table_page[0].text:
            if "(" in Name:
                return [table_page[0],FileName]
            return Page(Name,FormChange(Name,Url)) #メガシンカ
        else:
            return [table_page[0],FileName] #tag having Picture URL
    except IndexError:
        return False


def FormChange(Name,Url):
    res_page=requests.get(Url)
    soup_page=bs4.BeautifulSoup(res_page.content,"html.parser")
    for j in soup_page.select("li a"):
        if Name == j.getText("href"):
            res_forme = requests.get(url + str(j.get("href")))
            soup_forme = bs4.BeautifulSoup(res_forme.content, "html.parser")
            table_forme = soup_forme.select('th[colspan="2"]')
            if name_poke == table_forme[0].getText():
                return url+str(j.get("href")) #URLを返す
    return False

print("Searching...")

url="https://yakkun.com"  #BasicURL

os.makedirs("picture",exist_ok=True)

res=requests.get('https://yakkun.com/sm/status_list.htm')
res.raise_for_status()
soup=bs4.BeautifulSoup(res.content,"html.parser")

for i in soup.find_all("a"):
    h=i.get("href")
    name_poke=i.text
    if "zukan" in str(h):
        newUrl=url+"/sm"+str(h[1:])
        pokelink=Page(name_poke,newUrl) #Call function
        if pokelink==False:
            continue
        poke_regex=re.compile(r"url\(.+\)")   #Regular Expression
        poke_search=poke_regex.search(str(pokelink[0]))
        if poke_search !=None:
            target="http:"+str(poke_search.group())[5:-2]
            picture_request=requests.get(target)

            with open("picture/"+pokelink[1]+"-"+target.split("/")[-1],"wb") as f: #saving picture
                f.write(picture_request.content)





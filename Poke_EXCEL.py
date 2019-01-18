import requests,sys,webbrowser,bs4,os,re,openpyxl

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
                return [table_page[0],num_poke[2].text,num_poke[-1].text]
            return Page(Name,FormChange(Name,Url)) #メガシンカ
        else:
            return [table_page[0],num_poke[2].text,num_poke[-1].text] #tag having Picture URL
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

wb=openpyxl.Workbook()
ws=wb.worksheets[0]
ws.cell(row=1, column=1).value="画像"
ws.cell(row=1,column=2).value="No."
ws.cell(row=1,column=3).value="和名"
ws.cell(row=1,column=4).value="name"

url="https://yakkun.com"  #BasicURL

os.makedirs("picture",exist_ok=True)

res=requests.get('https://yakkun.com/sm/status_list.htm')
res.raise_for_status()
soup=bs4.BeautifulSoup(res.content,"html.parser")
rrr=1
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
            rrr+=1
            target="http:"+str(poke_search.group())[5:-2]
            picture_request=requests.get(target)

            img="picture/"+pokelink[1]+"-"+pokelink[2]+"-"+target.split("/")[-1]
            with open(img,"wb") as f: #saving picture
                f.write(picture_request.content)

            xImg=openpyxl.drawing.image.Image(img)

            #xImg.anchor
            ws.add_image(xImg,"A"+str(rrr))
            ws.cell(row=rrr,column=2).value=pokelink[1]
            ws.cell(row=rrr,column=3).value=name_poke
            ws.cell(row=rrr,column=4).value=pokelink[2]
            if rrr==20:
                break

wb.save('out.xlsx')
wb.close()
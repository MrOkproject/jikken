import requests,sys,webbrowser,bs4,os
print("Googling...")

url="https://yakkun.com/sm"

os.makedirs("picture",exist_ok=True)

res=requests.get('https://yakkun.com/sm/zukan/n1')
res.raise_for_status()
soup=bs4.BeautifulSoup(res.content,"html.parser")

link_elems=soup.select('th[colspan="2"]')
print(link_elems[0].getText())

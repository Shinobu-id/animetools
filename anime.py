#module_pdf
import requests, os, sys, time
from bs4 import BeautifulSoup as BS
from PIL import Image
from io import BytesIO
#module_img
import requests,re,time,os,random
from bs4 import BeautifulSoup as bs
save  = []
os.system("clear")
try:
    grey = '\x1b[90m'
    red = '\x1b[91m'
    green = '\x1b[92m'
    yellow = '\x1b[93m'
    blue = '\x1b[94m'
    purple = '\x1b[95m'
    cyan = '\x1b[96m'
    white = '\x1b[37m'
    flag = '\x1b[47;30m'
    off = '\x1b[m'
except:
	pass

def img():
	x = f"""Author : hudaxcode
Tools  : untuk pencinta animehh 
{red}___________           .__          
\__    ___/___   ____ |  |   ______
  |    | /  _ \ /  _ \|  |  /  ___/
  |    |(  <_> |  <_> )  |__\___ \ 
  |____| \____/ \____/|____/____  {off}> version {grey}3.0{red}
                                \/ {off}"""
	print(x)

def menu():
	img()
	print(f" 1. downloads gambar waifumu")
	print(f" 2. downloads manga pdf")
	hx = input("hudaxcode/> ")
	if hx =="1":
		search()
	if hx =="2":
		pdf()
#pdf
MAINDIR="/storage/emulated/0/Download/animetools"
try:
        os.mkdir(MAINDIR)
except: pass
ses=requests.Session()
def download(cap, url, title, num, pdf):
        MAINPATH=f"{MAINDIR}/{title}"
        PATH=f"{MAINPATH}/{cap[num-1]['cap']}"
        try:
                os.mkdir(MAINPATH)
        except: pass

        if pdf == False:
                try:
                        os.mkdir(PATH)
                except: pass

        req=ses.get(url)
        bs=BS(req.text, "html.parser")
        img=bs.find_all("div", {"id": "all"})
        src=img[0].find_all("img")

        n=1
        imgs=[]
        for x in src:
                link=[x["data-src"].replace("//","https://") if x["data-src"][0:2] == "//" else x["data-src"]]
                proges=f"[#] Downloading \"{PATH.split('/')[-1]}/"+"{:02}.jpg\"".format(n)
                print(f"\r{proges}",end="",flush=True)
                if pdf == False:
                        with open(f"{PATH}/"+"{:02}.jpg".format(n), "wb") as img:
                                req=ses.get(link[0])
                                img.write(req.content)
                        n+=1
                        if n > len(src):
                                print(f"\r{' '*len(proges)}", end="", flush=True)
                                print(f"\r[✓] Done {PATH.split('/')[-1]}", end="", flush=True)
                                path = f"{PATH}"
                                print(f"\n[!] Saved to {path}")
                else:
                        imgs.append(ses.get(link[0]).content)
                        n+=1
        if pdf == True:
                print(f"\r{' '*len(proges)}",end="", flush=True)
                print("\r[*] Converting to pdf",end="",flush=True)
                cpdf=[]
                for i in imgs:
                        cpdf.append(Image.open(BytesIO(i)).convert('RGB'))
                cpdf[0].save(f"{PATH}.pdf", save_all=True, append_images=cpdf[1:])
                print(f"\r[✓] Done {PATH.split('/')[-1]}   ",end="",flush=True)
                path = f"{PATH}"
                print(f"\n[!] Saved to {path}")
        print()

def chap_dl(cap, pilih, title):
        tny=input("[?] Apakah anda ingin menconvert hasil download ke pdf (Y/T) ")
        if tny.lower() == "y":
                pdf=True
        else:
                pdf=False

        if "-" in pilih:
                pilih=pilih.split("-")
                if len(pilih) == 2 and pilih[1] != "":
                        ran=range(int(pilih[0]), int(pilih[1])+1)
                else:
                        ran=range(int(pilih[0]), len(cap)+1)
                for x in ran:
                        download(cap, cap[x-1]["url"], title, x, pdf)
        else: 
        	download(cap, cap[int(pilih)-1]["url"], title, int(pilih), pdf)

def get_chap(manga):
        _cap=[]
        req=ses.get("https://mangaid.click/manga/"+manga)
        bs=BS(req.text, "html.parser")
        data=bs.find_all("h5", {"class":"chapter-title-rtl"})

        info=bs.find("dl", {"class":"dl-horizontal"})
        rate=info.find("div",{"class":"rating clearfix"})
        genre=", ".join([i.text for i in info.find_all("a")])
        print(f"- Genre : {green}{genre}{off}\n- Rating: {green}{rate.text.strip()[:-1]}{off}")
        time.sleep(2)

        n=0
        for x in data:
                nc=x.text.strip()
                _cap.append([n, nc, x.find("a")["href"]])
                n-=1
        _cap.sort()
        hasil=[{"cap":y[1], "url":y[2]} for y in _cap]
        return hasil

def cari(q):
        req=ses.get("https://mangaid.click/search?query="+q)
        return req.json()

def pdf():
	query=input(f"query({green}korohi ai{off}): ")
	hasil=cari(query)["suggestions"]
	if len(hasil) > 1:
		n=1
		for x in hasil:
		    print(f'{n}. {x["value"]}')
		    n+=1
		pil=int(input("Pilih: "))
		lih=hasil[pil-1]["data"]
		title=hasil[pil-1]["value"]
	elif len(hasil) == 1:
	    lih=hasil[0]["data"]
	    title=hasil[0]["value"]
	else:
	    print("! manga tidak di temukan atau gunakan query lain")
	    input("[ Enter ]")
	    pdf()

	print(f"- Title :{green} {title} {off}")
	cap=get_chap(lih)
	for y in range(len(cap)):
	    print(f"{y+1}. {green}{cap[y]['cap']}{off}")
	print(f"[ {len(cap)} (Total) Chapter ditemukan ]\n# ketik (misalnya: 10-) untuk mendownload dari nomor 10 sampai akhir\n# ketik (misalnya: 10-20) untuk mendownload dari nomor 10 sampai 20\n# ketik angka saja tanpa garis untuk mendownload salah satu")
	pilih=input("hudaxcode/> ")
	chap_dl(cap, pilih, lih)




#img
def search():
	global search
	num = 1
	search = input(f"query wifumu({green}kurumi{off}): ")
	s      = search.replace(" ","+")
	url    = f"https://wallpapercave.com/search?q={s}"
	get    = requests.get(url).text
	hxc    = bs(get,'html.parser')
	zt     = hxc.findAll("a")
	ztt    = re.findall('<div class="albumphoto" href="(.*?)"',str(zt))
	zttt   ="".join(ztt)
	with open("hudaxcode","a") as hxc:
		hxc.write(zttt.replace("/","\n"))
	z      = re.findall('p class="number">(.*?)</p>',str(zt))
	print(f"results for query {green}{search}{off}....")
	for a in z:
		print(f"[{num}]. {yellow}{a}{off}")
		num +=1
	op  = open("hudaxcode").readlines()
#	print(f"\ntype '{green}all{off}' untuk mendownloads semua image")
#	print(f"type '{green}1,2{off}' untuk mengabungkan mendownloads  image")
	x   = input("hudaxcode: ")
	url = op[int(x)]
	get_url(url.replace("\n",""))

def get_url(url):
	print("please wait, Getting data..")
	urlku = f"https://wallpapercave.com/mwp/"
	urlme = f"https://wallpapercave.com/{url}"
	hxc   = requests.get(urlme).text
	if not 'source media' in hxc:
		hxc1  = bs(hxc,'html.parser')
		for index in re.findall('<a class="download" href="(.*?)"',str(hxc1)):
			save.append(index)
		downloads()
	elif 'source media' in hxc:
		hxc1  = bs(hxc,'html.parser')
		hxc2  = hxc1.findAll("source")
		for index in re.findall('srcset="/mwp/(.*?)"',str(hxc2)):
			save.append(index)
		downloads1()
def downloads1():
	global search
	urlku = "https://wallpapercave.com/mwp/"
#	urlku = "https://wallpapercave.com"
	loads = 1
	print(f"Total data foto di dapatkan {red}{len(save)}{off}")
	folder = input(f"Masukan folder save downloads( {green}/sdcard/Download/{search}{off} )\nhudaxcode: ")
	try:os.system(f"mkdir {folder}")
	except:pass
	print(f"{cyan}Starting downloads...{off}")
	if not "download" in save:
		for hxc in save:
			print(f"{loads}. {green}{urlku}{hxc} downloads √{off} ")
			urlme = f"{urlku}{hxc}"
			response = requests.get(urlme)
			if response.status_code == 200:
				with open(f"{folder}/{loads}.png", 'wb') as f:
					f.write(response.content)
			loads += 1

def downloads():
	global search
#	urlku = "https://wallpapercave.com/mwp/"
	urlku = "https://wallpapercave.com"
	loads = 1
	print(f"Total data foto di dapatkan {red}{len(save)}{off}")
	folder = input(f"Masukan folder save downloads( {green}/sdcard/Download/{search}{off} )\nhudaxcode: ")
	try:os.system(f"mkdir {folder}")
	except:pass
	print(f"{cyan}Starting downloads...{off}")
	if not "download" in save:
		for hxc in save:
			print(f"{loads}. {green}{urlku}{hxc} downloads √{off} ")
			urlme = f"{urlku}{hxc}"
			response = requests.get(urlme)
			if response.status_code == 200:
				with open(f"{folder}/{loads}.png", 'wb') as f:
					f.write(response.content)
			loads += 1

	elif "download" in save:
		tok = "https://wallpapercave.com/"
		tok1 = "https://wallpapercave.com/wp/"
		for hxc in save:
			print(f"{loads}. {green}{tok}{hxc} downloads √ {off}")
			urlme = f"{tok1}{hxc}"
			response = requests.get(urlme)
			if response.status_code == 200:
				with open(f"{folder}/{loads}.png", 'wb') as f:
					f.write(response.content)
			loads += 1



if __name__=="__main__":
	try:os.system("rm -rf hudaxcode")
	except:pass
	menu()

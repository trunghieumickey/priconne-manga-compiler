import requests,os,re
from PIL import Image

lost = 0
image = []

while True: 

    if lost > 9: #the server skip page index sometime, stop if 9 page index is missing in total
        break

    response = requests.get("https://web.priconne-redive.us/cartoon/detail/"+str(len(image)+lost+1))
    if ("lost" in response.text):
        lost+=1

    response = re.search("https://assets-priconne-redive-us.akamaized.net/media/cartoon/image/.*png|$", response.text)[0]
    if (response != ""):
        image.append(response) 

    print("\rFound",len(image),"Pages",end="")
print()

with open("URI-LIST.txt","w") as img:
    print(*image,file=img,sep="\n")

os.system("aria2c -i URI-LIST.txt -d image")

image = [Image.open("image/" + x.split('/')[-1]).convert("RGB") for x in image] 
image[0].save("priconne.pdf", save_all=True, append_images=image[1:])

import requests,os,re
from PIL import Image

# disable this if you want to start from the beginning
enable_recorver = True 

try: 
    # recorver page index to reduce hit to the server
    # download page from akaamized is fine as cdn can handle it
    if not enable_recorver:
        raise Exception("Recover is disabled")

    with open("LOST-PAGE.txt","r") as img:
        lost = int(img.read())
    
    with open("URI-LIST.txt","r") as img:
        image = img.read().split("\n")

except:
    lost = 0
    image = []

lostpoint = lost

while True: 

    # the server skip page index sometime, stop if 9 page index is missing in total
    if lost > 9: 
        break

    response = requests.get("https://web.priconne-redive.us/cartoon/detail/"+str(len(image)+lost+1))
    if ("lost" in response.text):
        lost+=1

    response = re.search("https://assets-priconne-redive-us.akamaized.net/media/cartoon/image/.*png|$", response.text)[0]
    if (response != ""):
        image.append(response)
        lostpoint = lost

    print("\rFound",len(image),"Pages",end="")

print()

with open("URI-LIST.txt","w") as img:
    print(*image,file=img,sep="\n")

with open("LOST-PAGE.txt","w") as img:
    print(lostpoint,file=img)

os.system("aria2c -i URI-LIST.txt -d image")

#check if the image is downloaded, if not remove the link from the list
for i in range(len(image)):
    if not os.path.isfile("image/"+image[i].split('/')[-1]):
        image = image[:i]
        break

image = [Image.open("image/" + x.split('/')[-1]).convert("RGB") for x in image] 
image[0].save("priconne.pdf", save_all=True, append_images=image[1:])

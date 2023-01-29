import os

with open("URI-LIST.txt","r") as img:
        image = img.read().split("\n")
        image = image[:-1]

os.mkdir("priconne")
os.system("cwebp cover.jpg -o priconne/cover.webp")
os.system("cp details.json priconne/details.json")

for i in range(len(image)):
    os.mkdir(f'priconne/ch{i+1:03}')
    os.system("cwebp image/"+image[i].split('/')[-1]+f" -o priconne/ch{i+1:03}/image.webp")

os.system("zip -9 -r priconne.zip priconne")
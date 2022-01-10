from PIL import Image 

def change_pix(url):
    img = Image.open(url)
    new_img = img.resize((256,256))
    new_img.save('../caras/face.png','png')


def create_meme(url):
    change_pix(url)

    img1 = Image.open(r"../meme/meme.jpeg") 
    img2 = Image.open(r"../caras/face.png") 
  
    img1.paste(img2,(34,45)) 
    img1.paste(img2,(230,480)) 
  
    img1.show()
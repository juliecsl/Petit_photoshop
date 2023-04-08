# ###########################
# Import

import tkinter as tk
import PIL as pil
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
from tkinter import simpledialog

# ###########################
# Fonctions

def nbrCol(matrice):
    return(len(matrice[0]))


def nbrLig(matrice):
    return len(matrice)


def saving(matPix, filename):
    toSave = pil.Image.new("RGBA", (nbrCol(matPix), nbrLig(matPix)))
    for i in range(nbrCol(matPix)):
        for j in range(nbrLig(matPix)):
            toSave.putpixel((i, j), matPix[j][i])
    toSave.save(filename)


def loading(filename):
    toLoad = pil.Image.open(filename)
    mat = [[(255, 255, 255, 255)]*toLoad.size[0] for k in range(toLoad.size[1])]
    for i in range(toLoad.size[1]):
        for j in range(toLoad.size[0]):
            mat[i][j] = toLoad.getpixel((j, i))
    return mat


create = True
nomImgCourante = ""


def charger(widg):
    global create
    global photo
    global img
    global canvas
    global dessin
    global nomImgCourante
    filename = filedialog.askopenfile(mode='rb', title='Choose a file')
    img = pil.Image.open(filename)
    nomImgCourante = filename.name
    photo = ImageTk.PhotoImage(img)
    if create:
        canvas = tk.Canvas(widg, width=img.size[0], height=img.size[1])
        dessin = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=1, rowspan=4, columnspan=2)
        create = False

    else:
        canvas.grid_forget()
        canvas = tk.Canvas(widg, width=img.size[0], height=img.size[1])
        dessin = canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        canvas.grid(row=0, column=1, rowspan=4, columnspan=2)


def modify(matrice):
    global imgModif
    global nomImgCourante

    saving(matrice, "modif.png")
    imgModif = ImageTk.PhotoImage(file="modif.png")
    canvas.itemconfigure(dessin, image=imgModif)
    nomImgCourante = "modif.png"


def filtre_vert():
    mat = loading(nomImgCourante)
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=(0,mat[i][j][1],0,255)
    modify(mat)


def negatif():
    mat = loading(nomImgCourante)   
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=(255-mat[i][j][0],255-mat[i][j][1],255-mat[i][j][2],255)
    modify(mat)


def symetrique(): 
    mat = loading(nomImgCourante)
    matSym=[[(0,0,0,0)]*nbrCol(mat) for k in range(nbrLig(mat))]
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            matSym[i][nbrCol(mat)-1-j]=mat[i][j]
    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            mat[i][j]=matSym[i][j]
    
    modify(mat)


def gris():
    mat = loading(nomImgCourante)
    #On utilisera la conversion CIE709 qui permet de calculer la teinte de gris qui va être affichée dans le pixel
    #La teinte affichée est : gris=0,2125*rouge + 0,0721*bleu + 0,7154*vert

    for i in range(nbrLig(mat)):
        for j in range(nbrCol(mat)):
            gris = int(0.2125*mat[i][j][0] + 0.7154*mat[i][j][1]+0.0721*mat[i][j][2])
            mat[i][j]=(gris, gris, gris, 255)

    modify(mat)


def close():
    racine.destroy()


# #######################
# Interface graphique

racine = tk.Tk()
racine.title("Mon Petit PhotoShop")

bouton_vert = tk.Button(racine, text="Filtre Vert", command=filtre_vert, bg="green yellow", relief="groove")
bouton_vert.grid(column=0, row=0)

bouton_gris = tk.Button(racine, text="Filtre Noir & Blanc", command=gris, bg="grey", fg="white", relief="groove")
bouton_gris.grid(column=0, row=1)

bouton_sym = tk.Button(racine, text="Symétrie", command=symetrique, bg="pale violet red", relief="groove")
bouton_sym.grid(column=0, row=2)

bouton_negatif = tk.Button(racine, text="Négatif", command=negatif, bg="cyan", relief="groove")
bouton_negatif.grid(column=0, row=3)

bouton_charger = tk.Button(racine, text="Charger l'image", fg="red", command=lambda :charger(racine), relief="groove")
bouton_charger.grid(column=0, row=4)

fermer = tk.Button(racine, text="Fermer", command=close, relief="groove", bg="red")
fermer.grid(column=3, row=4)

label = tk.Label(racine, text ="CIESLA Julie", font=('Times', '12', 'bold italic'))
label.grid(column=1, columnspan=2, row=4)

racine.mainloop()
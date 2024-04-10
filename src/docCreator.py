from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import referencesAndData as rad

import os
import requests

# __  __  ____  ___   ___ 
#(  \/  )(_  _)/ __) / __)
# )    (  _)(_ \__ \( (__ 
#(_/\/\_)(____)(___/ \___)

def y(coordy): #coordenadas y de arriba a abajo
    return A4[1] - coordy
def printTextInLines(coordx, text, maxWidth, font, fontSize): #Salto de línea automático
    global yActualLevel
    words = text.split()
    lines = []
    actualLine = ''    
    for word in words:
        trialText = actualLine + ' ' + word if actualLine else word
        trialWidth = c.stringWidth(trialText, font, fontSize)
        if trialWidth <= maxWidth:
            actualLine = trialText
        else:
            lines.append(actualLine)
            actualLine = word
    if actualLine:
        lines.append(actualLine)
    for line in lines:
        textWidth = c.stringWidth(line, font, fontSize)
        c.drawString(coordx + (rad.imageSize/2) - (textWidth/2), y(yActualLevel), line)
        yActualLevel += fontSize

#   ___  ____  ____    __    ____  ____    ____  ____   ____ 
#  / __)(  _ \( ___)  /__\  (_  _)( ___)  (  _ \(  _ \ ( ___)
# ( (__  )   / )__)  /(__)\   )(   )__)    )___/ )(_) ) )__) 
#  \___)(_)\_)(____)(__)(__) (__) (____)  (__)  (____/ (__) 
def createPDF(name):
    global c
    c = canvas.Canvas(name, pagesize=A4)
page = 1
global yLevel

#  ___  _____  _  _  ____  ____ 
# / __)(  _  )( \/ )( ___)(  _ \
#( (__  )(_)(  \  /  )__)  )   /
# \___)(_____)  \/  (____)(_)\_)
def coverImage(image):
    # Obtener dimensiones de la imagen original
    originalWidth, originalHeight = ImageReader(image).getSize()
    
    # Calcular el factor de escala necesario para ajustar la imagen al tamaño de la página
    scale_factor_width = A4[0] / originalWidth
    scale_factor_height = A4[1] / originalHeight
    scale_factor = max(scale_factor_width, scale_factor_height)
    
    # Calcular las nuevas dimensiones de la imagen
    new_width = originalWidth * scale_factor
    new_height = originalHeight * scale_factor
    
    # Calcular la posición para centrar la imagen en la página
    posX = (A4[0] - new_width) / 2
    posY = (A4[1] - new_height) / 2
    
    # Dibujar la imagen ajustada en el lienzo
    c.drawImage(image, posX, posY, width=new_width, height=new_height)

def coverCompany():
    c.setFont(rad.mainLightFont, rad.companySize)
    c.setFillColor(colors.black)
    textWidth = c.stringWidth(rad.company, rad.mainLightFont, rad.companySize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.companyY), rad.company)

def coverTitle():
    global yLevel
    yLevel = rad.coverTitleY
    c.setFont(rad.mainLightFont, rad.coverTitleSize)
    c.setFillColor(colors.black)
    for line in rad.coverTitleText:
        yLevel += rad.coverTitleSize
        textWidth = c.stringWidth(line, rad.mainLightFont, rad.coverTitleSize)
        c.drawString((A4[0]/2) - (textWidth/2), y(yLevel), line)

def coverPhrase():
    c.setFont(rad.mainLightFont, rad.coverPhraseSize)
    c.setFillColor(colors.black)
    textWidth = c.stringWidth(" ".join(rad.coverPhraseText), rad.mainLightFont, rad.coverPhraseSize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.coverPhrasePaddingFromTitle + yLevel), " ".join(rad.coverPhraseText))

def coverFooter():
    c.setFillColorRGB(11/255,11/255,69/255)
    c.rect(0, 0, A4[0]+1, rad.coverFooterSize, stroke=0, fill=1)
    c.setFont(rad.mainFont, rad.coverFooterFontSize)
    c.setFillColor(colors.white)
    phoneWidth = c.stringWidth(rad.coverFooterPhone, rad.mainFont, rad.coverFooterFontSize)
    webPageWidth = c.stringWidth(rad.coverFooterWebPage, rad.mainFont, rad.coverFooterFontSize)
    emailWidth = c.stringWidth(rad.coverFooterEmail, rad.mainFont, rad.coverFooterFontSize)
    coverFooterPadding = (A4[0] - 2 * rad.marginLeft - phoneWidth - webPageWidth - emailWidth) / 2
    c.drawString(rad.marginLeft, rad.coverPadding, rad.coverFooterPhone)
    c.drawString(rad.marginLeft + phoneWidth + coverFooterPadding, rad.coverPadding, rad.coverFooterWebPage)
    c.drawString(rad.marginRight - emailWidth, rad.coverPadding, rad.coverFooterEmail)

# Recopilación
def coverPage(image):
    coverImage(image)
    coverCompany()
    coverTitle()
    coverPhrase()
    coverFooter()

#  ____  _  _  ____   ____  _  _ 
# (_  _)( \( )(  _ \ ( ___)( \/ )
#  _)(_  )  (  )(_) ) )__)  )  ( 
# (____)(_)\_)(____/ (____)(_/\_)
def index(products):
    category_counts = {}

    for product in products:
        category = product['Category']
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    newPage("Index")
    current_page = 3
    xIndex = rad.marginLeft
    yIndex = rad.marginTop + 30
    c.setFont(rad.mainFont, rad.indexSize)
    c.setFillColor(colors.black)
    for category, count in category_counts.items():
        categoryWidth = c.stringWidth(category.lower().capitalize(), rad.mainFont, rad.indexSize)
        pageWidth = c.stringWidth(str(current_page), rad.mainFont, rad.indexSize)
        lines = (rad.marginRight - rad.marginLeft - categoryWidth - pageWidth)/c.stringWidth(".", rad.mainFont, rad.indexSize)
        c.drawString(xIndex, y(yIndex), category.lower().capitalize())
        c.setFillColor(colors.lightgrey)
        c.drawString(xIndex + categoryWidth, y(yIndex),"."*(int(lines)))
        c.setFillColor(colors.black)
        c.drawString((rad.marginRight - pageWidth), y(yIndex), str(current_page))
        yIndex += rad.indexSize * 3
        print(f"Category: {category} - Page: {current_page}")
        current_page += (count //16) + (1 if count % 16 > 0 else 0)


# ____  _____  ____  __  __    __    ____ 
#( ___)(  _  )(  _ \(  \/  )  /__\  (_  _)
# )__)  )(_)(  )   / )    (  /(__)\   )(  
#(__)  (_____)(_)\_)(_/\/\_)(__)(__) (__)
def header(): #rectángulo gris
    c.setFillColorRGB(11/255,11/255,69/255)
    c.rect(0, y(0) - rad.headerSize, A4[0]+1, rad.headerSize, stroke=0, fill=1)
def title(text): #título en el header
    c.setFont(rad.mainBoldFont, 30)
    c.setFillColor(colors.white)
    c.drawString(rad.xTitle, y(rad.yTitle), text.lower().capitalize())
def footer(text): #Zienen
    c.setFont(rad.mainLightFont, rad.footerSize)
    c.setFillColor(colors.lightgrey)
    textWidth = c.stringWidth(text, rad.mainLightFont, rad.footerSize)
    c.drawString((A4[0]/2) - (textWidth/2), rad.footerBottomPadding, text)
def pageNumber(number): #Número de página
    c.setFont(rad.mainLightFont, rad.pageNumberSize)
    c.setFillColor(colors.black)
    textWidth = c.stringWidth(str(number), rad.mainLightFont, rad.pageNumberSize)
    c.drawString((A4[0] - rad.pageNumberPadding - textWidth), rad.pageNumberPadding, str(number))

# Crear nueva página con formato
def newPage(newTitle):
    global page, yLevel
    page += 1
    yLevel = rad.marginTop
    c.showPage()
    header()
    if newTitle != "":
        title(newTitle)
    footer(" ".join(rad.company))
    pageNumber(page)


#  ____  __  __    __     ___  ____    ___    __    _  _  ____  ____ 
# (_  _)(  \/  )  /__\   / __)( ___)  / __)  /__\  ( \/ )( ___)(  _ \
#  _)(_  )    (  /(__)\ ( (_-. )__)   \__ \ /(__)\  \  /  )__)  )   /
# (____)(_/\/\_)(__)(__) \___/(____)  (___/(__)(__)  \/  (____)(_)\_)
def printImage(url, directory):
    archName = url.split('/')[-1]  # Obtener el nombre del archivo de la URL
    archRoute = os.path.join(directory, archName)
    # Verificar si el archivo ya está descargado
    if not os.path.exists(archRoute):
        # Descargar la imagen si no está presente
        response = requests.get(url)
        if response.status_code == 200:
            with open(archRoute, 'wb') as archive:
                archive.write(response.content)
        else:
            print(f"No se pudo descargar la imagen desde {url}")
            return None

    return archRoute

# ____  ____  _____  ____   __  __   ___  ____  ___ 
#(  _ \(  _ \(  _  )(  _ \ (  )(  ) / __)(_  _)/ __)
# )___/ )   / )(_)(  )(_) ) )(__)( ( (__   )(  \__ \
#(__)  (_)\_)(_____)(____/ (______) \___) (__) (___/
def image(link): #imagen
    global yActualLevel
    yActualLevel += rad.imageSize
    if link != '':
        c.drawImage(printImage(link, rad.imageDirectory), xLevel, y(yActualLevel), width=rad.imageSize, height=rad.imageSize)
def imageId(idProduct): #ID producto
    c.setFillGray(0.4)
    global yActualLevel
    yActualLevel += rad.idSize
    c.rect(xLevel, y(yActualLevel), rad.imageSize, rad.idSize, stroke=0, fill=1)
    c.setFont(rad.mainLightFont, rad.idSize)
    c.setFillColor(colors.white)
    textWidth = c.stringWidth(idProduct, rad.mainLightFont, rad.idSize)
    c.drawString(xLevel + (rad.imageSize/2) - (textWidth/2), y(yActualLevel) + 2, idProduct)
def brand(brandName): #Logo de la marca
    for elemento in rad.brands:
        if brandName == elemento[0]:
            icon = elemento[1]
            global yActualLevel
            yActualLevel += rad.brandHeight
            if icon != "":
                #obtener ancho final de la imagen
                originalWidth, originalHeight = ImageReader(icon).getSize()
                brandWidth = (originalWidth / originalHeight) * rad.brandHeight 
                c.drawImage(icon, xLevel - (brandWidth/2)+(rad.imageSize/2), y(yActualLevel), width = brandWidth, height=  rad.brandHeight)
            break   
def name(name): #Nombre del artículo
    global yActualLevel
    yActualLevel += rad.nameSize
    c.setFont(rad.mainLightFont, rad.nameSize)
    c.setFillColor(colors.Color(0.2, 0.2, 0.2))
    printTextInLines(xLevel, name.lower().capitalize(), rad.imageSize, rad.mainLightFont, rad.nameSize)

# Añadir un artículo
def addProduct(item):
    image(item['Image url'])
    imageId(item['Model'])
    brand(item['Brand'])
    name(item['Title'])


#   ___  _____  _  _  ____  ____  _  _  ____ 
#  / __)(  _  )( \( )(_  _)( ___)( \( )(_  _)
# ( (__  )(_)(  )  (   )(   )__)  )  (   )(  
#  \___)(_____)(_)\_) (__) (____)(_)\_) (__)
def addProductsToPDF(products):
    element = 0
    product = products[element]
    current_category = product['Category']
    newPage(current_category)
    i = 0
    j = 0
    global yActualLevel, yLevel
    maxYItem = 0
    yActualLevel = yLevel
    global xLevel
    xLevel = rad.marginLeft
    while element < len(products):
        yActualLevel = yLevel
        product = products[element]
        if product['Category'] != current_category:
            current_category = product['Category']
            newPage(current_category)
            i=0
            j=0
            maxYItem = 0
            yActualLevel = yLevel
            xLevel = rad.marginLeft
        addProduct(product)
        print(element+1 , " / " , len(products)) #Ver progreso en consola
        xLevel += rad.nextXImages 
        if yActualLevel - yLevel > maxYItem:
                maxYItem = yActualLevel - yLevel 
        i += 1 
        if i == 4:
            i = 0
            j += 1 
            yLevel += maxYItem 
            maxYItem = 0 
            xLevel = rad.marginLeft 
        if element + 1 < len(products):
            product = products[element+1]
        if (j == 4) and (element + 1 < len(products) and product['Category'] == current_category):
            j = 0 
            newPage("") 
            yLevel = rad.marginTop 
        element += 1 

#  ____  _  _  ____     ____    __     ___  ____ 
# ( ___)( \( )(  _ \   (  _ \  /__\   / __)( ___)
#  )__)  )  (  )(_) )   )___/ /(__)\ ( (_-. )__) 
# (____)(_)\_)(____/   (__)  (__)(__) \___/(____)
def endPage():
    c.showPage()
    c.setFont(rad.mainLightFont, rad.coverTitleSize)
    c.setFillColor(colors.black)
    textWidth = c.stringWidth(rad.company, rad.mainLightFont, rad.coverTitleSize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.coverTitleY), rad.company)
    c.setFont(rad.mainFont, rad.coverPhraseSize)
    textWidth = c.stringWidth(rad.coverFooterPhone, rad.mainFont, rad.coverPhraseSize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.coverTitleY+2*rad.coverTitleSize), rad.coverFooterPhone)
    textWidth = c.stringWidth(rad.coverFooterEmail, rad.mainFont, rad.coverPhraseSize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.coverTitleY+3*rad.coverTitleSize), rad.coverFooterEmail)
    textWidth = c.stringWidth(rad.coverFooterWebPage, rad.mainFont, rad.coverPhraseSize)
    c.drawString((A4[0]/2) - (textWidth/2), y(rad.coverTitleY+4*rad.coverTitleSize), rad.coverFooterWebPage)
    c.setFillColorRGB(11/255,11/255,69/255)
    c.rect(0, 0, A4[0]+1, 100, stroke=0, fill=1)
    
#  ___    __    _  _  ____    ____  ____   ____ 
# / __)  /__\  ( \/ )( ___)  (  _ \(  _ \ ( ___)
# \__ \ /(__)\  \  /  )__)    )___/ )(_) ) )__) 
# (___/(__)(__)  \/  (____)  (__)  (____/ (__) 
def savePDF():
    c.save()
    print("~~~Archivo listo~~~")


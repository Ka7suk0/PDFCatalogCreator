from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
# ____  ____  ____  ____  ____  ____  _  _   ___  ____  ___ 
#(  _ \( ___)( ___)( ___)(  _ \( ___)( \( ) / __)( ___)/ __)
# )   / )__)  )__)  )__)  )   / )__)  )  ( ( (__  )__) \__ \
#(_)\_)(____)(__)  (____)(_)\_)(____)(_)\_) \___)(____)(___/

#  _  _    __    __  __  ____ 
# ( \( )  /__\  (  \/  )( ___)
#  )  (  /(__)\  )    (  )__) 
# (_)\_)(__)(__)(_/\/\_)(____)
archiveName = "Catalog.pdf"

#  ____     __    ____    __   
# (  _ \   /__\  (_  _)  /__\  
#  )(_) ) /(__)\   )(   /(__)\ 
# (____/ (__)(__) (__) (__)(__)
company = "COMPANY"
coverTitleText = ["CATALOG","2024"] # separate by lines
coverPhraseText = "QUALITY PRODUCTS"
coverFooterPhone = "✆ +XX (XXX) XXX XXXX"
coverFooterWebPage = "www.xxxxxx.com"
coverFooterEmail = "✉ sales@xxxxxx.com"

#    __    ____   ___  _   _  ____  _  _  ____  ___ 
#   /__\  (  _ \ / __)( )_( )(_  _)( \/ )( ___)/ __)
#  /(__)\  )   /( (__  ) _ (  _)(_  \  /  )__) \__ \
# (__)(__)(_)\_) \___)(_) (_)(____)  \/  (____)(___/
coverWallpaper = "resources/images/coverpage/Cover.png"
archiveCSV = 'data/Lista.csv'
imageDirectory = "resources\\images\\products\\"
brands = [["brand1","resources\\images\\brands\\brand1.jpg"],
        ["brand2","resources\\images\\brands\\brand2.jpg"],
        ["brand3","resources\\images\\brands\\brand3.jpg"],
        ["brand4","resources\\images\\brands\\brand4.jpg"],
        ["no brand",""],
        ["",""]]


#  ____  _____  _  _  ____  ___ 
# ( ___)(  _  )( \( )(_  _)/ __)
#  )__)  )(_)(  )  (   )(  \__ \
# (__)  (_____)(_)\_) (__) (___/
pdfmetrics.registerFont(TTFont('Helvetica-Light', "resources/fonts/helvetica_light.ttf"))
mainFont = "Helvetica"
mainLightFont = "Helvetica-Light"
mainBoldFont = "Helvetica-Bold"

#  ____   ____  __  __  ____  _  _  ___  ____  _____  _  _  ___ 
# (  _ \ (_  _)(  \/  )( ___)( \( )/ __)(_  _)(  _  )( \( )/ __)
#  )(_) ) _)(_  )    (  )__)  )  ( \__ \ _)(_  )(_)(  )  ( \__ \
# (____/ (____)(_/\/\_)(____)(_)\_)(___/(____)(_____)(_)\_)(___/

# FONT SIZES ~~~~~~~~~~~~~~~~~~~~~
# Cover
companySize = 30
coverTitleSize = 60
coverPhraseSize = 25
coverFooterFontSize = 15

#Header
headerSize = 80

# Footer
footerSize = 30
pageNumberSize = 20

# Products info
idSize = 13
nameSize = 10
descriptionSize = 10

# ALIGNMENT ~~~~~~~~~~~~~~~~~~~~~~
# Cover
companyY = 220
coverTitleY = 290
coverPhrasePaddingFromTitle = 30
coverFooterSize = 120
coverPadding = coverFooterSize - 50

# Header
xTitle = 70
yTitle = headerSize - 15

# Footer
footerBottomPadding = 25 #Distancia de la compañía al borde inf
pageNumberPadding = 20 #Distancia del número a los bordes izq e inf

# Margen contenido
marginLeft = 70
marginRight = A4[0] - marginLeft
marginTop = headerSize + 10
marginBottom = 50

# Index
indexSize = 17

# Imagenes
spaceXImages = 10 # espacio entre imágenes
imageSize = ((A4[0]- 2 * marginLeft)-(3*spaceXImages))/4
nextXImages = imageSize + spaceXImages
brandHeight = 20 #El ancho de la marca es automático

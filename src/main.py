import docCreator as dc
from referencesAndData import archiveName, coverWallpaper
from importCSV import sorted_products

#  ___  ____  ____    __    ____  ____    ____   _____   ___  __  __  __  __  ____  _  _  ____ 
# / __)(  _ \( ___)  /__\  (_  _)( ___)  (  _ \ (  _  ) / __)(  )(  )(  \/  )( ___)( \( )(_  _)
#( (__  )   / )__)  /(__)\   )(   )__)    )(_) ) )(_)( ( (__  )(__)(  )    (  )__)  )  (   )(  
# \___)(_)\_)(____)(__)(__) (__) (____)  (____/ (_____) \___)(_____) (_/\/\_)(____)(_)\_) (__) 

dc.createPDF(archiveName)
dc.coverPage(coverWallpaper)
dc.index(sorted_products)
dc.addProductsToPDF(sorted_products)
dc.endPage()
dc.savePDF()
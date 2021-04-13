from PyQt5.QtCore               import QThread
from manager.DataManager        import DataManager
from manager.ImageLoaderManager import ImageLoaderManager
# Zip File
import zipfile  as ZIP
# system
import uuid     as UUID
import time     as TIME

class DataZipManager(QThread):

    def __init__(self, imgLoaderManager: ImageLoaderManager):
        super(DataZipManager, self).__init__()
        self.imgLoaderManager           = imgLoaderManager
        self.dataManager:DataManager    = None
        self.fileName                   = "default"
        
    
    def start(self, dataManager:DataManager, fileName:str="default") -> None:
        self.dataManager = dataManager
        self.fileName    = fileName
        super().start()

    def run(self):

        # print( self._dataManager.getDataDictinoary() )
        zipFile = ZIP.ZipFile( self.fileName, 'w' )

        imgWidgetList   = self.dataManager.getImageList()
        threadPool      = self.imgLoaderManager.getImageThreadPool()

        # loading haven't loaded image data
        for imgWidget in imgWidgetList:
            if( imgWidget.isLoaded() == False ):
                self.imgLoaderManager.loadRawData( imgWidget )

        # insure all the image data is loaded
        activeThead = threadPool.activeThreadCount()
        while( activeThead > 0 ):
            print( "active:" + str(activeThead) )
            TIME.sleep( 1 )
            activeThead = threadPool.activeThreadCount()
        
        serialNum = 1
        # writing data into zip file
        for imgWidget in imgWidgetList:
            netImage    = imgWidget.getImage()  # get image
            data        = netImage.getData()    # get image data
            # it Must be need to is showing, and not remove by user either
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                # data can't be null
                if( data != None ):
                    # writing data into zip file
                    zipFile.writestr( str(serialNum) + "-" + str(UUID.uuid4()) + netImage.getExtension(), data)
                    serialNum += 1

        zipFile.close()
from obj.ProgressWidget import ProgressWidget
from PyQt5.QtCore               import QEventLoop, QObject, QThread, QTimer, pyqtSignal
from manager.DataManager        import DataManager
from manager.ImageLoaderManager import ImageLoaderManager
# Zip File
import zipfile  as ZIP
# system
import uuid     as UUID
import time     as TIME

class DataZipManager(QThread):

    progressSignal = pyqtSignal( int, int, str, int )
    
    def __init__(self, imgLoaderManager: ImageLoaderManager, dataManager:DataManager):
        super(DataZipManager, self).__init__()
        self._imgLoaderManager          = imgLoaderManager
        self._dataManager               = dataManager
        self._fileName                   = "default"

    
    def start(self, fileName:str="default") -> None:
        self._fileName    = fileName
        super().start()
        

    def run(self):
        # print( self._dataManager.getDataDictinoary() )
        zipFile = ZIP.ZipFile( self._fileName, 'w' )

        imgWidgetList   = self._dataManager.getImageList()
        threadPool      = self._imgLoaderManager.getImageThreadPool()

        listLength      = len( imgWidgetList )
        listCount       = 0
        self.progressSignal.emit( listCount, listLength, "開始下載圖片......", ProgressWidget.PROGRESS_WIDGET_SHOW )
  
        # loading haven't loaded image data
        for imgWidget in imgWidgetList:
            if( imgWidget.isLoaded() == False ):
                self._imgLoaderManager.loadRawData( imgWidget )
            self.progressSignal.emit(  listCount, listLength, "正在從網路取得資料...... ( {} / {} )".format( listCount, listLength ), ProgressWidget.PROGRESS_WIDGET_NORML )  
            listCount += 1

        self.progressSignal.emit(  listCount, listLength, "準備開始下載檔案......", ProgressWidget.PROGRESS_WIDGET_NORML )  
        self._delay( 1000 ) # Delay one second

        # ---------------------------------------------------------------------
        # insure all the image data is loaded
        activeThead = threadPool.activeThreadCount()
        while( activeThead > 0 ):
            print( "active:" + str(activeThead) )
            TIME.sleep( 1 )
            activeThead = threadPool.activeThreadCount()

        # ---------------------------------------------------------------------
        serialNum = 1
        dataLengeth = self._dataManager.countData()
        self.progressSignal.emit(  serialNum, dataLengeth, "正在壓縮圖片檔案...... ( {} / {} )".format( serialNum - 1, dataLengeth ), ProgressWidget.PROGRESS_WIDGET_NORML )
        # writing data into zip file
        for imgWidget in imgWidgetList:
            netImage    = imgWidget.getImage()          # get image
            data        = imgWidget.getImageData()      # get image data
            # it Must be need to is showing, and not remove by user either
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                # data can't be null
                if( data != None ):
                    # writing data into zip file
                    zipFile.writestr( str(serialNum) + "-" + str(UUID.uuid4()) + netImage.getExtension(), data)
                    serialNum += 1

                    self.progressSignal.emit(  serialNum, dataLengeth, "正在壓縮圖片檔案...... ( {} / {} )".format( serialNum - 1, dataLengeth ), ProgressWidget.PROGRESS_WIDGET_NORML )  

        zipFile.close()

        self.progressSignal.emit(  serialNum, dataLengeth, "下載完成！", ProgressWidget.PROGRESS_WIDGET_NORML )  
        self._delay( 2000 )                 # Delay one second
        self.progressSignal.emit(  serialNum, dataLengeth, "", ProgressWidget.PROGRESS_WIDGET_HIDE )  

    def getProgressSignal( self ):
        return self.progressSignal

    def _delay( self, ms: int ):
        """ single shot delay"""
        loop = QEventLoop()
        QTimer.singleShot( ms, lambda x=loop: x.quit() )
        loop.exec()
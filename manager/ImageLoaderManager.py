
from PyQt5.QtCore import (QThreadPool, QThread, QEventLoop, QTimer)

class ImageLoaderManager():

    def __init__(self, centerScrollArea ):
        self._centerScrollArea  = centerScrollArea
        self._flowLayout        = centerScrollArea.widget().layout()
        self._threadPool        = QThreadPool()

        self._centerScrollArea.verticalScrollBar().valueChanged.connect( self._loadImg )
        
    def load( self, imgList: list):
        """first loading"""
        self._imgWidgetList = imgList
        self._notLoadList   = imgList
        if( len(self._imgWidgetList) > 0 ):
            i = 0
            for imgWidget in self._imgWidgetList:
                self._flowLayout.addWidget( imgWidget ) 

                # preload 10 img
                if i < 10:
                     self._work( imgWidget )
               
            return True
        else:
            print( 'No images can load！' )
            return False

        

    def _loadImg( self ):
        """scroll bar loading event"""
        for imgWidget in self._notLoadList:
            self._work( imgWidget )

    def _work(self, imgWidget):
        """let image loading resourse from web"""
        if( self._isVisibleWidget( imgWidget ) ):
            self._notLoadList.remove( imgWidget )
            imgThread = imgWidget.getImageLoaderThread()

            self.delay( 250 )    # add a delay prevent too frequcy getting img
            self._threadPool.start( imgThread )
    
    def delay( self, ms: int ):
        """ single shot delay"""
        loop = QEventLoop()
        QTimer.singleShot( ms, lambda x=loop: x.quit() )
        loop.exec()

    def _isVisibleWidget(self, imgWidget):
        """check this obj is in sight"""
        if not imgWidget.visibleRegion().isEmpty():
            return True
        return False     

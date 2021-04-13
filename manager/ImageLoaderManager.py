
from typing import List
from obj.ImageWidget import ImageWidget
from PyQt5.QtCore import (QThreadPool, QEventLoop, QTimer)

class ImageLoaderManager():

    def __init__(self, centerScrollArea ):
        self._centerScrollArea  = centerScrollArea
        self._flowLayout        = centerScrollArea.widget().layout()
        self._threadPool        = QThreadPool()
        self._imgWidgetList     = List[ImageWidget]
        self._centerScrollArea.verticalScrollBar().valueChanged.connect( self._loadImg )
        
    def load( self, imgList: list):
        """first loading"""
        self._imgWidgetList = imgList
        if( len(self._imgWidgetList) > 0 ):
            i = 0
            for imgWidget in self._imgWidgetList:
                self._flowLayout.addWidget( imgWidget ) 

                # preload 10 img
                if i < 10:
                    self._work( imgWidget, True )
                    i += 1
               
            return True
        else:
            print( 'No images can load！' )
            return False

        

    def _loadImg( self ):
        """scroll bar loading event"""
        for imgWidget in self._imgWidgetList:
            if( imgWidget.isLoaded() == False ):
                self._work( imgWidget )

    def _work(self, imgWidget: ImageWidget, forceLoad: bool = False):
        """let image loading resourse from web"""
        if( self._isVisibleWidget( imgWidget ) or forceLoad ):
            imgWidget.setIsLoaded( True )
            imgThread = imgWidget.getImageLoaderThread()

            self._delay( 250 )    # add a delay prevent too frequcy getting img
            self._threadPool.start( imgThread )

    def loadRawData( self, imgWidget:ImageWidget ):
        """ when user saving data, but image haven't load data"""
        imgWidget.setIsLoaded( True )
        imgThread = imgWidget.getImageLoaderThread()
        self._delay( 250 )
        self._threadPool.start( imgThread )

    def getImageThreadPool( self ) -> QThreadPool:
        return self._threadPool

    def _delay( self, ms: int ):
        """ single shot delay"""
        loop = QEventLoop()
        QTimer.singleShot( ms, lambda x=loop: x.quit() )
        loop.exec()

    def _isVisibleWidget(self, imgWidget):
        """check this obj is in sight"""
        if not imgWidget.visibleRegion().isEmpty():
            return True
        return False     

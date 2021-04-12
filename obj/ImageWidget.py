
from obj.NetImage import NetImage
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QLabel, QWidget) 
from PyQt5.QtGui        import (QImage, QPixmap)
from PyQt5.QtCore       import QByteArray, QPropertyAnimation, QSize, Qt, QRunnable

import os as OS
# Get Image Form URL
import urllib.request as URL_REQUEST
import urllib.error

# 設計好的ui檔案路徑
qtImgCreatorFile = OS.getcwd() + OS.sep + "ui" + OS.sep + "imageview.ui"  
# 讀入用Qt Designer設計的GUI layout
uiImageWidget, QtImgBaseClass = uic.loadUiType(qtImgCreatorFile)   



class ImageWidget(QtWidgets.QWidget, uiImageWidget):

    class ImageLoaderThread(QRunnable):
        def __init__(self, imageWidget):
            super(ImageWidget.ImageLoaderThread, self).__init__()
            self.imageWidget = imageWidget

        def run(self):
            try:
                self.imageWidget.loadingImage()
            except urllib.error.HTTPError:
                print( 'HTTP Error' )
                self.imageWidget.getImage().print()
                self.imageWidget.deleteLater()          # delete itself
                self.imageWidget = None              


    MAX_IMAGE_SIZE = 324
    def __init__(self, netImage):
        QtWidgets.QWidget.__init__(self)
        uiImageWidget.__init__(self)
        self.setupUi(self)

        self._authorNameLabel    = self.findChild(QLabel, name='authorNameLabel')    # label of author
        self._authorIDLabel      = self.findChild(QLabel, name='authorIDLabel')      # label of author ID
        self._floorLabel         = self.findChild(QLabel, name='floorLabel')         # label of floor
        self._GPLabel            = self.findChild(QLabel, name='gpLabel')            # label of GP
        self._BPLabel            = self.findChild(QLabel, name='bpLabel')            # label of BP

        self._authorNameLabel.setText( netImage.getAuthorName() )
        self._authorIDLabel.setText(   netImage.getAuthorID() )
        self._floorLabel.setText( str( netImage.getFloor() ) )
        self._GPLabel.setText(    str( netImage.getGP() ) )
        self._BPLabel.setText(    str( netImage.getBP() ) )
        # -------------------------------------------------------------------
        self._imageLabel:QLabel = self.findChild(QLabel, name='imageLabel')          # showImageLabel
        self._url:str           = netImage.getImageUrl()
        # -------------------------------------------------------------------
        self._netImage:NetImage = netImage
        self._isLoaded:bool     = False
        self._imageLoaderThread = self.ImageLoaderThread( self )

    def getImage( self ) -> NetImage:
        return self._netImage

    def getImageLoaderThread(self) -> ImageLoaderThread:
        """use to put in a thread pool to loading images"""
        return self._imageLoaderThread

    def isLoaded( self ) -> bool:
        """ get the image is loaded"""
        return self._isLoaded

    def setIsLoaded( self, flag:bool ):
        """set the flag image are loaded"""
        self._isLoaded = flag 

    def loadingImage(self):
        """ loading image from web"""
        data    = URL_REQUEST.urlopen( self._url ).read()
        
        image = QImage()
        if( image.loadFromData( data ) == False ):
            self.imageLabel.setText( "圖片讀取失敗！" )
        else:
            maxlen      = max( image.width(), image.height() )
            scaleRate   = 1.0 if maxlen < self.MAX_IMAGE_SIZE else (float(maxlen) / self.MAX_IMAGE_SIZE)
            pixmap      = QPixmap( image ).scaled( int(image.width() / scaleRate), int(image.height() / scaleRate), Qt.IgnoreAspectRatio,  Qt.SmoothTransformation)
            self.imageLabel.setPixmap( pixmap )

    def test( self ):


        formerSize = QSize( self.size() ) # storing previous geometry in order to be able to restore it later

        self.hideAnimation = QPropertyAnimation( self, QByteArray().append( "size" ) )
        self.hideAnimation.setDuration( 500 ) # chose the value that fits you
        self.hideAnimation.setStartValue( formerSize )
        # computing final geometry
        # endTopLeftCorner = QPoint( self.pos() + QPoint( 0, self.height() ) )
        finalSize = QSize( 0, 0 )
        self.hideAnimation.setEndValue( finalSize )

        self.hideAnimation.start()
        
        

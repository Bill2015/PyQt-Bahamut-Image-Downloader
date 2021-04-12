
from obj.NetImage       import NetImage
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QLabel, QPushButton, QSizePolicy) 
from PyQt5.QtGui        import (QImage, QPixmap)
from PyQt5.QtCore       import QByteArray, QPropertyAnimation, Qt, QRunnable, QPoint, QRect

import os as OS
# Get Image Form URL
import urllib.request as URL_REQUEST
import urllib.error

# 設計好的ui檔案路徑
qtImgCreatorFile = OS.getcwd() + "\\".join( ["","resource", "ui", "imageview.ui"] ) 
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

    # =========================================================================================================
    MAX_IMAGE_SIZE = 324
    MAX_WIDGET_HEIGHT_SIZE = 384

    def __init__(self, netImage):
        QtWidgets.QWidget.__init__(self)
        uiImageWidget.__init__(self)
        self.setupUi(self)

        self._authorNameLabel:QLabel    = self.findChild(QLabel, name='authorNameLabel')    # label of author
        self._authorIDLabel:QLabel      = self.findChild(QLabel, name='authorIDLabel')      # label of author ID
        self._floorLabel:QLabel         = self.findChild(QLabel, name='floorLabel')         # label of floor
        self._GPLabel:QLabel            = self.findChild(QLabel, name='gpLabel')            # label of GP
        self._BPLabel:QLabel            = self.findChild(QLabel, name='bpLabel')            # label of BP
        self._deleteButton:QPushButton  = self.findChild(QPushButton, name='deleteButton')        # button of delete

        self._authorNameLabel.setText( netImage.getAuthorName() )
        self._authorIDLabel.setText(   netImage.getAuthorID() )
        self._floorLabel.setText( str( netImage.getFloor() ) )
        self._GPLabel.setText(    str( netImage.getGP() ) )
        self._BPLabel.setText(    str( netImage.getBP() ) )
        # -------------------------------------------------------------------
        # image netowrk 
        self._imageLabel:QLabel = self.findChild(QLabel, name='imageLabel')          # showImageLabel
        self._url:str           = netImage.getImageUrl()
        
        # -------------------------------------------------------------------
        # image loading
        self._netImage:NetImage = netImage
        self._isLoaded:bool     = False
        self._imageLoaderThread = self.ImageLoaderThread( self )

        # -------------------------------------------------------------------
        # image showing & hiding
        self._isVisiable:bool   = True
        self._originGeometry:QRect
        self._originPos:QPoint
        self._showAnimation = QPropertyAnimation( self, QByteArray().append( "geometry" ) )
        self._hideAnimation = QPropertyAnimation( self, QByteArray().append( "geometry" ) )
        self.setMinimumHeight( ImageWidget.MAX_WIDGET_HEIGHT_SIZE )
        self.setSizePolicy( QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed ) )

        # -------------------------------------------------------------------
        self._isRemoved         = False
        # -------------------------------------------------------------------
        # initial event
        self._initialEvent()


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

    def isVisible(self) -> bool:
        return self._isVisiable

    def isRemoved( self ) -> bool:
        """ get this widget is removed by user"""
        return self._isRemoved

    def setRemoved( self, flag:bool ):
        """ setting isRemoved flag """
        self._isRemoved = flag

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
            self._netImage.setImageData( data ) # setting image byte data into NetImage    

    def _fixedHeight( self ):
        """ fixed height to make animation more smooth """
        self._isVisiable = True
        self.setMinimumHeight( ImageWidget.MAX_WIDGET_HEIGHT_SIZE )
        self.setSizePolicy( QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed ) )

    def _pressRemoveButtonEvent( self ):
        """ when user remove image """
        self._isRemoved = True
        self.hideWidget()

    def _initialEvent( self ):
        """ initial event """
        self._deleteButton.clicked.connect( self._pressRemoveButtonEvent )
        self._hideAnimation.finished.connect( self.hide )
        self._showAnimation.finished.connect( self._fixedHeight )


    def hideWidget( self ):
        """ hiding Net Image animation"""
        self._isVisiable = False
        self.setMinimumHeight( 0 )
        self.setSizePolicy( QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Preferred ) )

        self._originGeometry = QRect( self.geometry() ) # storing previous geometry in order to be able to restore it later
        self._originPos      = QPoint( self.pos() )

        self._hideAnimation.setDuration( 250 ) 
        self._hideAnimation.setStartValue( self._originGeometry )
        finalSize = QRect( self._originPos.x(), self._originPos.y() + (self._originGeometry.height() / 2), self._originGeometry.width(), 0 )
        self._hideAnimation.setEndValue( finalSize )
        self._hideAnimation.start()

    def showWidget( self ):
        """ showing Net Image animation"""
        self.show()
        startSize = QRect( self._originPos.x(), self._originPos.y() + (self._originGeometry.height() / 2), self._originGeometry.width(), 0 )
        self._showAnimation.setDuration( 250 )
        self._showAnimation.setStartValue( startSize )
        self._showAnimation.setEndValue( self._originGeometry )
        self._showAnimation.start()
        

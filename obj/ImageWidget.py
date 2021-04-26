
from obj.NetImage       import NetImage
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QLabel, QPushButton, QSizePolicy) 
from PyQt5.QtGui        import (QImage, QMovie, QPixmap)
from PyQt5.QtCore       import QBuffer, QByteArray, QIODevice, QObject, QPropertyAnimation, Qt, QRunnable, QPoint, QRect, pyqtSignal

import os as OS
import traceback    as TRACE

# Get Image Form URL
import urllib.request as URL_REQUEST
import urllib.error


class ImageWidget(QtWidgets.QWidget):
    class ImageLoaderThread(QRunnable):
        def __init__(self, imageWidget ):
            super(ImageWidget.ImageLoaderThread, self).__init__()
            self._imageWidget: ImageWidget = imageWidget


        def run(self):
            try:
                if( self._imageWidget != None  ):
                    self._imageWidget.loadRawData()
                    if( self._imageWidget.isLoadRawData() == False ):
                        if( self._imageWidget._showImgSignal != None ):
                            self._imageWidget._showImgSignal.emit()
            except urllib.error.HTTPError:
                print( 'HTTP Error' )
                TRACE.print_exc()
                self._imageWidget.setIsLoadFailed( True )
                self._imageWidget.getImage().print()
                self._imageWidget.deleteLater()          # delete itself
                self._imageWidget = None              

    # =========================================================================================================
    _MAX_IMAGE_SIZE = 324
    _MAX_WIDGET_HEIGHT_SIZE = 384
    _REQUEST_HEADER = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    # a signal to let the thread call on it
    _showImgSignal = pyqtSignal()

    UI_RESOURCE_PATH = OS.getcwd() + "\\".join( ["","resource", "ui",""] ) 

    def __init__(self, netImage):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi( ImageWidget.UI_RESOURCE_PATH + "imageview.ui", self )

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

        # -------------------------------------------------------------------
        # image loading
        self._netImage:NetImage     = netImage
        self._isLoaded:bool         = False
        self._isLoadFailed:bool     = False
        self._imageLoaderThread     = self.ImageLoaderThread( self )
        self._isLoadRawData:bool    = False
        self._imageData:bytearray   = None
        self._imageShowing:bool     = False
        self._showImgSignal.connect( self.showImage )

        # -------------------------------------------------------------------
        # image showing & hiding
        self._isVisiable:bool       = True
        self._originGeometry:QRect  = None
        self._originPos:QPoint      = None
        self._showAnimation         = QPropertyAnimation( self, QByteArray().append( "geometry" ) )
        self._hideAnimation         = QPropertyAnimation( self, QByteArray().append( "geometry" ) )
        self.setMinimumHeight( ImageWidget._MAX_WIDGET_HEIGHT_SIZE )
        self.setSizePolicy( QSizePolicy( QSizePolicy.Preferred, QSizePolicy.Fixed ) )

        # -------------------------------------------------------------------
        # user remove image
        self._isRemoved         = False
        # -------------------------------------------------------------------
        
        # -------------------------------------------------------------------
        self._buffer:QBuffer        = None
        self._moive:QMovie          = None
        self._qByte:QByteArray      = None
        # initial event
        self._initialEvent()


    def getImage( self ) -> NetImage:
        return self._netImage

    def getImageLoaderThread(self) -> ImageLoaderThread:
        """use to put in a thread pool to loading images"""
        return self._imageLoaderThread

    def getImageData( self ) -> bytearray:
        return self._imageData

    def isLoadRawData( self ):
        """get load raw data flag"""
        return self._isLoadRawData

    def isImageShowing( self ):
        """ get the image is showing in the label """
        return self._imageShowing

    def isLoaded( self ) -> bool:
        """ get the image is loaded"""
        return self._isLoaded
    
    def isLoadFailed( self ) -> bool:
        """ get the image is load Failed"""
        return self._isLoadFailed    

    def setIsLoaded( self, flag:bool ):
        """set the flag image are loaded"""
        self._isLoaded = flag 

    def setIsLoadFailed( self, flag:bool ):
        """set the flag image are loaded Failed"""
        self._isLoadFailed = flag 


    def setLoadRawData( self, flag:bool ):
        """set load raw data"""
        self._isLoadRawData = flag

    def isVisible(self) -> bool:
        return self._isVisiable

    def isRemoved( self ) -> bool:
        """ get this widget is removed by user"""
        return self._isRemoved

    def setRemoved( self, flag:bool ):
        """ setting isRemoved flag """
        self._isRemoved = flag

    def loadRawData( self ):
        """ load raw Data """
        imgRequest          = URL_REQUEST.Request( self._netImage.getImageUrl(), headers=self._REQUEST_HEADER )
        self._imageData     = URL_REQUEST.urlopen( imgRequest ).read()

    def showImage( self ):
        """ loading image from web"""
        self._imageShowing = True
        
        if( self._netImage.isGif() ):
            self._qByte     = QByteArray( self._imageData )
            self._buffer    = QBuffer( self._qByte )
            if( self._buffer.open( QIODevice.ReadOnly ) ):
                self._moive = QMovie( self._buffer, b"GIF" )
                self._moive.setDevice( self._buffer )
                self._moive.setCacheMode( QMovie.CacheAll )
                self._imageLabel.setMovie( self._moive )
                self._moive.start()

        else:
            image = QImage()
            if( image.loadFromData( self._imageData ) == False ):
                return
            else:
                maxlen      = max( image.width(), image.height() )
                scaleRate   = 1.0 if maxlen < self._MAX_IMAGE_SIZE else (float(maxlen) / self._MAX_IMAGE_SIZE)
                pixmap      = QPixmap( image ).scaled( int(image.width() / scaleRate), int(image.height() / scaleRate), Qt.IgnoreAspectRatio,  Qt.SmoothTransformation)
                self._imageLabel.setPixmap( pixmap )    

    def _fixedHeight( self ):
        """ fixed height to make animation more smooth """
        self._isVisiable = True
        self.setMinimumHeight( ImageWidget._MAX_WIDGET_HEIGHT_SIZE )
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
        

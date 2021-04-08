
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QLabel) 
from PyQt5.QtGui        import (QImage, QPixmap)
from PyQt5.QtCore       import Qt, QRunnable

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

        self.authorNameLabel    = self.findChild(QLabel, name='authorNameLabel')    # label of author
        self.authorIDLabel      = self.findChild(QLabel, name='authorIDLabel')      # label of author ID
        self.floorLabel         = self.findChild(QLabel, name='floorLabel')         # label of floor
        self.GPLabel            = self.findChild(QLabel, name='gpLabel')            # label of GP
        self.BPLabel            = self.findChild(QLabel, name='bpLabel')            # label of BP

        self.authorNameLabel.setText( netImage.getAuthorName() )
        self.authorIDLabel.setText(   netImage.getAuthorID() )
        self.floorLabel.setText( str( netImage.getFloor() ) )
        self.GPLabel.setText(    str( netImage.getGP() ) )
        self.BPLabel.setText(    str( netImage.getBP() ) )
        # -------------------------------------------------------------------
        self.imageLabel        = self.findChild(QLabel, name='imageLabel')          # showImageLabel
        self.url               = netImage.getImageUrl()
        # -------------------------------------------------------------------
        self.netImage          = netImage

        self.imageLoaderThread = self.ImageLoaderThread( self )

    def getImage( self ):
        return self.netImage

    def getImageLoaderThread(self):
        """use to put in a thread pool to loading images"""
        return self.imageLoaderThread

    def loadingImage(self):
        """ loading image from web"""
        data    = URL_REQUEST.urlopen( self.url ).read()
        
        image = QImage()
        if( image.loadFromData( data ) == False ):
            self.imageLabel.setText( "圖片讀取失敗！" )
        else:
            maxlen      = max( image.width(), image.height() )
            scaleRate   = 1.0 if maxlen < self.MAX_IMAGE_SIZE else (float(maxlen) / self.MAX_IMAGE_SIZE)
            pixmap      = QPixmap( image ).scaled( int(image.width() / scaleRate), int(image.height() / scaleRate), Qt.IgnoreAspectRatio,  Qt.SmoothTransformation)
            self.imageLabel.setPixmap( pixmap )


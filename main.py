from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import (QFileDialog, QLabel, QLineEdit, QPushButton, QScrollArea, QSpinBox, QSlider)
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import * 


# 原生 Python 程式
import os           as OS
import sys          as SYSTEM

# Zip File
import zipfile as ZIP


from obj.FlowLayout             import FlowLayout
from obj.QRangeSlider           import QRangeSlider
from obj.QSliderLineEdit        import QSliderLineEdit
from manager.DataManager        import DataManager
from manager.ImageLoaderManager import ImageLoaderManager
from manager.NetCrawlerManager  import NetCrawlerManager



# 設計好的ui檔案路徑
qtCreatorFile = OS.getcwd() + "\\".join( ["","resource", "ui", "mainwindow.ui"] ) 
# 讀入用Qt Designer設計的GUI layout
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)   

# Python的多重繼承 MainUi 繼承自兩個類別
class MainUi(QtWidgets.QMainWindow, Ui_MainWindow):
            
    # =========================================================
    # ==================== UI main program ====================
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        # 取得內部物件
        self._searchButton:QPushButton       = self.findChild(QPushButton, name='searchButton')      # 搜尋按鈕
        self._searchEditText:QLineEdit       = self.findChild(QLineEdit, name='searchTextEdit')      # search text
        self._centerScrollArea:QScrollArea   = self.findChild(QScrollArea, name='centerScrollArea')  # center scroll area
        self._resetButton:QPushButton        = self.findChild(QPushButton, name='resetButton')       # reset filter button
        self._downloadButton:QPushButton     = self.findChild(QPushButton, name='downloadButton')    # download button
        # floor text
        self._floorEditText       = [self.findChild(QSpinBox, name='floorTextEditStart') ,self.findChild(QSpinBox, name='floorTextEditStart')]

        # gp & bp slider
        self._GpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='gpSlider'),  self.findChild(QLineEdit, name='gpLineEdit'), "爆" )
        self._BpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='bpSlider'),  self.findChild(QLineEdit, name='bpLineEdit'), "X" )

        # initial Image flowLayout 
        self._flowLayout = FlowLayout()
        self._flowLayout.setSpacing( 2 )
        self._centerScrollArea.widget().setLayout( self._flowLayout )

        # initial img loader manager
        self._imgLoaderManager = ImageLoaderManager( self._centerScrollArea )

        self._dataManager      = DataManager()

        self._initialEvent()

    # 初始化影片顯示區域
    def _pressSearch(self):
        # # downloading image
        # downloadUrl = 'https://www.mymypic.net/data/attachment/album/202103/30/134312jgtytf14jscepftu.gif'
        # data2 = URL_REQUEST.urlopen( downloadUrl ).read()
        # filePath = OS.getcwd() + OS.sep + "testImage.gif"
        # with open( filePath, 'wb' ) as localFile:
        #     localFile.write( data2 )


        searchUrl = self._searchEditText.text()

        # check the url is legal
        if( searchUrl == "" ):
            return

        try:
            imgWidgetList = NetCrawlerManager().getData( searchUrl, [1, 1] )
            self._imgLoaderManager.load( imgWidgetList )
            self._dataManager.setImageList( imgWidgetList )
        # Occuer an error
        except Exception as e: 
            print( e )
            print( "URL format error" )

    # ---------------------------------------------------------------
    def _downloadAsZip( self ):
        """ download whole images as a zip """
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"壓縮檔下載","","Zip Files (*.zip)", options=options)
        

        # print( self._dataManager.getDataDictinoary() )
        zipFile = ZIP.ZipFile( fileName, 'w' )
        # writing data into zip file
        dataDict = self._dataManager.getDataDictinoary()
        for key in dataDict:
            zipFile.writestr( dataDict[ key ][ DataManager.FLIE_NAME ], dataDict[ key ][ DataManager.DATA_NAME ] )
        zipFile.close()
    # ---------------------------------------------------------------
    def _resetFilterEvent( self ):
        """press reset button event"""
        self._GpSliderEdit.setValue( 0 )
        self._BpSliderEdit.setValue( 1000 )

        # initial image widget showing
        for imgWidget in self._dataManager.getImageList():
            if( imgWidget.isVisible() == False ):
                imgWidget.setRemoved( False )   # restore the image that delete by user
                imgWidget.showWidget()
    # ---------------------------------------------------------------
    def _filterEvent( self ):
        """gp and bp filter event"""
        gpPoint = self._GpSliderEdit.value()
        bpPoint = self._BpSliderEdit.value()

        # check each image widget
        for img in self._dataManager.getImageList():
            netImage = img.getImage()

            # check gp and bp range
            if netImage.getGP() < gpPoint or netImage.getBP() >= bpPoint:
                if( img.isVisible() == True ):
                    img.hideWidget()
            # make sure that widget is not visiable, and not remove by user
            elif( img.isVisible() == False and img.isRemoved() == False ):
                img.showWidget()    
            

    def _initialEvent( self ):
        """inital all the event"""
        self._searchButton.clicked.connect( self._pressSearch )
        self._GpSliderEdit.initialEvent()
        self._BpSliderEdit.initialEvent()
        self._GpSliderEdit.getSlider().valueChanged.connect( self._filterEvent )
        self._BpSliderEdit.getSlider().valueChanged.connect( self._filterEvent )

        self._resetButton.clicked.connect( self._resetFilterEvent )

        self._downloadButton.clicked.connect( self._downloadAsZip )






# =========================================================
# ======================= 啟動程式 ========================
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication( SYSTEM.argv )
        window = MainUi()
        window.show()
        app.exec_()

    run_app()
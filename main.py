from manager.HistoryManager import HistoryManager
from obj.FilterWidget import FilterWidget
from obj.ProgressWidget import ProgressWidget
from PyQt5              import QtWidgets, uic
from PyQt5.QtWidgets    import (QCheckBox, QFileDialog, QLineEdit, QPushButton, QScrollArea, QSpinBox, QVBoxLayout, QWidget)
from PyQt5.QtGui        import *
from PyQt5.QtCore       import * 


# origin python
import os               as OS
import sys              as SYSTEM
# request
import urllib.error     as URL_ERROR


from obj.FlowLayout             import FlowLayout
from obj.WarningDialog          import WarningDialog
from manager.DataManager        import DataManager
from manager.ImageLoaderManager import ImageLoaderManager
from manager.NetCrawlerManager  import NetCrawlerManager
from manager.DataZipManager     import DataZipManager
from manager.CrashLogManager    import CrashLogManager




# Python的多重繼承 MainUi 繼承自兩個類別
class MainUi(QtWidgets.QMainWindow):
    UI_RESOURCE_PATH = OS.getcwd() + "\\".join( ["","resource", "ui"] ) 
    # =========================================================
    # ==================== UI main program ====================
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        uic.loadUi( MainUi.UI_RESOURCE_PATH + "\\" + "mainwindow.ui", self )

        # add Filter widget
        self._filterWidget = FilterWidget()
        self.findChild(QWidget, name='filterWidget').layout().addWidget(  self._filterWidget )
        self._filterWidget.getSortSignal().connect( self._sortEvent )
        

        # getting inner object
        self._searchButton:QPushButton       = self.findChild(QPushButton, name='searchButton')      # 搜尋按鈕
        self._searchEditText:QLineEdit       = self.findChild(QLineEdit, name='searchTextEdit')      # search text
        self._centerScrollArea:QScrollArea   = self.findChild(QScrollArea, name='centerScrollArea')  # center scroll area
        self._clearPreCheckBox:QCheckBox     = self.findChild(QCheckBox, name='clearPreSeachCheckBox') # clearPreSearch CheckBox
        
        # floor text
        self._floorEditText       = [self.findChild(QSpinBox, name='floorTextEditStart') ,self.findChild(QSpinBox, name='floorTextEditEnd')]

        # initial Image flowLayout 
        self._flowLayout = FlowLayout()
        self._flowLayout.setSpacing( 2 )
        self._centerScrollArea.widget().setLayout( self._flowLayout )

        # initial progress bar
        self._downloadWidget   = ProgressWidget()
        self.findChild(QVBoxLayout, name='centerVerticalLayout').addWidget( self._downloadWidget )
        
        # initial manager
        self._imgLoaderManager = ImageLoaderManager( self._centerScrollArea )   # initial img loader manager
        self._dataManager      = DataManager()                                  # initial image data manager
        self._dataZipManager   = DataZipManager(  self._imgLoaderManager, self._dataManager )      # initial image save manager
        self._dataZipManager.getProgressSignal().connect( self._updateZipProgress )
        self._crashManager     = CrashLogManager()
        self._historyManager   = HistoryManager()
        self._netCrawlerManager= NetCrawlerManager()

        # initial warning messsage 
        self._warningBox       = WarningDialog( self )

        
        
        self._historyInitialLoad()
        self._initialEvent()


    def _historyInitialLoad( self ):
        try:
            self._historyManager.load()
        # Error Message is history data format error
        except:
            self._warningBox.show( "下載歷史紀錄讀取失敗！\n可能是格式錯誤或者其他問題！" )

    # ======================================================================
    def _pressSearch(self):
        """ when search button press """

        # get search text
        searchUrl = self._searchEditText.text()

        # Error Message check the url is legal
        if( searchUrl == "" ):
            self._warningBox.show( "搜尋欄不可為空！" )
            return
        
        # check the user is want to clear previous search result
        clearPreSearch = self._clearPreCheckBox.isChecked() 
        if( clearPreSearch == True ):
            self._dataManager.clearSearchData()
            self._flowLayout.clearAllWidget()

        imgWidgetList = []
        try:
            floor = [ int(self._floorEditText[0].text()), int(self._floorEditText[1].text()) ]

            imgWidgetList = self._netCrawlerManager.getData( searchUrl, floor )
            [bsn, snA, floors, date] = self._netCrawlerManager.getNowTaskInfo()
            self._historyManager.addHistory( bsn, snA, floors, date )
        # Occuer an error
        except Exception as e: 
            # Error Message
            if( type( e ) == URL_ERROR.URLError ):
                self._crashManager.writeCrashLog( str( e ) )
            else:
                self._warningBox.show( "URL 格式錯誤！" )    
        else:
            # check the loading is success or not
            if( self._imgLoaderManager.load( imgWidgetList ) == True ):
                try:
                    if( clearPreSearch == True ):
                        self._dataManager.setImageList( imgWidgetList )
                    else:
                        self._dataManager.apendImageList( imgWidgetList )
                    # accoding GP and BP update image
                    self._filterEvent()
                # Occuer an error
                except Exception as e: 
                    # Error Message image loading failed
                    self._warningBox.show( "圖片讀取時發生錯誤！" )
                    self._crashManager.writeCrashLog( str( e ) )
            else:
                # Error Message no any images can't be loaded
                self._warningBox.show( "沒有任何圖片可以讀取喔！" )
        

    # ======================================================================
    def _downloadAsZip( self ):
        """ download whole images as a zip """

        # Error Message if there is no image can be downloaded
        if( self._dataManager.isImageEmpty() == True ):
            self._warningBox.show( "目前沒有任何一張圖可以下載喔！" )
            return

        options     = QFileDialog.Options()
        fileName, _ = QFileDialog.getSaveFileName(self,"壓縮檔下載","","Zip Files (*.zip)", options=options)
        
        # Error Message file name can't not be null
        if( fileName == "" ):
            self._warningBox.show( "檔案名稱不可為空！" )
            return

        self._dataZipManager.start( fileName )
        
    # ======================================================================
    def _updateZipProgress( self, val:int, max:int, text:str, status:int=ProgressWidget.PROGRESS_WIDGET_NORML ):
        """when zip image file, update progress"""
        if( status == ProgressWidget.PROGRESS_WIDGET_SHOW ):
            self._downloadWidget.show()
        elif( status == ProgressWidget.PROGRESS_WIDGET_HIDE ):
            self._downloadWidget.hide()
        self._downloadWidget.setMaxValue( max )
        self._downloadWidget.setValue( val )
        self._downloadWidget.setText( text )

    # ======================================================================
    def _resetFilterEvent( self ):
        """press reset button event"""
        self._filterWidget.getGpSliderEidt().setValue( 0 )
        self._filterWidget.getBpSliderEidt().setValue( 1000 ) 
        # initial image widget showing
        for imgWidget in self._dataManager.getImageList():
            if( imgWidget.isVisible() == False ):
                imgWidget.setRemoved( False )   # restore the image that delete by user
                imgWidget.showWidget()
    
    # ======================================================================
    def _filterEvent( self ):
        """gp and bp filter event"""
        gpPoint = self._filterWidget.getGpSliderEidt().value()
        bpPoint = self._filterWidget.getBpSliderEidt().value()

        try:
            self._imgLoaderManager.loadImg()
            # check each image widget
            for img in self._dataManager.getImageList():
                # make sure the image is loaded successful
                if( img.isLoadFailed() == False ):
                    netImage = img.getImage()

                    # check gp and bp range
                    if netImage.getGP() < gpPoint or netImage.getBP() >= bpPoint:
                        if( img.isVisible() == True ):
                            img.hideWidget()
                    # make sure that widget is not visiable, and not remove by user
                    elif( img.isVisible() == False and img.isRemoved() == False ):
                        img.showWidget() 
        # Error Message if exception happed       
        except Exception as e:
            if( type( e ) != TypeError ):
                self._crashManager.writeCrashLog( str( e ) )
    
    # ======================================================================
    def _sortEvent( self, sortType:int, order:bool ):
        if( self._dataManager.isImageEmpty() ):
            return

        if( sortType == FilterWidget.SORT_BY_FLOOR ):
            self._dataManager.getImageList().sort(key=lambda obj: obj.getImage().getFloor(), reverse=order)
        elif( sortType == FilterWidget.SORT_BY_GP ):
            self._dataManager.getImageList().sort(key=lambda obj: obj.getImage().getGP(), reverse=order)
        elif( sortType == FilterWidget.SORT_BY_BP ):
            self._dataManager.getImageList().sort(key=lambda obj: obj.getImage().getBP(), reverse=order)
        
        self._imgLoaderManager.reload( self._dataManager.getImageList() )
        
    # ======================================================================
    def _initialEvent( self ):
        """inital all the event"""
        self._searchButton.clicked.connect( self._pressSearch )
      
        self._filterWidget.getGpSliderEidt().getSlider().valueChanged.connect( self._filterEvent )
        self._filterWidget.getBpSliderEidt().getSlider().valueChanged.connect( self._filterEvent )

        self._filterWidget.getResetButton().clicked.connect( self._resetFilterEvent )

        self._downloadWidget.getDownloadButton().clicked.connect( self._downloadAsZip )






# =========================================================
# ======================= 啟動程式 ========================
if __name__ == "__main__":
    def run_app():
        app = QtWidgets.QApplication( SYSTEM.argv )
        window = MainUi()
        window.show()
        app.exec_()

    try:
        run_app()
    except Exception as e: 
        print("main crashed. Error: %s", e)

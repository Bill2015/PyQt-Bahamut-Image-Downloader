
from PyQt5.QtCore import pyqtSignal
from obj.ToggleButton       import ToggleButton
from PyQt5.QtWidgets        import QGroupBox, QLineEdit, QPushButton, QSlider, QWidget 
from PyQt5                  import uic
from obj.QSliderLineEdit    import QSliderLineEdit
import os as OS

# 設計好的ui檔案路徑
qtCreatorFile = OS.getcwd() + "\\".join( ["","resource", "ui", "filterWidget.ui"] ) 
# 讀入用Qt Designer設計的GUI layout
FilterWidgetUI, _ = uic.loadUiType(qtCreatorFile)   

class FilterWidget(QWidget, FilterWidgetUI):
    _sortSignal = pyqtSignal(int, bool)

    SORT_BY_FLOOR   = 1
    SORT_BY_GP      = 2
    SORT_BY_BP      = 3
    ORDER_ASCENDING       = True
    ORDER_DESCENDING      = False
    def __init__(self) -> None:
        QWidget.__init__( self )
        FilterWidgetUI.__init__( self )
        self.setupUi( self )
        # -----------------------------------------
        self._resetButton:QPushButton       = self.findChild(QPushButton, name='resetButton')       # reset filter button
        self._groupbox:QGroupBox            = self.findChild(QGroupBox, name='filterGroupBox')

         # gp & bp slider
        self._GpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='gpSlider'),  self.findChild(QLineEdit, name='gpLineEdit'), "爆" )
        self._BpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='bpSlider'),  self.findChild(QLineEdit, name='bpLineEdit'), "X" )

        # sorter
        self._floorSortButton               = ToggleButton( self.findChild(QPushButton, name='floorSortButton'), self.findChild(QPushButton, name='floorAscButton') )
        self._gpSortButton                  = ToggleButton( self.findChild(QPushButton, name='gpSortButton'), self.findChild(QPushButton, name='gpAscButton') )
        self._bpSortButton                  = ToggleButton( self.findChild(QPushButton, name='bpSortButton'), self.findChild(QPushButton, name='bpAscButton') )
        self._floorSortButton.setToggle( True )
        self._floorSortButton.setOrder( self.ORDER_ASCENDING )

        self._nowToggle:ToggleButton        = self._floorSortButton
        # -----------------------------------------
        # initial event
        self._GpSliderEdit.initialEvent()
        self._BpSliderEdit.initialEvent()
        self._floorSortButton.button().clicked.connect( self._floorSortToggle )
        self._floorSortButton.orderButton().clicked.connect( self._orderToggle )
        self._gpSortButton.button().clicked.connect( self._gpSortToggle )
        self._gpSortButton.orderButton().clicked.connect( self._orderToggle )
        self._bpSortButton.button().clicked.connect( self._bpSortToggle )
        self._bpSortButton.orderButton().clicked.connect( self._orderToggle )

        

    def getResetButton( self ) -> QPushButton:
        return self._resetButton

    def getGpSliderEidt( self ) -> QSliderLineEdit:
        return self._GpSliderEdit
    
    def getBpSliderEidt( self ) -> QSliderLineEdit:
        return self._BpSliderEdit

    def getSortSignal( self ) -> pyqtSignal:
        return self._sortSignal

    def _orderToggle( self ):
        if( self._nowToggle == self._floorSortButton ):
            self._sortSignal.emit( self.SORT_BY_FLOOR, not( self._nowToggle.sortOrder() ) )
        if( self._nowToggle == self._gpSortButton ):
            self._sortSignal.emit( self.SORT_BY_GP, not( self._nowToggle.sortOrder() ) )
        if( self._nowToggle == self._bpSortButton ):
            self._sortSignal.emit( self.SORT_BY_BP, not( self._nowToggle.sortOrder() ) )

    def _floorSortToggle( self ):
        self._gpSortButton.setToggle( False )
        self._bpSortButton.setToggle( False )
        self._nowToggle = self._floorSortButton
        self._orderToggle()

    def _gpSortToggle( self ):
        self._floorSortButton.setToggle( False )
        self._bpSortButton.setToggle( False )
        self._nowToggle = self._gpSortButton
        self._orderToggle()

    def _bpSortToggle( self ):
        self._gpSortButton.setToggle( False )
        self._floorSortButton.setToggle( False )
        self._nowToggle = self._bpSortButton
        self._orderToggle()
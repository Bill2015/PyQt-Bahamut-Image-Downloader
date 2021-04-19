
from obj.ToggleButton import ToggleButton
from PyQt5.QtWidgets        import QGroupBox, QLineEdit, QPushButton, QSizePolicy, QSlider, QWidget 
from PyQt5                  import uic
from typing                 import Union
from obj.QSliderLineEdit    import QSliderLineEdit
import os as OS

# 設計好的ui檔案路徑
qtCreatorFile = OS.getcwd() + "\\".join( ["","resource", "ui", "filterWidget.ui"] ) 
# 讀入用Qt Designer設計的GUI layout
FilterWidgetUI, _ = uic.loadUiType(qtCreatorFile)   

class FilterWidget(QWidget, FilterWidgetUI):
    
    def __init__(self) -> None:
        QWidget.__init__( self )
        FilterWidgetUI.__init__( self )
        self.setupUi( self )
        # -----------------------------------------
        self._resetButton:QPushButton       = self.findChild(QPushButton, name='resetButton')       # reset filter button

         # gp & bp slider
        self._GpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='gpSlider'),  self.findChild(QLineEdit, name='gpLineEdit'), "爆" )
        self._BpSliderEdit: QSliderLineEdit  = QSliderLineEdit( self.findChild(QSlider, name='bpSlider'),  self.findChild(QLineEdit, name='bpLineEdit'), "X" )

        # sorter
        self._floorSortButton   = ToggleButton( 'floorSortButton' )
        self.layout().addChildWidget( self._floorSortButton )
        self.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.setMaximumWidth( 80 )
        self.setFixedHeight( 30 )

        """
        QPushButton#floorSortButton:hover
        {
            background-color:rgb(255, 119, 119);
            color:white;
        }
        QPushButton#floorSortButton{
            color:rgb(100, 100, 100);
            background-color:rgb(255, 157, 157);
            border-style: solid;
            border-radius: 8px;
        }

        """
        # -----------------------------------------
        # initial event
        self._GpSliderEdit.initialEvent()
        self._BpSliderEdit.initialEvent()

    def getResetButton( self ) -> QPushButton:
        return self._resetButton

    def getGpSliderEidt( self ) -> QSliderLineEdit:
        return self._GpSliderEdit
    
    def getBpSliderEidt( self ) -> QSliderLineEdit:
        return self._BpSliderEdit
        
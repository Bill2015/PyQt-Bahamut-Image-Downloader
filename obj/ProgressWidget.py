from PyQt5              import uic
from PyQt5.QtWidgets    import QLabel, QProgressBar, QPushButton, QSizePolicy, QSpacerItem, QWidget

import os as OS


class ProgressWidget(QWidget):
    PROGRESS_WIDGET_SHOW = 0
    PROGRESS_WIDGET_HIDE = 1
    PROGRESS_WIDGET_NORML = 2

    def __init__(self, uiPath) -> None:
        QWidget.__init__( self )
        uic.loadUi( uiPath + "downloadWidget.ui", self )
        # ----------------------------------------------------------
        self._downloadBtn: QPushButton      = self.findChild(QPushButton, name='downloadButton')
        self._label: QLabel                 = self.findChild(QLabel, name='progressLabel')
        self._progress: QProgressBar        = self.findChild(QProgressBar, name='progressBar')
        self._hSpacer: QSpacerItem          = QSpacerItem(0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        self._widget: QWidget               = self.findChild(QWidget, name='downloadWidget')
        self._widget.layout().insertItem( 1, self._hSpacer )

        self.hide()

    
    def getDownloadButton( self ) -> QPushButton:
        return self._downloadBtn

    def setText( self, text: str):
        """ set the showing text """
        self._label.setText( text )

    def setValue( self, value:int ):
        """ set the value of progress bar """
        self._progress.setValue( value )

    def setTextAndVal( self, text: str, value:int ):
        """ set the value of progress bar """
        self._label.setText( text )
        self._progress.setValue( value )


    def setMaxValue( self, value:int ):
        """ set the maximum of progress bar """
        self._progress.setMaximum( value )

    def setMinValue( self, value:int ):
        """ set the minimum of progress bar """
        self._progress.setMinimum( value )

    def hide( self ):
        """ hide progress widget """
        self._label.hide()
        self._progress.hide()
        self._hSpacer.changeSize( 0, 20, QSizePolicy.Expanding, QSizePolicy.Minimum )
    
    def show( self ):
        """ show progress widget """
        self._label.show()
        self._progress.show()
        self._hSpacer.changeSize( 0, 20, QSizePolicy.Minimum, QSizePolicy.Minimum )

    def getProgressbar( self ) -> QProgressBar:
        """ get the progress bar """
        return self._progress

    def getProgressLabel( self ) -> QLabel:
        """ get the progress label """
        return self._label
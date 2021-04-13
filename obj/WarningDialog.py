from PyQt5 import uic
from PyQt5.QtCore import QEvent, QPoint, QRect, Qt
from PyQt5.QtGui import QCursor, QMouseEvent
from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QPushButton

import os           as OS
import winsound     as WINSOUND

from PyQt5.uic.properties import QtCore
# 設計好的ui檔案路徑
qtCreatorFile = OS.getcwd() + "\\".join( ["","resource", "ui", "warningBox.ui"] ) 
# 讀入用Qt Designer設計的GUI layout
WaringDialogUI, _ = uic.loadUiType(qtCreatorFile)   

class WarningDialog( QDialog, WaringDialogUI ):
    def __init__( self, paraent ) -> None:
        QDialog.__init__( self, paraent )
        WaringDialogUI.__init__( self )
        self.setWindowFlags( self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute( Qt.WA_TranslucentBackground, True )
        self.setupUi( self )

        # ----------------------------------------------
        self._confirmButton:QPushButton         = self.findChild( QPushButton, name='okButton' )
        self._messageLabel:QPlainTextEdit       = self.findChild( QPlainTextEdit, name='messageLabel' )

        # ----------------------------------------------
        self._dialogSize:QRect                  = self.geometry()
        self._pressPos:QPoint                   = QPoint(0, 0)
        # ----------------------------------------------

        self._confirmButton.clicked.connect( self.close )
        self.installEventFilter( self )

    def show( self, message:str = "你好" ):
        self.setMessage( message )
        WINSOUND.PlaySound( 'SystemHand', WINSOUND.SND_ASYNC )
        QDialog.show( self )

    def setMessage( self, message:str ):
        """ set message """
        self._messageLabel.setPlainText( message )

    def eventFilter(self, source, event: QEvent):
        """Just make user can grapping windows"""
        if event.type() == QEvent.MouseButtonPress:
            if event.buttons() == Qt.LeftButton:
                mouseEvent: QMouseEvent = event
                self._pressPos = mouseEvent.pos()

        if event.type() == QEvent.MouseMove:
            if event.buttons() == Qt.LeftButton:
                cursor = QCursor()
                self.move( cursor.pos().x() - self._pressPos.x(), cursor.pos().y() - self._pressPos.y() )
    
        return QDialog.eventFilter(self, source, event)

        
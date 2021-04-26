from PyQt5 import uic
from PyQt5.QtCore import QEvent, QPoint, QRect, Qt
from PyQt5.QtGui import QCursor, QMouseEvent, QPixmap
from PyQt5.QtWidgets import QDialog, QLabel, QPlainTextEdit, QPushButton

import os           as OS
import winsound     as WINSOUND

from PyQt5.uic.properties import QtCore

class WarningDialog( QDialog ):
    DIALOG_WARNING  = 0
    DIALOG_INFO     = 1
    def __init__( self, paraent ) -> None:
        QDialog.__init__( self, paraent )
        uic.loadUi( OS.getcwd() + "\\".join( ["","resources", "ui", "warningBox.ui"] ), self ) 

        self.setWindowFlags( self.windowFlags() | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute( Qt.WA_TranslucentBackground, True )

        # ----------------------------------------------
        self._confirmButton:QPushButton         = self.findChild( QPushButton, name='okButton' )
        self._messageLabel:QPlainTextEdit       = self.findChild( QPlainTextEdit, name='messageLabel' )
        self._iconLabel:QLabel                  = self.findChild( QLabel, name='titleIconLabel' )
        self._titleLable:QLabel                 = self.findChild( QLabel, name='titleLabel' )

        # ----------------------------------------------
        self._pressPos:QPoint                   = QPoint(0, 0)
        # ----------------------------------------------

        # ----------------------------------------------
        path = OS.getcwd() + "\\".join( ["","resources", ""] ) 
        self._infoImg = QPixmap( path + 'info.png' )          # the info image Pixmap
        self._waringImg = QPixmap( path + 'waring.png' )      # the waring image Pixmap


        self._confirmButton.clicked.connect( self.close )
        self.installEventFilter( self )

    def show( self, message:str = "你好", title="警告", type=DIALOG_WARNING ):
        if( type == self.DIALOG_WARNING ):
            self._iconLabel.setPixmap( self._waringImg )
        else:
            self._iconLabel.setPixmap( self._infoImg )
            
        self._titleLable.setText( title )
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

        
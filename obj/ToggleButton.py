from typing             import overload
from PyQt5.QtCore       import QPropertyAnimation, QSize
from PyQt5.QtWidgets    import QGraphicsOpacityEffect, QPushButton

class ToggleButton():

    def __init__( self, button:QPushButton, ascButton:QPushButton ):
        self._button     = button
        self._orderButton  = ascButton
        # ---------------------------------------
        self._isEnable  = False
        self._ascending = False

        # ---------------------------------------
        self._button.clicked.connect( self._toggle )
        self._orderButton.clicked.connect( self._clickAscending )
        self._orderButton.setVisible( False )

        # ---------------------------------------
        self._opacity = QGraphicsOpacityEffect( self._button  )
        self._opacity.setOpacity( 0.5 ) 
        self._button.setAutoFillBackground( True )
        self._button.setGraphicsEffect( self._opacity )

        self._animation = QPropertyAnimation( self._button, b"size" )
        self._animation.finished.connect( self._orederButtonVisible )

    def _clickAscending( self ):
        self._ascending = not (self._ascending)
        self._orderButton.setText( "▲" if self._ascending else "▼" )
        self._orderButton.setToolTip( "遞增排序" if self._ascending else "遞減排序" )

    def _animate( self ):
        self._animation.setStartValue( self._button.size() )
        self._animation.setDuration( 250 ) 
        self._animation.setEndValue( QSize( self._button.width() - (30 if self._isEnable else -30), self._button.height())  )
        self._animation.start()
        if( self._isEnable == False ):
            self._orderButton.setVisible( self._isEnable )
    
    def _orederButtonVisible( self ):
        self._orderButton.setVisible( self._isEnable )
        
    def _toggle( self ):
        # insure have one is toggle all the time
        if( self._isEnable ):
            return
        self._isEnable = not( self._isEnable )
        self._update()
        self._animate()

    def setToggle( self, flag:bool ):
        """set the button to trigge"""
        preFlag = self._isEnable
        self._isEnable = flag
        self._update()

        # prevent Oscillate happen
        if( preFlag != flag ):
            self._animate()

    def setOrder( self, flag:bool ):
        self._ascending = flag
        self._orderButton.setText( "▲" if self._ascending else "▼" )
        self._orderButton.setToolTip( "遞增排序" if self._ascending else "遞減排序" )

    def _update( self ):
        self._opacity.setOpacity( 1.0 if self._isEnable else 0.35 ) 
        self._button.setProperty('toggle', self._isEnable )
        self._button.style().unpolish( self._button )
        self._button.style().polish( self._button )    
        self._button.update()
        self._orderButton.setProperty('toggle', self._isEnable )
        self._orderButton.style().unpolish( self._orderButton )
        self._orderButton.style().polish( self._orderButton )    
        self._orderButton.update() 

    def isToggle( self ) -> bool:
        """get the button is triggered """
        return self._isEnable

    def sortOrder( self ) -> bool:
        """get the order of the sort button """
        return self._ascending

    def orderButton( self ) -> QPushButton:
        """get order button """
        return self._orderButton

    def button( self ) -> QPushButton:
        """get text button """
        return self._button

      
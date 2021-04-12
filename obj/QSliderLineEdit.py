from PyQt5.QtWidgets import (QLineEdit, QSlider)
from PyQt5.QtGui import QIntValidator

class QSliderLineEdit():
    def __init__(self, slider:QSlider, lineEdit:QLineEdit, overText:str):
        self._slider: QSlider        = slider  
        self._lineEdit: QLineEdit    = lineEdit
        self._overText: str = overText
        self._lineEdit.setValidator( QIntValidator() )

        self._preVal = 0
        self._curVal = 0

    def _lineEditToSliderBinding( self ):
        try:
            value = min( int( self._lineEdit.text() ), 1000 )
            self._preVal = self._curVal
            self._curVal = value
            self._slider.setValue(  self._curVal  )
        except ValueError:
            self._curVal = self._preVal
        
    def _SliderToLineEidtBinding( self ):
        self._preVal = self._preVal
        self._curVal = self._slider.value()
        if self._curVal  >= 1000:
            self._lineEdit.setText( self._overText )
        elif self._curVal  == 0:
            self._lineEdit.setText( "-" )
        else:
            self._lineEdit.setText(  str( self._curVal ) )

    def initialEvent( self ):
        """initial slider & lineEdit binding event"""
        self._slider.valueChanged.connect( self._SliderToLineEidtBinding )
        self._lineEdit.textChanged.connect( self._lineEditToSliderBinding )

    def value( self ) -> int:
        """get now value of slider"""
        return self._slider.value()

    def setValue( self, val ):
        """setting slider value"""
        self._slider.setValue( val )
    
    def getSlider( self ) -> QSlider:
        return self._slider
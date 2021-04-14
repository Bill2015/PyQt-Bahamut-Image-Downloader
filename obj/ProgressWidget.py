
from PyQt5.QtWidgets import QLabel, QProgressBar


class ProgressWidget():
    PROGRESS_WIDGET_SHOW = 0
    PROGRESS_WIDGET_HIDE = 1
    PROGRESS_WIDGET_NORML = 2

    def __init__(self, label:QLabel, progress:QProgressBar) -> None:
        self._label         = label
        self._progress      = progress
    
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
        """ show progress widget """
        self._label.hide()
        self._progress.hide()
    
    def show( self ):
        """ show progress widget """
        self._label.show()
        self._progress.show()

    def getProgressbar( self ) -> QProgressBar:
        """ get the progress bar """
        return self._progress

    def getProgressLabel( self ) -> QLabel:
        """ get the progress label """
        return self._label
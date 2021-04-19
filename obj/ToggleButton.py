from PyQt5.QtWidgets import QPushButton

class ToggleButton(QPushButton):

    def __init__( self,  objName, parent=None ):
        super(ToggleButton, self).__init__(parent)
        self.setObjectName( objName )
        
        # ---------------------------------------
        self._isEnable = False


        # ---------------------------------------
        self.clicked.connect( self._toggle )

    def _toggle( self ):
        self._isEnable = not( self._isEnable )
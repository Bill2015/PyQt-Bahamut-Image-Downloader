
from PyQt5.QtWidgets import QFileDialog
from obj.ImageWidget import ImageWidget
from obj.NetImage import NetImage
from typing import List


import uuid as UUID

class DataManager():
    FLIE_NAME = "fileName"
    DATA_NAME = "data"
    def __init__(self) -> None:
        self.imgWidgetList:List[ImageWidget] = []

    def setImageList( self, imgWidgetList:List[ImageWidget] ):
        self.imgWidgetList  = imgWidgetList

    def getImageList( self ) -> List[ImageWidget]:
        return self.imgWidgetList

    def isImageEmpty( self ) -> int:
        for imgWidget in self.imgWidgetList:
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                return False
        return True

    def getDataDictinoary( self ) -> dict:
        """get the image data dictionary"""
        dataDict = {}

        serialNum = 1
        # writing data into zip file
        for imgWidget in self.imgWidgetList:
            netImage    = imgWidget.getImage()
            data        = netImage.getData()
            # it Must be need to is showing, and not remove by user either
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                if( data != None ):
                    tempSN = str(serialNum)
                    dataDict[ tempSN ] = {}
                    dataDict[ tempSN ][ DataManager.FLIE_NAME ] = tempSN + "-" + str(UUID.uuid4()) + netImage.getExtension()
                    dataDict[ tempSN ][ DataManager.DATA_NAME ] = data
                    serialNum += 1

        return dataDict


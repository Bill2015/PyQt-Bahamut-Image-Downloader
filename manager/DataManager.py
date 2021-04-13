
from obj.ImageWidget import ImageWidget
from typing import List

class DataManager():
    FLIE_NAME = "fileName"
    DATA_NAME = "data"
    def __init__( self ) -> None:
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



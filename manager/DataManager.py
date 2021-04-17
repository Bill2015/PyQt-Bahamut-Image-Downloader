
from obj.ImageWidget import ImageWidget
from typing import List

class DataManager():
    FLIE_NAME = "fileName"
    DATA_NAME = "data"
    def __init__( self ) -> None:
        self._imgWidgetList:List[ImageWidget] = []

    def clearSearchData( self ):
        for img in self._imgWidgetList:
            if( img.isLoadFailed() == False ):
                img.deleteLater()
                del img
        self._imgWidgetList.clear()

    def apendImageList( self, imgWidgetList:List[ImageWidget] ):
        self._imgWidgetList = self._imgWidgetList + imgWidgetList

    def setImageList( self, imgWidgetList:List[ImageWidget] ):
        self._imgWidgetList  = imgWidgetList

    def getImageList( self ) -> List[ImageWidget]:
        return self._imgWidgetList

    def isImageEmpty( self ) -> int:
        for imgWidget in self._imgWidgetList:
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                return False
        return True

    def countData( self ) -> int:
        count = 0
        for imgWidget in self._imgWidgetList:
            if( imgWidget.isVisible() == True and imgWidget.isRemoved() == False ):
                count += 1
        return count



from obj.ImageWidget import ImageWidget
from obj.NetImage import NetImage
from typing import List, Union


class DataManager():
    def __init__(self) -> None:
        self.imgWidgetList:List[ImageWidget] = []

    def setImageList( self, imgWidgetList:List[ImageWidget] ):
        self.imgWidgetList  = imgWidgetList

    def getImageList( self ) -> List[ImageWidget]:
        return self.imgWidgetList

    def showFilter( self, gp:int, bp:int ):
        for img in self.imgWidgetList:
            netImage = img.getImage()
            if netImage.getGP() < gp and netImage.getBP() >= bp:
                img.test()
                print("A")
            else:
                img.show()
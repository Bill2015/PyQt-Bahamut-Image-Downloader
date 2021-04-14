
class NetImageBuilder:
    def __init__( self ):
        self._imageData = None
        pass
    
    def setAuthor( self, id, name ):
        """set article author"""
        self.id = id
        self.name = name
        return self

    def setFloor( self, floor):
        """set article floor"""
        self.floor = floor
        return self

    def setGP( self, gp ):
        """set article GP"""
        self.gp = gp
        return self

    def setBP( self, bp ):
        """set article BP"""
        self.bp = bp
        return self

    def setImageUrl( self, url ):
        """set image url"""
        self.url = url
        return self


    def build( self ):
        """build the NetImage Object"""
        return NetImage( authorID=self.id, authorName=self.name, floor=self.floor, gp=self.gp, bp=self.bp, imageUrl=self.url )

class NetImage:
    _EXTENSION_LIST = [".jpg", ".JPG", ".PNG",".png", ".gif", ".GIF", ".jfif", ".JFIF", ".apng", ".APNG"]
    #=============================================================================================================
    def __init__( self, authorID:str, authorName:str, floor:int, gp:int, bp:int, imageUrl:str ):
        self._authorID:str   = authorID
        self._authorName:str = authorName
        self._floor:int      = floor
        self._gp:int         = gp 
        self._bp:int         = bp
        self._imageUrl:str   = imageUrl
        self._extension:str  = self._getExtensionOfUrl()

    def _getExtensionOfUrl( self ):
        """ get the type of image extension """
        for ext in NetImage._EXTENSION_LIST:
            if( self._imageUrl.endswith( ext ) ):
                return ext
        return ".txt"

    def print( self ):
        """print this article all of infomation"""
        print( "authorID:", self._authorID, "   authorName:", self._authorName, "  floor:", self._floor, "   GP:", self._gp, "   BP:", self._bp  )
        print(  self._imageUrl, "\n" )

    def toString( self ) -> str:
        """print this article all of infomation"""
        return "".join( ["authorID:", self._authorID, "   authorName:", self._authorName, "  floor:",  str(self._floor), "   GP:", str(self._gp), "   BP:", str(self._bp), "\n",  self._imageUrl, "\n\n"] ).encode("utf8")

    def getAuthorName(self) -> str:
        """get author name"""
        return self._authorName
    
    def getAuthorID(self) -> str:
        return self._authorID

    def getFloor(self) -> int:
        return self._floor
    
    def getGP(self) -> int:
        return self._gp

    def getBP(self) -> int:
        return self._bp

    def getImageUrl(self) -> str:
        return self._imageUrl

    def getExtension( self ) -> str:
        return self._extension



    @staticmethod
    def getBuilder():
        return NetImageBuilder()
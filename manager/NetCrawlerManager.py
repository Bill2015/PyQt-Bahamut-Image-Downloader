# Web Crewler
import urllib.request as URL_REQUEST
import urllib.error   as URL_ERROR
import math as MATH

from typing import List, Union
from bs4 import BeautifulSoup

from obj.NetImage import NetImage
from obj.ImageWidget import ImageWidget

class NetCrawlerManager:
    MAX_FLOOR_PER_PAGE = 20 # acconding to bahamut page, each page have 20 floor
    def __init__(self):
        self.netImageList: List[NetImage] = []
        self.netImageWidgetList: List[ImageWidget] = []
        pass

    def _getScore( self, element ):
        """let score(str) convert to integer"""
        scoreStr = element.select( "span" )[0].text
        if scoreStr ==  "爆" or scoreStr == "X":
            return 999
        elif scoreStr == "-":
            return 0
        else:
            return int(scoreStr)       

    def _getUrlData( self, url: str ):
        # example1 url: https://forum.gamer.com.tw/C.php?bsn=60076&snA=5993618&tnum=54
        # example2 url: https://forum.gamer.com.tw/C.php?page=2&bsn=60076&snA=5993618&tnum=54
        # example3 url: https://forum.gamer.com.tw/C.php?bsn=60076&snA=6243913&tnum=638&bPage=2
        # example4 url: https://forum.gamer.com.tw/C.php?bsn=60076&snA=6267967
        url        = url.replace("?", "&")
        strArray   = url.split( "&" )
        bsn = snA = maxFloor = ""

        for string in strArray:
            if string.find( "bsn" ) >= 0:
                bsn = string.replace("bsn=", "")
                
            elif string.find( "snA" ) >= 0:
                snA = string.replace("snA=", "")
            
            elif string.find( "tnum" ) >= 0:
                maxFloor = string.replace("tnum=", "")

        # check is url is vailded 
        if( bsn == "" or snA == "" or maxFloor == "" ):
            raise URL_ERROR.URLError()

        # get the max page of this article
        maxPage = MATH.ceil( int( maxFloor ) / self.MAX_FLOOR_PER_PAGE)

        print( "bsn:", bsn, "  snA:", snA, "  max floor:", maxFloor, "   max page:", maxPage )

        return [bsn, snA,  int( maxFloor ), maxPage]
        
    def getData( self, url: str, floor=[1, 999999], outputDebugTxt=False ) -> List[ImageWidget]:
        """ get the bahamut image"""

        # get the info of url
        [bsn, snA, maxFloor, maxPage] = self._getUrlData( url )
       
        self.bsnPre     = bsn
        self.snaPre     = snA
        self.maxFloor   = maxFloor

        # setting floor
        currentMinPage = MATH.ceil( floor[0] / self.MAX_FLOOR_PER_PAGE )
        currentMaxPage = min( MATH.ceil( floor[1] / self.MAX_FLOOR_PER_PAGE ), maxPage )
        nowPage = currentMinPage
        
        # get every page of this form
        for nowPage in range(currentMinPage, currentMaxPage + 1):  
            url = "".join( ["https://forum.gamer.com.tw/C.php?", "page=", str(nowPage), "&bsn=", bsn, "&snA=", snA] )

            htmlRequest = URL_REQUEST.Request( url, headers={'User-Agent': 'Mozilla/5.0'} )
            htmlRaw     = URL_REQUEST.urlopen( htmlRequest ).read()

            soupHTML = BeautifulSoup( htmlRaw, "html.parser")
            
    

            # get whole articles in this page
            for article in soupHTML.select( "section" ):

                # check that aritcle is removed or not
                if article.has_attr( "id" ) == False:
                    continue
                
                if len( article.select( ".c-disable" ) ) >= 1:
                    continue

                # check floor, break if lower or exceed
                nowFloor = int( article.select( ".floor" )[0][ "data-floor" ] )
                if nowFloor < floor[0] or nowFloor > floor[1]:
                    break

                # get this artcle infomation
                authorID        = article.select( ".userid" )[0].text
                authorName      = article.select( ".username" )[0].text
                articleGP       = self._getScore( article.select( ".postgp" )[0] )
                articleBP       = self._getScore( article.select( ".postbp" )[0] )

                # initial netImage builder
                netImageBuilder = NetImage.getBuilder()
                netImageBuilder.setAuthor( authorID, authorName )
                netImageBuilder.setFloor( nowFloor )
                netImageBuilder.setGP( articleGP )
                netImageBuilder.setBP( articleBP )
                                            
                # getting image url
                for imgURL in article.select( ".photoswipe-image" ):
                    netImageBuilder.setImageUrl( imgURL[ "href" ] )
                    netImage = netImageBuilder.build()

                    self.netImageList.append( netImage )                            # raw data net image
                    self.netImageWidgetList.append( ImageWidget( netImage ) )      # net image widget object


        # just verify web crawler are correct or not
        if( outputDebugTxt == True ):
            text_file = open("result.txt", "wb")
            for netImage in self.netImageList:
                text_file.write( netImage.toString() )
            text_file.close()


        return self.netImageWidgetList

        
        
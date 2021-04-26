
import json     as JSON
from math import floor
import os       as OS
from typing import List

class HistoryManager():
    
    class History():
        def __init__(self, title:str, bsn:str, snA:str, floors:list, date:str):
            self._title:str     = title
            self._bsn:str       = bsn
            self._snA:str       = snA
            self._floors:list   = floors
            self._date:str      = date
        
        def getTitle( self ) -> str:
            return self._title

        def getBsn( self ) -> str:
            return self._bsn
        
        def getSnA( self ) -> str:
            return self._snA
        
        def getFloors( self ) -> list:
            return self._floors

        def getDate( self ) -> str:
            return self._date

        def getDictData( self ) -> dict:
            tempDict = {}
            tempDict['title']   = self._title
            tempDict['bsn']     = self._bsn
            tempDict['snA']     = self._snA
            tempDict['floor']   = self._floors
            tempDict['date']    = self._date
            return tempDict

        def setFloors( self, floors:list ):
            self._floors = floors
        
        def setDate( self, date:str ):
            self._date = date

        def setTitle( self, title:str ):
            self._title = title

        def checkFloorInRange( self, floor:list ):
            floorRange = range( self._floors[0], self._floors[1] )
            if( ( floor[0] in floorRange ) or ( floor[1] in floorRange ) ):
                return True
            return False

    def __init__(self):
        self._historyData:List[HistoryManager.History] = list()
        pass

    def addHistory(self, title:str, bsn:str, snA:str, floors:list, date:str):
        # if data exist, replace it
        for history in self._historyData:
            if( history.getBsn() == bsn and history.getSnA() == snA ):
                history.setTitle( title )
                history.setFloors( floors )
                history.setDate( date )
                return
        # add data
        self._historyData.append( HistoryManager.History( title, bsn, snA, floors, date ) )
        
    def getHistory( self, bsn:str, snA:str ) -> History:
        for history in self._historyData:
            if( history.getBsn() == bsn and history.getSnA() == snA ):
                return history
        return None

    def getNewFloors( self, bsn:str, snA:str ) -> list():
        for history in self._historyData:
            if( history.getBsn() == bsn and history.getSnA() == snA ):
                return [history.getFloors()[1], 99999]
        return None
       
    def save( self ):
        if( len( self._historyData ) > 0 ):
            data = {}
            data['history'] = list()
            for history in self._historyData:
                data['history'].append( history.getDictData() )

            with open('history.json', 'w', encoding='utf8') as outfile:
                JSON.dump(data, outfile, ensure_ascii=False)

        

    def load( self ):
        filePath = "history.json"
        if OS.path.isfile( filePath ):
            with open('history.json', encoding='utf-8') as file:
                data = JSON.load( file )
                for history in data['history']:
                    # print('bsn: '       + history['bsn'])
                    # print('snA: '       + history['snA'])
                    # print('floor: '     + str(history['floor']))
                    # print('date:'       + history['date'])
                    # print('')
                    self._historyData.append( HistoryManager.History( history['title'], history['bsn'], history['snA'], list(history['floor']), history['date'] ) )
                
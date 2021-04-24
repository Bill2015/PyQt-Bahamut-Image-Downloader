
import json     as JSON
import os       as OS
from typing import List

class HistoryManager():
    
    class History():
        def __init__(self, bsn:str, snA:str, floors:list, date:str):
            self._bsn:str       = bsn
            self._snA:str       = snA
            self._floors:list   = floors
            self._date:str      = date

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
            tempDict['bsn']     = self._bsn
            tempDict['snA']     = self._snA
            tempDict['floor']   = self._floors
            tempDict['date']    = self._date
            return tempDict

    def __init__(self):
        self._historyData:List[HistoryManager.History] = list()
        pass

    def addHistory(self, bsn:str, snA:str, floors:list, date:str):
        self._historyData.append( HistoryManager.History( bsn, snA, floors, date ) )
        

    def save( self ):
        if( len( self._historyData ) > 0 ):
            data = {}
            data['history'] = list()
            for history in self._historyData:
                data['history'].append( history.getDictData() )

            with open('history.json', 'w') as outfile:
                JSON.dump(data, outfile)

        

    def load( self ):
        filePath = "history.json"
        if OS.path.isfile( filePath ):
            with open('history.json') as file:
                data = JSON.load( file )
                for history in data['history']:
                    # print('bsn: '       + history['bsn'])
                    # print('snA: '       + history['snA'])
                    # print('floor: '     + str(history['floor']))
                    # print('date:'       + history['date'])
                    # print('')
                    self._historyData.append( HistoryManager.History(history['bsn'], history['snA'], list(history['floor']), history['date'] ) )
                
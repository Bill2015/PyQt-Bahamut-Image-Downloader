import os           as OS
import pytz         as PYTZ
import traceback    as TRACE

from datetime       import datetime, timezone

class CrashLogManager( ):
    def __init__(self) -> None:
        self._timezone = PYTZ.timezone('Asia/Taipei')
        self._filePath = OS.getcwd() + "\\".join( ["", "crash-report",""] )
        

    def writeCrashLog( self, errorMessage:str ):
        """ when program crash, it will write into the txt file with exception and errors """
        TRACE.print_exc()

        utcTime = datetime.now( timezone.utc )
        formatTime = utcTime.astimezone( self._timezone ).strftime ("-%Y-%m-%d_%H-%M-%S")
        with open( self._filePath + "crash" + formatTime + ".txt" , "wb") as file:
            file.write( "=============== crash report =============== \n".encode("utf-8") )
            file.write( (errorMessage + "\n" + TRACE.format_exc()).encode("utf-8") )

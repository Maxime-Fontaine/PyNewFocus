

from PyNewFocus.Constants import *


class NFError(Exception):

    def __init__(self, ErrorCode=0, ErrorCause=None):
        Exception.__init__(self)
        self.ErrorCause = ErrorCause
        self.ErrorCode = ErrorCode
    
    
    def __str__(self):
        ErrorMsg = "\nPyNewFocus Error " +  str(self.ErrorCode) + " : "
        if self.ErrorCode == NF_ERROR_COMMUNICATION:
            ErrorMsg += "Communication with equipment " + str(self.ErrorCause) + " cannot be established"
        elif self.ErrorCode == NF_ERROR_BADCOMMAND:
            ErrorMsg += "Command '" + str(self.ErrorCause) + "' can't be interpreted by the equipment"
        elif self.ErrorCode == NF_ERROR_ARGUMENT_TYPE:
            ErrorMsg += "Wrong argument type for '" + str(self.ErrorCause) + "'"
        elif self.ErrorCode == NF_ERROR_ARGUMENT_VALUE:
            ErrorMsg += "Wrong argument value for '" + str(self.ErrorCause) + "'"
        else:
            ErrorMsg += "Error code not defined"
        
        return ErrorMsg

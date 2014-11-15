

from serial import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

#                               TUNABLE LASER CONSTANTS
# ----------------------------------------------------------------------------

NF_TLS_BAUDRATE = 115200
NF_TLS_NBITS = EIGHTBITS
NF_TLS_PARITY = PARITY_NONE
NF_TLS_STOPBIT = STOPBITS_ONE
NF_TLS_FLOWCONTROL = False

# MIN AND MAX WAVELENGTHS (nm)
NF_TLS_WLMIN = 1510
NF_TLS_WLMAX = 1580

# MIN AND MAX POWERS (dBm)
NF_TLS_PWMIN = 0
NF_TLS_PWMAX = 10


#                            ERROR NUMBER CONSTANTS
# ------------------------------------------------------------------------------
NF_ERROR_COMMUNICATION = -1
NF_ERROR_BADCOMMAND = -2
NF_ERROR_ARGUMENT_TYPE = -11
NF_ERROR_ARGUMENT_VALUE = -12

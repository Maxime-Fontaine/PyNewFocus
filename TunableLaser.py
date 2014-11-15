

class TunableLaser():
    '''
    This class allows to remote control the Tunable Laser Source (TLS) of New Focus
    '''

    def __init__(self, ComPort=0, Simulation=False):
        '''
        Constructor of AP1000 equipment.
        ComPort is the COM port number (integer) of the Laser.
        Simulation is a boolean to indicate to the program if it has to run in simulation mode or not
        '''
        self.ComPort = ComPort
        self.Simulation = Simulation
        if self.Simulation:
            print("Connected successfully to the New Focus Tunable Laser")
        else:
            self.Connexion = self.Open()

        self.Wavelength = 1550
        self.Power = 0
        self.UnitIndex = 0
        self.Units = ["dBm", "mW"]
        self.ValidUnits = ["dbm", "mw"]
        self.StatusIndex = 0
        self.Status = ["OFF", "ON"]
        self.UnLock()
        self.GetWavelength()


    def __str__(self):
        return "New Focus Tunable Laser on " + str(self.ComPort)


    def Open(self):
        '''
        Open connexion to New Focus TLS equipment.
        This method is called by the constructor of TunableLaser class
        '''
        import serial, sys
        
        try:
            Connexion = serial.Serial(self.ComPort, NF_TLS_BAUDRATE, NF_TLS_NBITS, NF_TLS_PARITY, \
                    NF_TLS_STOPBIT, NF_TLS_FLOWCONTROL)
        except:
            print("Cannot open connexion with New Focus Tunable Laser")
            sys.exit()
        else:
            print("Connected successfully to the New Focus Tunable Laser")
            return Connexion


    def Close(self, Error=False):
        '''
        Close connexion to New Focus TLS equipment
        '''
        if not self.Simulation:
            if not Error:
                self.Lock()
            self.Connexion.close()


    def Send(self, Command):
        '''
        Send a string Command to the TLS equipment (ending character must be \'\n')
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE, NF_ERROR_COMMUNICATION
        from PyNewFocus.Errors import NFError
        
        if not isinstance(Command, str):
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "Command")
        
        if not self.Simulation:
            try:
                self.Connexion.write(Command.encode('utf-8'))
            except:
                self.Close(True)
                raise NFError(NF_ERROR_COMMUNICATION, "Command")


    def Receive(self, ByteNumber=1024):
        '''
        Receive a string from the TLS equipment
        ByteNumber is an integer (default to 1024) representing the number of bytes to receive
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE, NF_ERROR_BADCOMMAND
        from PyNewFocus.Errors import NFError
        
        if not isinstance(ByteNumber, int):
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "ByteNumber")
        
        if not self.Simulation:
            try:
                data = self.Connexion.readline()
            except:
                self.Close(True)
                raise NFError(NF_ERROR_BADCOMMAND, "Last command")
            else:
                return data.decode('utf-8')[1:]


    def ConvertToLog(self, LinearPower):
        '''
        Return a converted logaritmic power (dBm) from a linear one (mW)
        LinearPower is the mW power to convert
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE
        from PyNewFocus.Errors import NFError
        from math import log10 as log
        
        try:
            LinearPower = float(LinearPower)
        except:
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "LinearPower")
        
        return 10*log(LinearPower)


    def ConvertToLin(self, LogPower):
        '''
        Return a converted linear power (mW) from a logaritmic one (dBm)
        LogPower is the dBm power to convert
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE
        from PyNewFocus.Errors import NFError
        
        try:
            LogPower = float(LogPower)
        except:
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "LogPower")
        
        return 10**(LogPower / 10)


    def SetWavelength(self, Wavelength):
        '''
        Set wavelength of the New Focus TLS equipment
        Wavelength is expressed in nm
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE, NF_TLS_WLMIN, NF_TLS_WLMAX
        from PyNewFocus.Errors import NFError
        
        try :
            Wavelength = float(Wavelength)
        except:
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "Wavelength")
        
        if Wavelength < NF_TLS_WLMIN:
            Wavelength = NF_TLS_WLMIN
        if Wavelength > NF_TLS_WLMAX:
            Wavelength = NF_TLS_WLMAX
        
        if not self.Simulation:
            Command = "WAV " + ("%4.3f" % Wavelength).zfill(8) + "\n"
            self.Send(Command)
        
        self.Wavelength = Wavelength


    def GetWavelength(self):
        '''
        Get wavelength of the New Focus TLS equipment
        The return wavelength is expressed in nm
        '''
        if not self.Simulation:
            Command = "WAV?\n"
            self.Send(Command)
            self.Wavelength = float(self.Receive()[:-1])
        
        return self.Wavelength


    def SetPower(self, Power):
        '''
        Set output power of the New Focus TLS equipment
        Power is expressed in the unit defined by the GetUnit() method
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE, NF_TLS_PWMIN, NF_TLS_PWMAX
        from PyNewFocus.Errors import NFError
        
        try :
            Power = float(Power)
        except:
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "Power")
        
        if Power < NF_TLS_PWMIN:
            Power = NF_TLS_PWMIN
        if Power > NF_TLS_PWMAX:
            Power = NF_TLS_PWMAX
        
        if not self.Simulation:
            Command = "POW " + ("%2.2f" % Power).zfill(5) + self.Units[self.UnitIndex].upper() + "\n"
            self.Send(Command)
        
        if self.UnitIndex == 1:
            Power = self.ConvertToLog(Power)
        self.Power = Power


    def GetPower(self):
        '''
        Get output power of the New Focus TLS equipment
        The return power is expressed in the unit defined by the GetUnit() method
        '''
        if not self.Simulation:
            Command = "POW?\n"
            self.Send(Command)
            self.Power = float(self.Receive()[:-1])
        
        if self.UnitIndex == 1:
            self.Power = self.ConvertToLin(self.Power)
        
        return self.Power


    def SetUnit(self, Unit):
        '''
        Set the power unit of the New Focus TLS equipment
        Unit is a string which could be "dBm" for logaritmic or "mW" for linear power
        '''
        from PyNewFocus.Constants import NF_ERROR_ARGUMENT_TYPE, NF_ERROR_ARGUMENT_VALUE
        from PyNewFocus.Errors import NFError
        
        if not isinstance(Unit, str):
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_TYPE, "Unit")
        if not Unit.lower() in self.ValidUnits:
            self.Close(True)
            raise NFError(NF_ERROR_ARGUMENT_VALUE, "Unit")
        else:
            self.UnitIndex = self.ValidUnits.index(Unit.lower())
        
        if not self.Simulation:
            Command = "POW:UNIT " + Unit.upper() + "\n"
            self.Send(Command)


    def GetUnit(self):
        '''
        Get power unit of the New Focus TLS equipment
        The return unit is a string
        '''
        if not self.Simulation:
            Command = "POW:UNIT?\n"
            self.Send(Command)
            self.UnitIndex = int(self.Receive()[:-1])
        
        return self.Units[self.UnitIndex]


    def On(self):
        '''
        Activate the output power of the New Focus TLS equipment
        '''
        self.UnLock()
        if not self.Simulation:
            Command = "OUTP 1\n"
            self.Send(Command)
        
        self.StatusIndex = 1


    def Off(self):
        '''
        Shut down the output power of the New Focus TLS equipment
        '''
        if not self.Simulation:
            Command = "OUTP 0\n"
            self.Send(Command)
        
        self.StatusIndex = 0


    def GetStatus(self):
        '''
        Return the status ("ON" or "OFF") of the New Focus TLS equipment
        '''
        if not self.Simulation:
            Command = "OUTP?\n"
            self.Send(Command)
            self.StatusIndex = int(self.Receive()[:-1])
        
        return self.Status[self.StatusIndex]


    def Lock(self):
        '''
        Lock the New Focus TLS equipment
        This method is called by the 'Close' method of the TunableLaser class
        '''
        if not self.Simulation:
            Command = "LOCK 1\n"
            self.Send(Command)


    def UnLock(self):
        '''
        Unlock the New Focus TLS equipment
        This method is called by the constructor of TunableLaser class
        '''
        if not self.Simulation:
            Command = "LOCK 0\n"
            self.Send(Command)

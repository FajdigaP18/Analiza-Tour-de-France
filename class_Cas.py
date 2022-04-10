
import json

class InvalidTimeException(Exception):
    def __init__(self, niz):
        super().__init__("'" + niz + "' ni veljaven cas!")


class Cas:
    def __init__(self,ure = None, minute = None, sekunde = None,):
        if ure == None:
            ure = 0
        if minute == None:
            minute = 0
        if sekunde == None:
            sekunde = 0
        try:
            if ure < 0 or minute > 59 or minute < 0 or sekunde > 59 or sekunde < 0:
                raise Exception()
        except Exception:
            raise InvalidTimeException("{}:{}:{}".format(ure, minute, sekunde))
        self.ure = ure
        self.minute = minute
        self.sekunde = sekunde
        
    def __str__(self):
        return "{}:{}:{}".format( self.ure, self.minute, self.sekunde)
    
    def __repr__(self):
        return "Cas({}, {}, {})".format(self.ure, self.minute, self.sekunde)
    
    def __lt__(self, other):
        if self.ure < other.ure:
            return True
        elif self.ure == other.ure:
            if self.minute < other.minute:
                return True
            elif self.minute == other.minute:
                if self.sekunde < other.sekunde:
                    return True
        else: return False
    
    def __add__(self, other):
        ure = self.ure + other.ure
        minute = self.minute + other.minute
        sekunde = self.sekunde + other.sekunde
        if sekunde > 60:
            sekunde -= 60
            minute += 1
        if minute > 59:
            minute -= 60
            ure += 1
        return Cas(ure, minute, sekunde) 
    
    def __sub__(self, other): # od najvecjega odstejemo najmanj
        niz_1 = '{}:{}:{}'.format(self.ure, self.minute, self.sekunde)
        niz_2 = '{}:{}:{}'.format(other.ure, other.minute, other.sekunde)
        if self < other:
            raise Exception("Prvi cas je manjsi od drugega! Ne moremo imeti v negativen cas!!")
        else:
            ure = self.ure - other.ure
            if self.sekunde < other.sekunde:
                sekunde = 60 - abs(self.sekunde - other.sekunde)
                other.minute += 1
            if self.sekunde >= other.sekunde:
                sekunde = self.sekunde - other.sekunde
            if self.minute < other.minute:
                minute = 60 - abs(self.minute - other.minute)
                ure -= 1
            if self.minute >= other.minute:
                minute = self.minute - other.minute
            return Cas(ure, minute, sekunde)



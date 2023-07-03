

class Functions:
    def __init__(self, name):
        self.name = name
        
    @staticmethod
    def DisplayOff(hour: int) -> bool:
        return hour >= 21 or hour <= 9


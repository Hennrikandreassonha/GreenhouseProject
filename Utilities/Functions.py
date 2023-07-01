

class Functions:
    def __init__(self, name):
        self.name = name
        
    @staticmethod
    def HourIsPastNine(hour: int) -> bool:
        return hour >= 21


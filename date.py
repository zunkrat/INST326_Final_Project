PAYSTUB = {
    "11/10/23": "210",
    "10/11/23": "310", 
    "09/13/21": "500"
}

class example:
    
    def __init__(self, key):
        
        self.key = PAYSTUB.get(key)
     
    def __str__(self):
        
        return f"This is how much money you inputed on this day: ${self.key}"
        
        
e = example("09/13/21")
print(e)


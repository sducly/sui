
class State:
    """Objet contenant l'état de l'application"""
    def __init__(self):
        self.vision = None 
        self.audio = None  
        self.message = None 
    
    def update_vision(self, value):
        self.vision = value
        print(f"👀 Vision mise à jour : {self.vision}")

    def update_audio(self, value):
        self.audio = value
        print(f"🎙️ Audio mis à jour : {self.audio}")

    def update_message(self, value):
        self.message = value
        print(f"💬 Message mis à jour : {self.sui_message}")
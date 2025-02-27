import key_api
import time


class TLBBHelper:
    def __init__(self):
        self.game_helper = key_api.GameHelper()
        

def printMousePosition():
    for i in range(10):
        mouse_position = key_api.pyautogui.position()
        print(mouse_position)
        time.sleep(1)
    
    
    
    
    
    
    



if __name__ == "__main__":
    printMousePosition()

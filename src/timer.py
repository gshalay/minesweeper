import datetime 
from constants import *

class Timer():
    def __init__(self, label, parent):
        self.label = label
        self.parent = parent
        self.counter = TIME_INIT
        self.running = False
        self.count()
    
    def count(self):
        if self.running:
            # To manage the initial delay. 
            if self.counter == TIME_INIT:             
                display = TIME_INIT_STR
            else:
                date_str = datetime.datetime.fromtimestamp(self.counter).isoformat().split('T')[1]
                display = date_str 
  
            self.label['text'] = display   # Or label.config(text=display) 
  
            # label.after(arg1, arg2) delays by  
            # first argument given in milliseconds 
            # and then calls the function given as second argument. 
            # Generally like here we need to call the  
            # function in which it is present repeatedly. 
            # Delays by 1000ms=1 seconds and call count again. 
            self.label.after(1000, self.count)  
            self.counter += 1
            self.parent.update_idletasks()
  
    # start function of the stopwatch 
    def start(self):
        self.running = True
        self.count() 
    
    # Stop function of the stopwatch 
    def stop(self): 
        self.running = False
    
    # Reset function of the stopwatch 
    def reset(self):
        self.counter = TIME_INIT
    
        # If rest is pressed after pressing stop. 
        if self.running:          
            self.label['text'] = TIME_INIT_STR
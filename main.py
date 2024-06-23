from sumobot import Sumobot

class Sumo_App:
    #Arena_Color dark = True or light = False
    Arena_Color = True
    TRIG1 = 0
    ECHO1 = 1
    Distance = 0
    Disqualify_Count = 0
    App_Loop_Counter_limit = 0
    motor_speed = 0
    hold_time = 0
    
    def __init__(self):
        self.App = self
        self.Sumo = Sumobot(self)
        print("Starting Sumo_App")
        self.test_loop_count = 5
        self.Distance = 35
        self.Disqualify_Count = 5
        self.hold_time = 1
        self.App_Loop_Counter_limit = 100
        self.motor_speed = 30
        
    
    def application_loop(self):
        #self.test_loop()
        #self.Sumo.test_ir(self.test_loop_count)
        self.Sumo.Start_Match()
        
    def test_loop(self):
        self.Sumo.test_motors(self.test_loop_count)
        self.Sumo.test_ultrasonic(self.test_loop_count)
        self.Sumo.test_ir(self.test_loop_count)
        self.Sumo.test_WS2812_LED(self.test_loop_count)
        
mybot = Sumo_App()        
mybot.application_loop()

    


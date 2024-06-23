import utime as Sumo_utime
import machine as Sumo_machine
import PWM_Motor_Control_test as Sumo_Motor_Control
import hcsr04_ultrasonic as Sumo_Ultrasonic
import tcrt_ir as Sumo_IR
import LED_Status as Sumo_LED

class Sumobot:
    def __init__(self, Parent):
        self.App = Parent
        self.Machine = Sumo_machine
        self.Utime = Sumo_utime
        self.PWM_Frequency = 20000
        self.Echo_Timeout_us = 10000
        self.IR_Surface = self.App.Arena_Color
        self.LED_Pin = 16
        self.spi_bus = 1
        self.led_count = 1
        self.intensity = 1
        self.Charge_Distance = self.App.Distance
        self.Loops_Disqualify = 0
        self.Sumo_Loop_counter = 0
        self.LR_Toggle = True
        self.Sumo_Standby = True
        
        self.Ultrasonic = Sumo_Ultrasonic.HCSR04(self)
        self.Motors = Sumo_Motor_Control.Motor_Controller(self)
        self.IR = Sumo_IR.TCRT5000(self)
        self.WS2812_LED = Sumo_LED.WS2812_RGB_LED(self)
        self.Loops_Disqualify = 0
        
    def test_motors(self, test_loops):
        self.Motors.change_speed(20)
        self.Motors.self_test(test_loops)
        self.Motors.change_speed(100)
        self.Motors.self_test(test_loops)
    
    def test_ultrasonic(self, test_loops):
        self.Ultrasonic.self_test(test_loops, 1)
    
    def test_ir(self, test_loops):
        self.IR.self_test(test_loops)
        
    def test_WS2812_LED(self, test_loops):
        self.WS2812_LED.self_test(test_loops)
    
    def Start_Match(self):
        while self.Sumo_Standby:
            print("waiting on standby")
            self.Standby()
            self.Utime.sleep(1)
        self.Find_Opponent()
    
    def Check_End_Match(self):
        if self.Loops_Disqualify < self.App.Disqualify_Count and self.Sumo_Loop_counter < self.App.App_Loop_Counter_limit:
            return True
        else:
            print("Match Ending")
            return False
            
    def Sumo_Distance_cm(self):
        measurement_1 = self.Ultrasonic.distance_cm()
        self.Utime.sleep(1)
        measurement_2 = self.Ultrasonic.distance_cm()
        self.Utime.sleep(1)
        measurement_3 = self.Ultrasonic.distance_cm()
        self.Utime.sleep(.5)
        print("Distance cm: " , measurement_1, ", ", measurement_2, ", ",measurement_3)
        Average = (measurement_1 + measurement_2 + measurement_3)/3
        print("Distance cm: " , Average)
        return Average
        
    def Standby(self):
        if self.Sumo_Distance_cm() > self.App.Distance:
            self.Sumo_Standby = True
            self.Motors.deinit()
        else:
            self.Sumo_Standby = False
            
        
    def Find_Opponent(self):
        print("Finding Opponent")
        self.Motors.change_speed(50)
        print("Adjusted Speed")
        while self.Check_End_Match():
            self.Sumo_Loop_counter = self.Sumo_Loop_counter + 1
            ("Checking if out or in bounds")
            if self.IR.ir_sensor_read() == self.IR_Surface:
                print("ready to Sumo!")
                self.Loops_Disqualify = 0
                
                if self.Sumo_Distance_cm() <= self.Charge_Distance:
                    self.Push_Opponent()
                else :
                    self.Move_Ahead()
                    
                if self.Sumo_Distance_cm() <= self.Charge_Distance:
                    self.Push_Opponent()
                else :
                    self.Move_Back()

                if self.Sumo_Distance_cm() <= self.Charge_Distance:
                    self.Push_Opponent()
                else :
                    self.Spin_Round()
                
            else :
                self.Look_for_Surface()
                
        self.Motors.deinit()
        
    def Push_Opponent(self):
        print("Bonzai!")
        self.Motors.charge(50)
        if self.IR.ir_sensor_read() == self.IR_Surface:
            print("Bonzai!!")
            self.Motors.charge(70)
        else:
            self.Look_for_Surface()
            
        while self.IR.ir_sensor_read() == self.IR_Surface:
            print("Bonzai!!!")
            self.Motors.charge(100)
        self.Look_for_Surface()
        
    def Spin_Round(self):
        if self.LR_Toggle:
            self.Motors.SpinL()
            self.Utime.sleep(self.App.hold_time)
            self.LR_Toggle = False
        else:
            self.Motors.SpinR()
            self.Utime.sleep(self.App.hold_time)
            self.LR_Toggle = True
        
    def Move_Ahead(self):
        print("Moving Ahead")
        self.Motors.forward()
        self.Utime.sleep(self.App.hold_time)
        self.Motors.left()
        self.Utime.sleep(self.App.hold_time)

    def Move_Back(self):
        print("Moving Back")
        self.Motors.backward()
        self.Utime.sleep(self.App.hold_time)
        self.Motors.left()
        self.Utime.sleep(self.App.hold_time)
       
    def Look_for_Surface(self):
        print("Looking for Sumo Mat")
        self.Motors.backward()
        self.Utime.sleep(self.App.hold_time)
        
        while self.IR.ir_sensor_read() != self.IR_Surface and self.Sumo_Loop_counter < self.App.App_Loop_Counter_limit :
            self.Sumo_Loop_counter = self.Sumo_Loop_counter + 1
            self.Spin_Round()
            self.Loops_Disqualify = self.Loops_Disqualify + 1
            self.Move_Ahead()


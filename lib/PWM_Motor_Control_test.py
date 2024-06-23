#PWM Motor Control app 5/22/2024
#Based on https://www.donskytech.com/raspberry-pi-pico-motor-control-using-the-drv8833/
class Motor_Controller:
    MAX_DUTY_CYCLE = 65535
    MIN_DUTY_CYCLE = 0

    def __init__(self, Parent):
        #Pico Setup
        self.Machine = Parent.Machine
        self.Utime = Parent.Utime
        self.frequency = Parent.PWM_Frequency
        self.IN1 = self.Machine.PWM(self.Machine.Pin(2, mode=self.Machine.Pin.OUT)) #PWM A1
        self.IN2 = self.Machine.PWM(self.Machine.Pin(3, mode=self.Machine.Pin.OUT)) #PWM B1
        self.IN3 = self.Machine.PWM(self.Machine.Pin(4, mode=self.Machine.Pin.OUT)) #PWM A2
        self.IN4 = self.Machine.PWM(self.Machine.Pin(5, mode=self.Machine.Pin.OUT)) #PWM B2
        # set PWM frequency
        self.IN1.freq(self.frequency)
        self.IN2.freq(self.frequency)
        self.IN3.freq(self.frequency)
        self.IN4.freq(self.frequency)
        #Class Properties
        self.current_speed = Motor_Controller.MAX_DUTY_CYCLE       
        self.configured = 1
        self.loop_counter = 1

    ''' Map duty cycle values from 0-100 to duty cycle 40000-65535 '''
    def __map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

    ''' new_speed is a value from 0% - 100% '''
    def change_speed(self, new_speed):
        if new_speed < 20:
            new_speed = 20
        print("Changing speed ", self.current_speed, "To -> ", new_speed)
        new_duty_cycle = self.__map_range(new_speed, 0, 100, 40000, 65535)
        
        self.current_speed = new_duty_cycle
        self.configured = 1

    def deinit(self):
        """deinit PWM Pins"""
        print("Deinitializing PWM Pins")
        self.stop()
        self.Utime.sleep(0.1)
        self.IN1.deinit()
        self.IN2.deinit()
        self.IN3.deinit()
        self.IN4.deinit()
        
    #Class methods
    def Movement(self, A0,A1,B0,B1):
        if A0 == 0:
            self.IN1.duty_u16(Motor_Controller.MIN_DUTY_CYCLE) #low()
        else:
            self.IN1.duty_u16(self.current_speed) #high()
            
        if A1 == 0:
            self.IN2.duty_u16(Motor_Controller.MIN_DUTY_CYCLE)
        else:
            self.IN2.duty_u16(self.current_speed)
        if B0 == 0:
            self.IN3.duty_u16(Motor_Controller.MIN_DUTY_CYCLE)
        else:
            self.IN3.duty_u16(self.current_speed)
            
        if B1 == 0:
            self.IN4.duty_u16(Motor_Controller.MIN_DUTY_CYCLE)
        else:
            self.IN4.duty_u16(self.current_speed)

    def forward(self):
        self.Movement(0,1,0,1)

    def backward(self):
        self.Movement(1,0,1,0)

    def SpinR(self):
        self.Movement(1, 0, 0, 1)
        
    def SpinL(self):
        self.Movement(0, 1, 1, 0)
        
    def stop(self):
        self.Movement(0, 0, 0, 0)

    def left(self):
        self.Movement(0, 1, 0, 0)
        
    def right(self):
        self.Movement(0, 0, 1, 0)
        
    def charge(self, Charge_Speed):
        self.change_speed(Charge_Speed)
        self.forward()
        self.Utime.sleep(.1)
        
    def self_test(self, test_loops):
        while self.configured == 1:
            if self.loop_counter < test_loops:
                #run progran
                self.change_speed(30)
                self.forward()
                self.Utime.sleep(.5)
                self.backward()
                self.Utime.sleep(.5)
                self.SpinR()
                self.Utime.sleep(.5)
                self.SpinL()
                self.Utime.sleep(.5)
                self.left()
                self.Utime.sleep(.5)
                self.right()
                self.Utime.sleep(.5)
                self.charge(50)
                self.Utime.sleep(.5)
                self.stop()
                self.loop_counter = self.loop_counter + 1
            else:
                #Exit program
                self.configured = 0
                self.loop_counter = 1
                self.deinit()
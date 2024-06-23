#IR Sensor floor color detection

class TCRT5000():
    def __init__(self, Parent):
        self.Parent = Parent
        self.IR_Pin = self.Parent.Machine.Pin(6, mode=self.Parent.Machine.Pin.IN, pull=None)
        self.loop_counter = 0
        
    def ir_sensor_read(self):
        return self.IR_Pin.value()
    
    def self_test(self, test_loops):
        while self.loop_counter < test_loops:
            if self.ir_sensor_read() == self.Parent.IR_Surface:
                print("sensor detects inside of arena")
            else:
                print("semsor detects outside of arena")
            self.Parent.Utime.sleep(1)
            self.loop_counter = self.loop_counter + 1

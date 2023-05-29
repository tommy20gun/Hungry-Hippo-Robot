#code guide provided by https://realpython.com/python-sockets/
from Ball import Ball
from Cart import Cart
import math
from simple_pid import PID
import time

def getdutycycledata(ball,cart, pid):
    #the data string
    data = ""

    #First the cart is checked (interally) and also set a dutycycle for opposite spinning motors to turn the cart
    dutycycle,negdutycycle = rotate(ball, cart)
    
    #the cart is not facing the bal
    if dutycycle != None:
        #I hardcoded the motor 2 to have -30 (0xD0)
        data = f"M1{dutycycle}\r\nM2{negdutycycle}\r\n"
    #this is True if the cart does not need to rotate anymore or IS facing the ball. It begins to drive to the cart.
    if dutycycle == None:
        dutycycle = proportionaldrive(ball,cart,pid)
        if dutycycle != None:
            data = f"M1{dutycycle}\r\nM2{dutycycle}\r\n"
    
    #data is a string right now
    return data
    

#returns a list for M1 duty and M2 duty
def rotate(balls, cart):
    #check if there are actually balls and a cart
    if balls and cart:
        #since balls is a list, we take drive the cart to the first ball that it "sees"
        ballx = balls[0].x
        bally = balls[0].y

        #find the angle that the ball is from the cart
        angle_rad = math.atan2(ballx-cart.x, -(bally-cart.y))
        angle_deg = math.degrees(angle_rad)
        #i dont want to deal with negative degrees
        if angle_deg < 0:
            angle_deg = angle_deg + 360

        #rotate clockwise until the angle is approximately correct
        #dutycycle to be changed upon testing
        dutycycle = []
        
        #gives the range of rotation 20 degrees. If the cart is within +- 3 degrees of the desired angle, it will stop rotating.
        if not (abs(angle_deg - cart.angle) <= 10 or abs(angle_deg - cart.angle + 360) <= 10 or abs(angle_deg - cart.angle - 360) <= 10):
            dutycycle.append(30)
            dutycycle.append("D0")
            return dutycycle[0],dutycycle[1]
        else:
            return None, None
    return None, None

def proportionaldrive(balls, cart, pid):

    if balls and cart:
        #since balls is a list, we take drive the cart to the first ball that it "sees"
        ballx = balls[0].x
        bally = balls[0].y

        #taking the distance so that we can apply a proportional controller to set its duty cycle
        distance = (math.hypot(ballx-cart.x,bally-cart.y))
        
        #apply pid controller and also int cast the output
        #dutycyclepercent  = int(pid(-distance))
        kp = 0.2
        dutycyclepercent  = int((kp*distance))

        if dutycyclepercent > 128:
            dutycyclepercent = 0x7f

        #reutrns the hexadecimal string that eliminates "0x" prefix from the string
        return hex(dutycyclepercent)[2:]
    
    #return none if there is no there is no ball or cart
    return None

if __name__ == "__main__":
    #initial conditions, will be arguments later
    ball = []
    ball.append(Ball('yellow',0, 100))
    ball.append(Ball('green', 0, 800))
    cart = Cart(0, 0, 900)
    pid = PID(.5,.1,.01, setpoint= 1)

    while True:
        time.sleep(.5)
        print(getdutycycledata(ball,cart, pid))
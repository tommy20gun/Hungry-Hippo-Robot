from Ball import Ball
from Cart import Cart
import math

def sendserialdata():
    #the data string
    data = ""

    #initial conditions, will be arguments later
    ball = []
    ball.append(Ball('yellow',50,400))
    ball.append(Ball('green', 50, 800))
    cart = Cart(90, 5, 400)
    
    
    #First the cart is checked (interally) and also set a dutycycle for opposite spinning motors to turn the cart
    dutycycle,negdutycycle = rotate(ball, cart)
    
    #the cart is not facing the bal
    if dutycycle != None:
        #I hardcoded the motor 2 to have -30 (0xD0)
        data = f"M1{dutycycle}\r\nM2{negdutycycle}\r\n"
    #this is TRue if the cart does not need to rotate anymore or IS facing the ball. It begins to drive to the cart.
    if dutycycle == None:
        dutycycle = proportionaldrive(ball,cart,0.3)
        data = f"M1{dutycycle}\r\nM2{dutycycle}\r\n"
    
    #data is a string right now
    return data
    

#returns a list for M1 duty and M2 duty
def rotate(balls, cart):
    
    #since balls is a list, we take drive the cart to the first ball that it "sees"
    ballx = balls[0].x
    bally = balls[0].y

    #find the angle that the ball is from the cart
    angle_rad = math.atan2(ballx-cart.x, bally-cart.y)
    angle_deg = math.degrees(angle_rad)

    #rotate clockwise until the angle is approximately correct
    #dutycycle to be changed upon testing
    dutycycle = []
    if cart.angle != angle_deg:
        dutycycle.append(30)
        dutycycle.append("D0")
        return dutycycle[0],dutycycle[1]
    else:
        return None, None

def proportionaldrive(balls, cart, kp):

    #since balls is a list, we take drive the cart to the first ball that it "sees"
    ballx = balls[0].x
    bally = balls[0].y

    #taking the distance so that we can apply a proportional controller to set its duty cycle
    distance = (math.hypot(ballx-cart.x,bally-cart.y))
    
    
    dutycyclepercent  = abs(kp*distance) 
    if dutycyclepercent > 128:
        dutycyclepercent = 0x7f
    
    return int(dutycyclepercent)

if __name__ == "__main__":

    sendserialdata()

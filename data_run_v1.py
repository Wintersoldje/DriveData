import pygame
pygame.init()
pygame.joystick.init()

joystick = pygame.joystick.Joystick(0)

joystick.init()

joy_name = joystick.get_name()

print(joy_name)#<----detected and correct name
print(joystick.get_numaxes())#<---- this returns zero

while(True):
    pygame.event.pump()

    # raw value
    # angle = joystick.get_axis(0)
    # accelerator = joystick.get_axis(2)
    # brake = joystick.get_axis(3)
    # clutch = joystick.get_axis(1)

    # fix value
    angle = round(joystick.get_axis(0) * 100, 3)
    accelerator = round((1-joystick.get_axis(2))*50, 3)
    brake = round((1-joystick.get_axis(3))*50, 3)
    clutch = round((1-joystick.get_axis(1))*50, 3)
    num_hats = joystick.get_numhats()
    for i in range(num_hats):
        gear = joystick.get_hat(i)
        print("num_hats : {0}, hats {1}, value {2}".format(num_hats, i, gear))
    print("angle : {0}, accelerator : {1}, brake : {2}, clutch : {3}".format(angle, accelerator, brake, clutch))
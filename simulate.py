from Box2D import *
from Box2D.b2 import *
import pygame
from pygame.locals import *

def main():

    PPM = 20.0 # pixels per meter
    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT=640,480
    
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Bopper")
    clock = pygame.time.Clock()


    world = b2World()
    groundBody=world.CreateStaticBody(
            position=(0, -9),
            shapes=b2PolygonShape(box=(50,10)))

    # Start dynamic stuff

    mbody_height = 10
    x_pos = 5
    height = 8
    mbody = world.CreateDynamicBody(position=(x_pos,mbody_height/2))
    box = mbody.CreatePolygonFixture(box=(1,mbody_height/2), density=1, friction=0.3)

    bicep_length = 4
    bicep_width = 0.5
    bicep_body = world.CreateDynamicBody(position=(x_pos+bicep_length*0.8,height), angle=pi/2)
    bicep = bicep_body.CreatePolygonFixture(box=(bicep_width, bicep_length/2), density=1, friction=0.3)

    joint1 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep_body, localAnchorA=(0, height - mbody_height/2), localAnchorB=(0, bicep_length/2), lowerAngle = -pi, upperAngle = pi)
    print joint1.anchorA
    print joint1.anchorB
    print dir(joint1)
    print joint1.GetLocalAnchorA()
    print joint1.GetLocalAnchorB()


    forearm_length = 4
    forearm_width = 0.5
    forearm_body = world.CreateDynamicBody(position=(x_pos+bicep_length, height), angle=pi/2)
    forearm = forearm_body.CreatePolygonFixture(box=(forearm_width, forearm_length/2), density=1, friction=0.3)

    world.CreateRevoluteJoint(bodyA=bicep_body, bodyB=forearm_body, localAnchorA=(0, -bicep_length/2), localAnchorB=(0, forearm_length/2), lowerAngle=00.5*pi, upperAngle = 0.25 * pi)
    # 
    timeStep = 1.0 / FPS
    vel_iters = 6
    pos_iters = 2

    running = True
    while running:
        screen.fill((0,0,0,0))

        for body in (groundBody, mbody, bicep_body, forearm_body):
            for fixture in body.fixtures:
                shape = fixture.shape
                vertices = [(body.transform*v)*PPM for v in shape.vertices]
                vertices = [(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]

                if body == groundBody:
                    pygame.draw.polygon(screen, (0,255,0,255), vertices)
                else:
                    pygame.draw.polygon(screen, (255,255,255,255), vertices)





        world.Step(timeStep, vel_iters, pos_iters)
        pygame.display.flip()
        clock.tick(FPS)

        print(mbody.position, mbody.angle)
        print(bicep_body.position, bicep_body.angle)

        #TODO: add in little ball on end and modularize for arbitrary data

if __name__ == "__main__":
    main()

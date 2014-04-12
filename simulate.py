import math
from Box2D import *
from Box2D.b2 import *
import pygame
from pygame.locals import *
import GA.Caveman as cm

def create_caveman(world, x_pos, caveman):
    mbody = world.CreateDynamicBody(position=(x_pos, cm.HEIGHT/2))
    mbody_density = caveman.wBody / 2 *(1 * cm.HEIGHT/2)
    box = mbody.CreatePolygonFixture(box=(1, cm.HEIGHT/2), density=mbody_density , friction=0.3)

    a1, aq = caveman.appendages

    bicep_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep, caveman.arm_height), angle=pi/2)
    bicep_density = a1.wBicep / 2*(0.5 * a1.lBicep)
    bicep = bicep_body.CreatePolygonFixture(box=(a1.wBicep, aq.lBicep/2), density=bicep_density, friction=0.3)
    joint1 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep_body, localAnchorA=(0, cm.HEIGHT - caveman.arm_height/2), localAnchorB=(0, a1.lBicep/2), lowerAngle = -pi, upperAngle = pi, enableMotor=True)

    forearm_width = 0.5
    forearm_body = world.CreateDynamicBody(position=(x_pos+a1.lForearm, caveman.arm_height), angle=pi/2)
    forearm_density = a1.wForearm / 2*(0.5 * a1.lForearm)
    forearm = forearm_body.CreatePolygonFixture(box=(0.5, a1.lForearm/2), density=forearm_density, friction=0.3)

    joint2=world.CreateRevoluteJoint(bodyA=bicep_body, bodyB=forearm_body, localAnchorA=(0, -a1.lBicep/2), localAnchorB=(0, a1.lForearm/2), lowerAngle=-pi, upperAngle = pi)

    bopper_radius = a1.rBopper
    bopper_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep+a1.lForearm, caveman.arm_height), angle=0)
    bopper_density = a1.wBopper / pi*(a1.rBopper)**2
    bopper = bopper_body.CreateCircleFixture(radius=bopper_radius, density=bopper_density, friction=0.3)

    return [mbody, bicep_body, forearm_body, bopper_body]

def simulate(caveman1, caveman2, graphics_enabled):

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

    bodies1 = create_caveman(world, 5, caveman1)
    bodies2 = create_caveman(world, 25, caveman2)

    boppers = [bodies1[3], bodies2[3]]
    bodies1 = bodies1[:-1]
    bodies2 = bodies2[:-1]
    
    all_bodies = bodies1 + bodies2 + [groundBody]


    timeStep = 1.0 / FPS
    vel_iters = 6
    pos_iters = 2

    running = True
    while running:
        screen.fill((0,0,0,0))

        print "--------------"
        for body in all_bodies:
            for fixture in body.fixtures:
                shape = fixture.shape
                # print shape
                print body
                if body not in boppers:
                    vertices = [(body.transform*v)*PPM for v in shape.vertices]
                    vertices = [(v[0], SCREEN_HEIGHT-v[1]) for v in vertices]

                    if body == groundBody:
                        pygame.draw.polygon(screen, (0,255,0,255), vertices)
                    else:
                        pygame.draw.polygon(screen, (255,255,255,255), vertices)

                else:
                    pygame_radius = fixture.shape.radius * PPM
                    pygame_loc = (int(body.position[0] * PPM), int(SCREEN_HEIGHT - body.position[1]*PPM))
                    pygame.draw.circle(screen, (255,0,0,255), pygame_loc, int(pygame_radius))

        world.Step(timeStep, vel_iters, pos_iters)
        pygame.display.flip()
        clock.tick(FPS)

        # print(mbody.position, mbody.angle)
        # print(bicep_body.position, bicep_body.angle)

        #TODO: add in little ball on end and modularize for arbitrary data

if __name__ == "__main__":
    simulate(cm.Caveman(2), cm.Caveman(2), True)

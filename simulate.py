import math
from Box2D import *
from Box2D.b2 import *
import pygame
from pygame.locals import *
import GA.Caveman as cm
import numpy as np

def create_caveman(world, x_pos, caveman):
    mbody = world.CreateDynamicBody(position=(x_pos, cm.HEIGHT/2))
    mbody_density = caveman.wBody / 2 *(1 * cm.HEIGHT/2)
    box = mbody.CreatePolygonFixture(box=(1, cm.HEIGHT/2), density=mbody_density , friction=0.3)
    box.filterData.groupIndex = -x_pos

    a1, a2 = caveman.appendages

    bicep_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep/2, caveman.arm_height), angle=pi/2)
    bicep_density = a1.wBicep / 2*(0.5 * a1.lBicep)
    bicep = bicep_body.CreatePolygonFixture(box=(0.5, a1.lBicep/2), density=bicep_density, friction=0.3)
    bicep.filterData.groupIndex = -x_pos
    joint1 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep_body, localAnchorA=(0,caveman.arm_height - cm.HEIGHT/2.0) , localAnchorB=(0, a1.lBicep/2), lowerAngle = -pi, upperAngle = pi, enableMotor=True)

    forearm_width = 0.5
    forearm_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep, caveman.arm_height), angle=pi/2)
    forearm_density = a1.wForearm / 2*(0.5 * a1.lForearm)
    forearm = forearm_body.CreatePolygonFixture(box=(0.5, a1.lForearm/2), density=forearm_density, friction=0.3)
    forearm.filterData.groupIndex = -x_pos

    joint2=world.CreateRevoluteJoint(bodyA=bicep_body, bodyB=forearm_body, localAnchorA=(0, -a1.lBicep/2), localAnchorB=(0, a1.lForearm/2), lowerAngle=-pi, upperAngle = pi)

    bopper_radius = a1.rBopper
    bopper_body = world.CreateDynamicBody(position=(x_pos+a1.lBicep+a1.lForearm, caveman.arm_height), angle=0)
    bopper_density = a1.wBopper / pi*(a1.rBopper)**2
    bopper = bopper_body.CreateCircleFixture(radius=bopper_radius, density=bopper_density, friction=0.3)
    joint3=world.CreateRevoluteJoint(bodyA=forearm_body, bodyB=bopper_body, localAnchorA=(0, -a1.lForearm/2), localAnchorB=(0,0), lowerAngle=-pi, upperAngle=pi)

    bicep2_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep/2, caveman.arm_height), angle= -pi/2)
    bicep2_density2 = a2.wBicep / 2*(0.5 * a2.lBicep)
    bicep2 = bicep2_body2.CreatePolygonFixture(box=(0.5, a2.lBicep/2), density=bicep2_density2, friction=0.3)
    bicep2.filterData.groupIndex = -x_pos
    joint12 = world.CreateRevoluteJoint(bodyA=mbody, bodyB=bicep2_body2, localAnchorA=(0,caveman.arm_height - cm.HEIGHT/2.0) , localAnchorB=(0, a2.lBicep/2), lowerAngle = -pi, upperAngle = pi, enableMotor=True)

    forearm_width2 = 0.5
    forearm_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep, caveman.arm_height), angle= -pi/2)
    forearm_density2 = a2.wForearm / 2*(0.5 * a2.lForearm)
    forearm2= forearm_body2.CreatePolygonFixture(box=(0.5, a2.lForearm/2), density=forearm_density2, friction=0.3)
    forearm2.filterData.groupIndex = -x_pos

    joint22=world.CreateRevoluteJoint(bodyA=bicep2_body2, bodyB=forearm_body2, localAnchorA=(0, -a2.lBicep/2), localAnchorB=(0, a2.lForearm/2), lowerAngle=-pi, upperAngle = pi)

    bopper_radius2 = a2.rBopper
    bopper_body2 = world.CreateDynamicBody(position=(x_pos-a2.lBicep-a2.lForearm, caveman.arm_height), angle=0)
    bopper_density2 = a2.wBopper / pi*(a2.rBopper)**2
    bopper2 = bopper_body2.CreateCircleFixture(radius=bopper_radius2, density=bopper_density2, friction=0.3)
    joint3=world.CreateRevoluteJoint(bodyA=forearm_body2, bodyB=bopper_body2, localAnchorA=(0, -a2.lForearm/2), localAnchorB=(0,0), lowerAngle=-pi, upperAngle=pi)

    return ([mbody, bicep_body, forearm_body, bopper_body, joint1, joint2], [mbody, bicep2_body2, forearm_body2, bopper_body2, joint12, joint22])

def simulate(caveman1, caveman2, graphics_enabled):

    PPM = 20.0 # pixels per meter
    FPS = 60
    SCREEN_WIDTH, SCREEN_HEIGHT=640,480
    
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("Bopper")
    clock = pygame.time.Clock()


    world = b2World()
    groundBody=world.CreateStaticBody(
            userData="ground",
            position=(0, -9),
            shapes=b2PolygonShape(box=(50,10)))

    bodies1_1, bodies1_2 = create_caveman(world,15, caveman1)
    mbody = bodies1_1[0]
    joint1_1 = bodies1_1[-2:]
    bodies1_1 = bodies1_1[:-2]
    joint1_2 = bodies1_2[-2:]
    bodies1_2 = bodies1_2[:-2]
    bodies2_1, bodies2_2 = create_caveman(world, 22, caveman2)
    mbody2 = bodies2_1[0]
    bodies2_1 = bodies2_1[:-2]
    joint2_1 = bodies2_1[-2:]
    bodies2_2 = bodies2_2[:-2]
    joint2_2 = bodies2_2[-2:]
    all_bodies = bodies1_1 + bodies2_1 + [groundBody] + bodies1_2 + bodies2_2

    boppers = [bodies1_1[3], bodies2_1[3], bodies1_2[3], bodies2_2[3]]
    bodies1_1 = bodies1_1[:-1]
    bodies2_1 = bodies2_1[:-1]
    bodies1_2 = bodies1_2[:-1]
    bodies2_2 = bodies2_2[:-1]

    game_over_bodies1 = bodies1_1 + bodies1_2
    game_over_bodies2 = bodies2_1 + bodies2_2
    
    timeStep = 1.0 / FPS
    vel_iters = 6
    pos_iters = 2

    running = True
    while running:

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    import pdb; pdb.set_trace()

        for b in game_over_bodies1:
            for contact in b.contacts:
                if contact.other.userData == 'ground':
                    if b is not mbody and b is not mbody2:
                        print "Player 1 loses"
                    if b is mbody and mbody.worldCenter[1] < 2.03:
                        print "Player 1 loses"

        for b in game_over_bodies2:
            for contact in b.contacts:
                if contact.other.userData == 'ground':
                    if b is not mbody and b is not mbody2:
                        print "Player 2 loses"
                        # import pdb; pdb.set_trace()
                    if b is mbody2 and mbody2.worldCenter[1] < 2.03:
                        print "Player 2 loses"
                        # import pdb; pdb.set_trace()

        # import pdb; pdb.set_trace()
        # np.polynomial.polynomial.polyval(1, caveman1.appendages[0].iElbow)
        # Motors for first arm of first robot
        joint1_1[0].maxMotorTorque = 1000
        joint1_1[0].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iShoulder)
        joint1_1[1].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iElbow)

        #Motors for first arm of 2nd robot
        joint2_1[0].maxMotorTorque = 1000
        joint2_1[0].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iShoulder)
        joint2_1[1].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iElbow)

        # Motors for second arm of first robot
        joint1_2[0].maxMotorTorque = 1000
        joint1_2[0].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iShoulder)
        joint1_2[1].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iElbow)

        #Motors for second arm of 2nd robot
        joint2_2[0].maxMotorTorque = 1000
        joint2_2[0].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iShoulder)
        joint2_2[1].motorSpeed = np.polynomial.polynomial.polyval(clock.get_time() % 1, caveman1.appendages[1].iElbow)

        # print np.polynomial.polynomial.polyval(clock.get_time()*100, caveman1.appendages[0].iElbow)

        if graphics_enabled:
            screen.fill((0,0,0,0))
            for body in all_bodies:
                for fixture in body.fixtures:
                    shape = fixture.shape
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


        if clock.get_time() > 20000: #Tie after 100 seconds
            if mbody.worldCenter[1] > mbody2.worldCentes[1]:
                print "Player 1 wins"
            else:
                print "Player 2 wins"

if __name__ == "__main__":
    simulate(cm.Caveman(2), cm.Caveman(2), True)

import pygame
import numpy as np
import math
#-------------------------------------------------------------------------------------
class Charge:
    def __init__(self,x,y,q):
        self.x = x
        self.y = y
        self.q = q
        self.radius = 15

def calculate_field(x, y, q, point_x, point_y ):
    dx = point_x - x
    dy = point_y - y

    distance = np.sqrt(dx**2+dy**2)
    distance = np.clip(distance, 1e-4, None)

    k = 8.99e9

    e_magnitude = (k*(q))/(distance**2)

    unit_x = dx / distance
    unit_y = dy / distance

    eE_x = unit_x * e_magnitude
    eE_y = unit_y * e_magnitude
    return eE_x, eE_y

def trace_field_line(start_x,start_y,charges,step_size=4,max_steps=300):
    points = [(start_x, start_y)]
    x, y = start_x, start_y

    for _ in range(max_steps):
        total_ex = 0.0
        total_ey = 0.0

        for charge in charges:
            ex, ey = calculate_field(charge.x, charge.y, charge.q, x, y)
            total_ex += ex
            total_ey += ey

        magnitude = np.sqrt(total_ex**2 + total_ey**2)
        if magnitude < 1e-9:
            break

        unit_x = total_ex / magnitude
        unit_y = total_ey / magnitude

        x += unit_x * step_size
        y += unit_y * step_size

        points.append((x,y))

        hit_charge = False
        for charge in charges:
            if math.hypot(x - charge.x, y - charge.y)<charge.radius:
                hit_charge = True
                break
        if hit_charge:
            break

        if x< 0 or x > 640 or y<0 or y> 640:
            break

    return points

def draw_arrowhead(screen, p1, p2, color, size=8):
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    lenght = math.hypot(dx,dy)

    if lenght == 0:
        return
    
    unit_x, unit_y = dx/lenght, dy/lenght
    prep_x, prep_y = -unit_y, unit_x

    tip= p2
    left = (p2[0] - unit_x * size + prep_x * size * 0.5,
            p2[1] - unit_y * size + prep_y * size * 0.5)
    right = (p2[0] - unit_x * size - prep_x * size * 0.5,
             p2[1] - unit_y * size - prep_y * size * 0.5)
    
    pygame.draw.polygon(screen,color,[tip,left,right])

def create_dipole(center_x,center_y,separation):
    positive_x = center_x - separation // 2
    negative_x = center_x + separation // 2

    charges.append(Charge(positive_x, center_y, 5))
    charges.append(Charge(negative_x, center_y, -5))

def create_quadrupole(center_x,center_y,half_size,separation):
    positions = [
        (center_x - half_size, center_y - half_size),
        (center_x + half_size, center_y - half_size),
        (center_x + half_size, center_y + half_size),
        (center_x - half_size, center_y + half_size),
    ]

    signs = [5, -5, 5, -5]

    for (x, y), charge_q in zip(positions, signs):
        charges.append(Charge(x,y,charge_q))

#-------------------------------------------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((640,640))
pygame.display.set_caption("Electromagnetic Field Simulation")
running = True
#-------------------------------------------------------------------------------------
FONT = pygame.font.SysFont("Arial",14)
FONT_BOLD = pygame.font.SysFont("Arial",15,bold=True)
#-------------------------------------------------------------------------------------
charges = []
color = (0,0,0)
selected_charge = None
electric_lines = False
dipole = False
quadrupole = False
center_x,center_y = 320, 320
separation = 100
half_size = 80
#-------------------------------------------------------------------------------------
while running:
    screen.fill((0,0,0))
    spacing = 40
    length = 30

#-------------------------------------------------------------------------------------
    for pos_x in range(0,640,spacing):
        for pos_y in range(0,640,spacing):

            total_equilavent_x = 0.0
            total_equilavent_y = 0.0

            for charge in charges:
                ex,ey = calculate_field(charge.x,charge.y,charge.q,pos_x,pos_y)

                total_equilavent_x += ex
                total_equilavent_y += ey

            e_magnitude_distance = np.sqrt(total_equilavent_x**2 + total_equilavent_y**2)

            if e_magnitude_distance > 0:
                unit_x = total_equilavent_x / e_magnitude_distance
                unit_y = total_equilavent_y / e_magnitude_distance

                arrow_length = np.clip(e_magnitude_distance * 1e-7,15,length)

                strenght = np.log1p(e_magnitude_distance)
                normalized = np.clip((strenght - 5) / (22-2),0,1)
                red = int(normalized * 255)
                blue = int((1 - normalized) * 255)
                arrow_color = (red, 0, blue)


                end_of_x = pos_x + unit_x * arrow_length
                end_of_y = pos_y + unit_y * arrow_length

                pygame.draw.line(screen,arrow_color,(pos_x,pos_y),(end_of_x,end_of_y))
                pygame.draw.circle(screen,(255,255,255),(int(end_of_x),int(end_of_y)),2)


#-------------------------------------------------------------------------------------
    if electric_lines == True:
        for charge in charges:
            if charge.q > 0:
                for i in range(12):
                    angle = (2 * math.pi / 12) * i
                    start_x = charge.x + charge.radius * math.cos(angle)
                    start_y = charge.y + charge.radius * math.sin(angle)

                    line_points = trace_field_line(start_x,start_y,charges)

                    if len(line_points) >1:
                        pygame.draw.lines(screen,(255,255,255),False,line_points,2)

                        mid_index = len(line_points) // 2
                        if mid_index + 1 < len(line_points):
                            draw_arrowhead(screen,line_points[mid_index],line_points[mid_index+1],(255,255,255))
#-------------------------------------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicking_existing = False
            x,y = event.pos

            for charge in charges:
                distance_of_charge = math.hypot(x - charge.x, y - charge.y)
                if distance_of_charge <= charge.radius:
                    selected_charge = charge
                    clicking_existing = True
                    break

            if not clicking_existing:
                if event.button == 1:
                    new_charge = Charge(x,y,5)
                    charges.append(new_charge)
                elif event.button == 3:
                    new_charge = Charge(x,y,-5)
                    charges.append(new_charge)

        elif event.type == pygame.MOUSEMOTION:
            if selected_charge is not None:
                selected_charge.x,selected_charge.y = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_charge = None

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                charges.clear()
                dipole = False
                quadrupole = False

            elif event.key == pygame.K_l:
                electric_lines = not electric_lines

            elif event.key == pygame.K_1:
                if not dipole and not quadrupole:
                    create_dipole(center_x, center_y, separation)
                    dipole = True

            elif event.key == pygame.K_2:
                if not quadrupole and not dipole:
                    create_quadrupole(center_x, center_y,half_size,separation)
                    quadrupole = True

#-------------------------------------------------------------------------------------
        if event.type == pygame.QUIT:
            running = False
#-------------------------------------------------------------------------------------
    for charge in charges:
        if charge.q > 0:
            color = (85,148,250)
        else:
            color = (255,41,112)
        pygame.draw.circle(screen,color,(charge.x,charge.y),charge.radius)
#-------------------------------------------------------------------------------------
    legend_lines = [
        "Left Mouse Click: Add positive charge",
        "Right Mouse Click: Add negative charge",
        "Click and hold on a charge to drag",
        "Button R: Reset charges",
        "Button L: Toggle field lines",
    ]
    preset_lines =[
        "Presets:",
        "Button 1: Dipole",
        "Button 2: Quadrupole"
    ]



    legend_x,legend_y = 10,10
    legend_height = 18

    preset_box_width = 200 
    preset_box_height = len(preset_lines)*legend_height+16

    preset_x = 640 - preset_box_width - 10
    preset_y = 10


    box_width, box_height = 260, len(legend_lines) * legend_height + 16
    pygame.draw.rect(screen,(15,15,25),(5,5,box_width,box_height))
    pygame.draw.rect(screen,(80,80,100),(5,5,box_width,box_height))

    pygame.draw.rect(screen,(15,15,25),(preset_x,preset_y,preset_box_width, preset_box_height))
    pygame.draw.rect(screen,(80,80,100),(preset_x,preset_y,preset_box_width, preset_box_height),1)

    for i, text in enumerate(legend_lines):
        rendered = FONT.render(text,True,(255,255,255))
        screen.blit(rendered, (legend_x,legend_y + i * legend_height))

    for j, text in enumerate(preset_lines):
        rendered = FONT.render(text,True,(255,255,255))
        screen.blit(rendered,(preset_x + 10, preset_y + 10 + j * legend_height))
#-------------------------------------------------------------------------------------
    pygame.display.flip()

pygame.quit()




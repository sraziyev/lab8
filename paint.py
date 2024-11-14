import pygame
from math import sqrt

def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    baseLayer = pygame.Surface((640, 480))
    clock = pygame.time.Clock()
    prevX = 0
    prevY = 0
    prevX1 = -1
    prevY1 = -1
    currentX1 = -1
    currentY1 = -1

    color = (0, 0, 0)
    screen.fill((255, 255, 255))
    baseLayer.fill((255, 255, 255))
    isMouseDown = False
    freehand = False

   
    pen_thickness = 5  
    eraser_thickness = 10  

    while True:
        pressed = pygame.key.get_pressed()
        currentX = prevX
        currentY = prevY
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    isMouseDown = True
                    if pressed[pygame.K_1]:  
                        prevX1 = event.pos[0]
                        prevY1 = event.pos[1]
                    elif pressed[pygame.K_2]:
                        prevX1 = event.pos[0]
                        prevY1 = event.pos[1]
                    elif pressed[pygame.K_0]:
                        prevX = event.pos[0]
                        prevY = event.pos[1]
                    elif pressed[pygame.K_3]: 
                        prevX = event.pos[0]
                        prevY = event.pos[1]

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    isMouseDown = False
                    baseLayer.blit(screen, (0, 0))
            if event.type == pygame.MOUSEMOTION:
                currentX = event.pos[0]
                currentY = event.pos[1]
                if isMouseDown and (freehand or pressed[pygame.K_0]):  
                    pygame.draw.line(screen, color, (prevX, prevY), (currentX, currentY), pen_thickness)
                    prevX = currentX
                    prevY = currentY
                elif isMouseDown and pressed[pygame.K_3]: 
                    pygame.draw.line(screen, (255, 255, 255), (prevX, prevY), (currentX, currentY), eraser_thickness)
                    prevX = currentX
                    prevY = currentY
                elif isMouseDown and pressed[pygame.K_1]:  
                    currentX1 = event.pos[0]
                    currentY1 = event.pos[1]
                    screen.blit(baseLayer, (0, 0))
                    r = calculateRect(prevX1, prevY1, currentX1, currentY1)
                    pygame.draw.rect(screen, color, pygame.Rect(r), 1)
                elif isMouseDown and pressed[pygame.K_2]: 
                    currentX1 = event.pos[0]
                    currentY1 = event.pos[1]
                    screen.blit(baseLayer, (0, 0))
                    c = centerCirc(prevX1, prevY1, currentX1, currentY1)
                    ra = radiusCirc(prevX1, prevY1, currentX1, currentY1)
                    pygame.draw.circle(screen, color, c, ra, 1)

            if event.type == pygame.KEYDOWN:  
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_y:
                    color = (255, 255, 0)
                elif event.key == pygame.K_p:
                    color = (255, 0, 255) 
                elif event.key == pygame.K_k:
                    color = (0, 0, 0)
                elif event.key == pygame.K_f:
                    freehand = not freehand 

        pygame.display.flip()
        clock.tick(60)

def calculateRect(x1, y1, x2, y2):
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def centerCirc(x1, y1, x2, y2):
    return abs(x1 - x2) / 2 + min(x1, x2), abs(y1 - y2) / 2 + min(y1, y2)

def radiusCirc(x1, y1, x2, y2):
    return int(sqrt((((abs(x1 - x2) / 2) ** 2) + (abs(y1 - y2) / 2) ** 2)))

main()

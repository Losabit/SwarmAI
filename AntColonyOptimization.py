from DrawerHelper import *

dHelper = DrawerHelper("test", 200, 200)

# run the game loop
while True:
    dHelper.draw_rect(dHelper.BLUE, (12, 20, 40 , 50))
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
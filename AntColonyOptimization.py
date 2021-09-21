from DrawerHelper import *


class AntColonyOptimization:

    def __init__(self):
        self.dHelper = DrawerHelper("AntColonyOptimization Example", 200, 200)

    def update(self):
        # run the game loop
        while True:
            self.dHelper.draw_rect(self.dHelper.BLUE, (12, 20, 40, 50))
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


demo = AntColonyOptimization()
demo.update()

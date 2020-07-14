import pygame 
class Button:

    def __init__(self, bColor, x, y, width, height, 
                fColor = (255, 255, 255), oColor = (0, 0, 0), text=''):
        
        self.bColor = bColor
        self.fColor = fColor
        self.oColor = oColor
        self.x = x
        self.y = y
        self.width = width
        self.height = height 
        self.text = text
        self.clickColor = (0, 0, 0)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def drawButton(self, window, mousePosition, click):
        ## Draws the button
        
        pygame.draw.rect(window, self.bColor, self.rect,0)

        if self.isOver(mousePosition):
            pygame.draw.rect(window, self.oColor, self.rect, 3)

        if click == True:
            pygame.draw.rect(window, self.clickColor, self.rect, 0)

        if self.text != "":
            font = pygame.font.SysFont ("comicsans", 56)
            text = font.render(self.text, 1, self.fColor)
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), 
                        self.y + (self.height/2 - text.get_height()/2)))
        
    def isOver(self, mousePosition):
        
        if mousePosition[0] > self.x and mousePosition[0] < self.x + self.width:
            if mousePosition[1] > self.y and mousePosition[1] < self.y + self. height:
                return True
        else:
            return False

    def getRect(self):
        return self.rect


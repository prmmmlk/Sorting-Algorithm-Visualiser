import pygame
import random


class Visualiser:
    def __init__(self) -> None:

        # Dimensions
        self.WIDTH = 900
        self.HEIGHT = 500

        # Color constants
        self.BLUE = 1
        self.GREEN = 2
        self.RED = 3
        self.YELLOW = 4
        self.AQUA = 5
        self.LIME = 6
        
        # Dict which maps to colors
        self.color_map = {
            self.BLUE: (0, 0, 255),
            self.GREEN: (0, 255, 0),
            self.RED: (255, 0, 0),
            self.YELLOW: (255, 255, 0),
            self.AQUA: (64, 224, 208),
            self.LIME: (230, 255, 230)
        }

        # Controls framerate
        self.clock = pygame.time.Clock()

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption('Sorting Algorithm Visualiser')

        self.myfont = pygame.font.SysFont('Comic Sans MS', 12)

        self.press_g = self.myfont.render(
            'Press g to generate a new set', False, self.color_map[self.GREEN])
        self.press_b = self.myfont.render(
            'Press b to bubble sort', False, self.color_map[self.GREEN])
        self.press_s = self.myfont.render(
            'Press s to selection sort', False, self.color_map[self.GREEN])
        self.press_m = self.myfont.render(
            'Press m to merge sort', False, self.color_map[self.GREEN])

        # Keybindings which correspond to an event
        self.events = {
            pygame.K_b: 'b', # bubble sort
            pygame.K_s: 's', # selection sort
            pygame.K_m: 'm', # merge sort
            pygame.K_g: None # generate new set
        }

        # determines which algorithm to run
        self.runSort = None

        # counter for each iteration of algorithm
        self.cycle = 0

        # used when running 'finished' animation
        self.finalCount = 0
        
        # frame rate
        self.FRAMES = 50

    def generateCaption(self):
        self.window.blit(self.press_g, (15, 15))
        self.window.blit(self.press_b, (15, 35))
        self.window.blit(self.press_s, (15, 55))
        self.window.blit(self.press_m, (15, 75))


class Rectangles(Visualiser):
    def __init__(self) -> None:
        super().__init__()
        self.REC_WIDTH = 20
        self.REC_COUNT = int(self.WIDTH/self.REC_WIDTH)

        self.recs = self.rec_array()
        self.states = self.rec_state()

    # Function which generates an array of rectangles of random height.
    def rec_array(self):
        return [random.randint(10, 350) for _ in range(self.REC_COUNT)]

    # Function which generates the state of each rectangle to determine whether it is not sorted, being sorted or sorted.
    def rec_state(self):
        return [1 for _ in range(self.REC_COUNT)]
    
    # Runs when a key is pressed. 
    def run_event(self, key):
        self.runSort = key
        self.cycle = 0
        self.finalCount = 0

        if key == None:
            self.window.fill('BLACK')
            self.recs = self.rec_array()
            self.states = self.rec_state()

    # Draws resetted rectangles onto the screen.
    def reset_rectangles(self):
        for i in range(self.REC_COUNT):
            pygame.draw.rect(self.window, self.color_map[self.BLUE], pygame.Rect(
                self.REC_WIDTH*i, self.HEIGHT-self.recs[i], self.REC_WIDTH, self.recs[i]))
        self.generateCaption()

    # Draws rectangles depending on the color
    def generateRectangles(self, i):
        color = self.color_map[self.states[i]]
        # Draws the rectangle.
        pygame.draw.rect(self.window, color, pygame.Rect(
            self.REC_WIDTH*i, self.HEIGHT-self.recs[i], self.REC_WIDTH, self.recs[i]))

    # Animations which runs when the rectangles have been sorted.
    def finished(self):
        for i in range(self.REC_COUNT):
            self.generateCaption()
            self.generateRectangles(i)
        if self.finalCount < self.REC_COUNT:
            self.states[self.finalCount] = 2
            self.finalCount += 1

        self.clock.tick(1000)
        pygame.display.update()

class Algorithm(Rectangles):
    def __init__(self) -> None:
        super().__init__()

    def bubbleSort(self):
        # Check if the number of iterations is still less than the number of rectangles (i.e. if the rectangles are fully sorted).
        if self.cycle < len(self.recs):
            for rec_height in range(len(self.recs) - self.cycle - 1):
                self.window.fill('BLACK')

                # Check if the first rectangles height is greater than the next rectangles height.
                if self.recs[rec_height] > self.recs[rec_height + 1]:

                    # Change the color of the rectangles being compared.
                    self.states[rec_height] = 6
                    self.states[rec_height+1] = 3

                    # Swap the rectangles and generate a new set of rectangles and update the screen.
                    self.recs[rec_height], self.recs[rec_height +
                                                        1] = self.recs[rec_height+1], self.recs[rec_height]
                    for i in range(self.REC_COUNT):
                        self.generateCaption()
                        self.generateRectangles(i)
                        self.states[i] = 1
                    self.clock.tick(self.FRAMES)
                    pygame.display.update()
                else:
                    # Change the color of the rectangles being compared.
                    self.states[rec_height] = 6
                    self.states[rec_height+1] = 3

                    # Keep the rectangles in their original positions and generate a new set of rectangles and update the screen.
                    for i in range(self.REC_COUNT):
                        self.generateCaption()
                        self.generateRectangles(i)
                        self.states[i] = 1
                    self.clock.tick(self.FRAMES)
                    pygame.display.update()
        else:
            self.finished()
    
    def selectionSort(self):
        # Check if the number of iterations is still less than the number of rectangles (i.e. if the rectangles are fully sorted).
        if self.cycle < len(self.recs):

            # Keeps track of the shortest rectangle.
            minimumIndex = self.cycle
            for rec_height in range(self.cycle+1, len(self.recs)):
                #self.window.fill('BLACK')
                # Sets the state of the rectangles being compared.
                self.states[minimumIndex] = 3
                self.states[rec_height] = 4
                for i in range(self.REC_COUNT):
                    self.generateCaption()
                    self.generateRectangles(i)
                self.clock.tick(self.FRAMES)
                pygame.display.update()

                # If a smaller rectangle has been found, the states are changed the new smallest rectangle is taken into account.
                if self.recs[rec_height] < self.recs[minimumIndex]:
                    self.states[minimumIndex] = 1
                    self.states[rec_height] = 1
                    minimumIndex = rec_height
                else:
                    self.states[rec_height] = 1
                    pass
            
            # The smallest rectangle is placed at the beginning of the array.
            self.recs[self.cycle], self.recs[minimumIndex] = self.recs[minimumIndex], self.recs[self.cycle]

    
            # Refreshes the screen.
            for i in range(self.REC_COUNT):
                # self.states[self.cycle] = 1
                # self.states[minimumIndex] = 1
                self.states[i] = 1
                self.generateCaption()
                self.generateRectangles(i)
            self.clock.tick(self.FRAMES)
            pygame.display.update()
        else:
            self.finished()

    def merge_sort(self, data):
        self.merge_sort_alg(data, 0, len(data)-1)

# Function which recursively divides the larger array into smaller sub-arrays.
    def merge_sort_alg(self, data, left, right):

        # Checks if the array can be divided further.
        if left < right:
            middle = (left + right) // 2
            self.merge_sort_alg(data, left, middle)
            self.merge_sort_alg(data, middle+1, right)
            
            # Calls the function to merge the small arrays into a larger one.
            self.merge(data, left, middle, right)

    # Merge the small arrays into a larger one.
    def merge(self, data, left, middle, right):

        # Variables to store the left half and right half of an array.
        leftPart = data[left:middle+1]
        rightPart = data[middle+1:right+1]

        # The index of each element being compared.
        leftIndex = rightIndex = 0
        self.window.fill('BLACK')

        # Iterate over the sub arrays
        for dataIndex in range(left, right+1):
            self.window.fill('BLACK')
            self.states[dataIndex] = 5

            # Check if the index we are accessing is within the array.
            if leftIndex < len(leftPart) and rightIndex < len(rightPart):

                # Compare the rectangle heights and add the smaller rectangle to the new "merged" array.
                if leftPart[leftIndex] <= rightPart[rightIndex]:
                    data[dataIndex] = leftPart[leftIndex]
                    leftIndex += 1
                    for i in range(self.REC_COUNT):
                        self.generateCaption()
                        self.generateRectangles(i)
                    self.states[dataIndex] = 1
                    pygame.display.update()
                else:
                    data[dataIndex] = rightPart[rightIndex]
                    for i in range(self.REC_COUNT):
                        self.generateCaption()
                        self.generateRectangles(i)
                    self.states[dataIndex] = 1
                    pygame.display.update()
                    rightIndex += 1
            
            # Check if the left array has been fully traversed.
            elif leftIndex < len(leftPart):
                data[dataIndex] = leftPart[leftIndex]
                for i in range(self.REC_COUNT):
                    self.generateCaption()
                    self.generateRectangles(i)
                self.states[dataIndex] = 1
                pygame.display.update()
                leftIndex += 1
            
            # Check if the right array has been fully traversed.
            else:
                data[dataIndex] = rightPart[rightIndex]
                for i in range(self.REC_COUNT):
                    self.generateCaption()
                    self.generateRectangles(i)
                self.states[dataIndex] = 1
                pygame.display.update()
                rightIndex += 1


			


if __name__ == '__main__':
    pygame.init()

    running = True

    visualiser = Visualiser()
    algorithm = Algorithm()


    while running:

        visualiser.window.fill(('BLACK'))

        # Listen for keystrokes
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                try:
                    algorithm.run_event(visualiser.events[event.key])
                except KeyError as error:
                    print(f"Key error: {error}")
                    pass

        if visualiser.runSort == None:
            algorithm.reset_rectangles()

        if algorithm.runSort == 'b':
            algorithm.bubbleSort()
            algorithm.cycle += 1
            
        if algorithm.runSort == 's':
            algorithm.selectionSort()
            algorithm.cycle += 1

        if algorithm.runSort == 'm':
            if algorithm.cycle < 1:
                algorithm.merge_sort(algorithm.recs)
                algorithm.cycle += 1

                # Refresh the screen.
                for i in range(algorithm.REC_COUNT):
                    algorithm.generateCaption()
                    algorithm.generateRectangles(i)
                pygame.display.update()
            else:
                # Display the finished animation.
                algorithm.finished()

        pygame.display.update()

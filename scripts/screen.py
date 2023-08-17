import cv2
import numpy as np
from PIL import ImageGrab

img = cv2.imread(filename="C:\Repositories\wizmatic\images\(Spell)_Scarecrow.png")

while (True):
    screen = np.array(ImageGrab.grab())
    screen = cv2.cvtColor(src=screen, code=cv2.COLOR_BGR2RGB)
    cv2.imshow('my_screen', screen)
    
    # press escape to exit
    if (cv2.waitKey(30) == 27):
       break
cv2.destroyAllWindows()
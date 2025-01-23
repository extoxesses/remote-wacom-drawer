from pyautogui import mouseDown, mouseUp
import time

button = 'primary'
time.sleep(2)

print('Clicking the mouse button')
mouseDown(button=button)
time.sleep(5)
print('Releasing the mouse button')
mouseUp(button=button)
import cv2
import os
import glob
import numpy

cards = {}
card_files = glob.glob('cards/*.png')

for card in card_files:
    cardname = card[6:-4]
    cardpng = cv2.imread(card)
    cardgreypng = cv2.cvtColor(cardpng, cv2.COLOR_BGR2GRAY)
    cards[cardname] = cardgreypng

os.system('adb exec-out screencap -p > screen.png')

img_rgb = cv2.imread('screen.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)

for card in cards:
    template = cards[card]
    w, h = template.shape[::-1]
    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF)
    y,x = numpy.unravel_index(res.argmax(), res.shape)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    dist_val = max_val - min_val
    print card
    print dist_val
    #print(cv2.minMaxLoc(res))
    if max_val < 175000000:
        continue
    if min_val < -150000000:
        continue
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    img_out = img_rgb.copy()
    cv2.rectangle(img_out, top_left, bottom_right, 255, 2)
    cv2.imwrite('output/' + card + 'res.png',img_out)

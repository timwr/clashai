import time
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

def play_card(slot, position):
    print "Playing slot " + str(slot) + " to " + str(position)
    sx = 400 + slot * 270
    px = position[0]
    py = position[1]
    playstr = "adb shell input swipe " + str(sx) + " 2400 " + str(px) + " " + str(py)
    #print "Playing: " + playstr
    os.system(playstr)

def get_hand():
    #os.system('rm output/*.png')
    os.system('adb exec-out screencap -p > screen.png')

    img_rgb = cv2.imread('screen.png')
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
    img_match = img_gray
    hand = [None, None, None, None]

    for card in cards:
        template = cards[card]
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(img_match,template,cv2.TM_CCOEFF)
        y,x = numpy.unravel_index(res.argmax(), res.shape)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        dist_val = max_val - min_val
        #print card
        #print(cv2.minMaxLoc(res))
        #if max_val < 180000000:
            #continue
        top_left = max_loc
        if top_left[1] < 2300 or top_left[1] > 2310:
            continue
        slot = (top_left[0] - 310) / 270
        if slot < 0 or slot > 3:
            continue
        #print slot, card
        if not hand[slot] or hand[slot][0] < max_val:
            hand[slot] = (max_val, card)
        #print(cv2.minMaxLoc(res))
        #bottom_right = (top_left[0] + w, top_left[1] + h)
        #img_out = img_rgb.copy()
        #cv2.rectangle(img_out, top_left, bottom_right, 255, 2)
        #cv2.imwrite('output/' + card + 'res.png',img_out)
    return hand

#play_card(2, (400, 1500))
#time.sleep(1)
#play_card(1, (400, 1500))
#time.sleep(3)

while True:
    hand = get_hand()
    print hand
    index = 0
    for x in range(0, 3):
        if hand[x] == None:
            continue
        if hand[x][1] == 'Fireball':
            continue
        if hand[x][1] == 'Arrows':
            continue
        index = x
        break
    play_card(index, (400, 1500))
    time.sleep(4)


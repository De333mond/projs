from random import random
from PyQt5 import QtWidgets, uic
from time import sleep, mktime, localtime
from numpy import true_divide
import pyautogui 
from threading import Thread


def getTime():
    return mktime(localtime())

def craft(index, amount, num):
    clickTimeout = 0.4
    startTime = getTime()
    count = amount #ui.spinBox.value()
    while (count > 0):
        # select(ui.part.currentIndex())
        select(index)

        sleep(clickTimeout)
        pyautogui.click(1580,950) # click create btn 
        sleep(clickTimeout)
        pyautogui.click(850,630) # click accept btn
        sleep(clickTimeout)

        complete = False
        while not complete:
            print("waiting", complete)
            sleep(0.3)
            
            print(getTime()-startTime)
            if (getTime()-startTime > 60*7):
                startTime = getTime()
                if not complete:
                    antiAFK()

            try: 
                if pyautogui.pixelMatchesColor(360,13, (255,255,0)):
                    complete = True
            except Exception:
                pass

            if ui.StartBTN.text() != "Stop":
                return 0
       
        sleep(clickTimeout)
        pyautogui.click(1580,950) # click get btn
        sleep(clickTimeout)
        count -= 1
        if num == 1:
            ui.spinBox.setValue(count)
        elif num == 2:
            ui.spinBox_2.setValue(count)
        elif num == 3:
            ui.spinBox_3.setValue(count)

            


def main():
    print("u in main", ui.StartBTN.text())
    
    if ((ui.spinBox.value() > 0) and (ui.StartBTN.text() != "Start")):
        print("1st condition")
        craft(index=ui.part.currentIndex(), amount= ui.spinBox.value(), num = 1)
    
    if (ui.spinBox_2.value() > 0) & (ui.StartBTN.text() != "Start"):
        print("2st condition")
        craft(index=ui.part_2.currentIndex(), amount= ui.spinBox_2.value(), num = 2)
    
    # if (ui.spinBox_3.value() > 0) & (ui.StartBTN.text() != "Start"):
    #     print("3st condition")
    #     craft(index=ui.part_3.currentIndex(), amount= ui.spinBox_3.value(), num = 3)
    
    ui.StartBTN.setText("Start")

def StartBtn_clicked():
    if ui.StartBTN.text() == "Start":
        craft_thread = Thread(target=main, name="Crafting Thread")
        ui.StartBTN.setText("Stop")
        craft_thread.start()
    else:
        ui.StartBTN.setText("Start")
        sleep(0.5)

def select(button):
    # button = ui.part.currentIndex()
    len = ui.part.count() 
    if button <= 6:
        pyautogui.moveTo(1310,440)
        pyautogui.vscroll(2000)
        sleep(0.2)
        pyautogui.vscroll(2000)
        sleep(0.2)
        pyautogui.click(440, 320+110*button)

    else: 
        pyautogui.moveTo(1310,440)
        sleep(0.2)
        pyautogui.scroll(1)
        sleep(0.2)
        pyautogui.scroll(1)

        pyautogui.click(440, 940-(110*(len - button - 1)))



def antiAFK():
    select(1)
    sleep(0.5)
    select(0)

pyautogui.FAILSAFE = False

application = QtWidgets.QApplication([])
ui = uic.loadUi("UI.ui")
ui.setWindowTitle("CraftBot")

ui.StartBTN.clicked.connect(StartBtn_clicked) 


ui.show()
application.exec()






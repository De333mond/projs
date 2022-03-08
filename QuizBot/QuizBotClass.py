from PyQt5 import QtWidgets, uic
import configparser
from threading import Thread
from time import *
from ahk import AHK
import keyboard
from random import random



class Quizbot():
    
    SettingsPath = 'settings.ini'
    ui_dir = 'sorce/reload1.1.ui'
    log_dir = 'C:\.lemoncraft\logs\latest.log'
    answ_dir = 'source/answer.txt'
    nickname = 'Dezzzmond'
    score = 0
    cur_time_str = ''

    ChatlogLines = []

    def __init__(self):
        self.application = QtWidgets.QApplication([])
        self.ui = uic.loadUi(r'C:\Users\vladb\Desktop\VScode\654\source\reload1.1.ui')
        self.ui.setWindowTitle('QuizBot')

        self.LoadSettings()



        self.ui.OpenLogBTN.clicked.connect(self.OpenLog)
        self.ui.OpenAnswBTN.clicked.connect(self.OpenAnswers)
        self.ui.A_Save.triggered.connect(self.SaveSettings)
        self.ui.A_Load.triggered.connect(self.LoadSettings)
        self.ui.StartBTN.clicked.connect(self.StartBtn_clicked)

    
    

    def gettime(self):
        return self.cur_time_str

    def checkWin(self):
        self.score = 0
        lines = self.ChatlogLines
        for line in lines:
            if self.nickname in line and 'победил!' in line:
                self.score += 50
        self.ui.lcd_total.display(self.score)

    def Tap(self, HotKey, Text, Delay=0.05):
        ahk = AHK()
        ahk.send(HotKey)
        sleep(0.05)
        for s in Text:
            keyboard.write(s)
            sleep(Delay - random()*0.007 + random()*0.014)
        sleep(0.05)
        keyboard.send('enter')

    def delay(self, question):

        if bool(self.ui.CB_Emulate_reading.isChecked()):
             Del = len(question)*int(self.ui.LE_reading_delay.text())/1000 + random()*float(self.ui.LE_random_multi.text())/1000
        else: Del =  int(self.ui.LE_delay_after_detecting.text())/1000 + random()*float(self.ui.LE_random_multi.text())/1000
        if Del < 1:
            print(1.2 + Del)
            return 1.2 + Del
        else:
            print(Del)
            return Del

    def Start(self):
        self.ui.show()
        self.application.exec()

    def LoadSettings(self):
        path = 'settings.ini'

        config = configparser.ConfigParser()
        config.read(path)

        try: self.nickname = config['Settings']['Nickname']
        except KeyError:
            self.SaveSettings()
            self.LoadSettings()

        self.log_dir = config['Dirs']['Log Directory']
        self.answ_dir = config['Dirs']['Answers Directory']

        self.ui.LE_check_timeout.setText(config['Settings']['Check timeout'])
        self.ui.LE_delay_after_detecting.setText(config['Settings']['Base delay']),
        self.ui.LE_random_multi.setText(config['Settings']['Random mult']),
        self.ui.LE_tapping_delay.setText(config['Settings']['Tapping delay']),
        self.ui.LE_quiz_timeout.setText(config['Settings']['Quiz timeout']),
        self.ui.LE_skip_chance.setText(config['Settings']['Skip chance']),
        self.ui.LE_night_delay.setText(config['Settings']['Night base delay']),
        self.ui.LE_reading_delay.setText(config['Settings']['Reading delay']),

        self.ui.CB_beep.setChecked(config.getboolean('CheckBoxes', 'Beep'))
        self.ui.CB_night_mode.setChecked(config.getboolean('CheckBoxes', 'Night mode'))
        self.ui.CB_Emulate_reading.setChecked(config.getboolean('CheckBoxes', 'Emulate reading'))
        
    def SaveSettings(self):
        config = configparser.ConfigParser()

        config['Dirs'] = {
            "Log Directory": self.log_dir,
            "Answers Directory": self.answ_dir,
        }


        config['Settings'] = {
            "Nickname": self.nickname,
            "Check timeout": self.ui.LE_check_timeout.text(),
            "Base delay": self.ui.LE_delay_after_detecting.text(),
            "Random mult": self.ui.LE_random_multi.text(),
            "Tapping delay": self.ui.LE_tapping_delay.text(),
            "Quiz timeout": self.ui.LE_quiz_timeout.text(),
            "Skip chance": self.ui.LE_skip_chance.text(),
            "Night base delay": self.ui.LE_check_timeout.text(),
            "Night random mult": self.ui.LE_night_delay.text(),
            "Reading delay": self.ui.LE_reading_delay.text(),
        }

        config['CheckBoxes'] = {
            "Beep": str(self.ui.CB_beep.isChecked()),
            "Night mode": str(self.ui.CB_night_mode.isChecked()),
            "Emulate reading": str(self.ui.CB_Emulate_reading.isChecked()),
        }
        config.write(open('settings.ini', 'w'))

    def OpenLog(self):
        temp = QtWidgets.QFileDialog.getOpenFileName()[0]
        if temp != '':
            self.log_dir = temp

    def OpenAnswers(self):
        temp = QtWidgets.QFileDialog.getOpenFileName()[0]
        if temp != '':
            self.answ_dir = temp

    def WriteNewQuestion(self, Question):
        file = open('new_questions.txt', 'a')
        file.write(Question + "\n")

    def FindAnswer(self, Question):
        file = open(self.answ_dir, 'r')
        lines = file.readlines()
        for line in lines:
            if Question in line:
                ind = line.index('%') + 1
                return line[ind:]
        return 0

    def Check(self):
        line = self.ChatlogLines[len(self.ChatlogLines)-1]
        if '!' in line:
            return None

        if 'сохранка карты' in line:
            line = self.ChatlogLines[len(self.ChatlogLines) - 2]


        try: ind = line.index("[Викторина]") + 12
        except ValueError:
            return None

        question = line[ind:].strip()
        print(question)
        answer = self.FindAnswer(question)
        print(answer)
        if answer != 0:
            answer = answer.strip()
            sleep(self.delay(question))
            self.Tap('t', answer, int(self.ui.LE_tapping_delay.text())/1000)
            print('Tapped')
            self.checkWin()
        else:
            self.WriteNewQuestion(question)

    def StartBtn_clicked(self):
        if self.ui.StartBTN.text() == 'Start':
            self.reading_thread = Thread(target=self.SrartReading, name="Reading Thread")
            self.timer_thread = Thread(target=self.StartTimer, name="Timer Thread")

            self.ui.StartBTN.setText('Stop')
            self.reading_thread.start()
        else:
            self.ui.StartBTN.setText('Start')
            sleep(0.5)

    def SrartReading(self, path = log_dir):
        previous_lines = []
        while self.ui.StartBTN.text() == 'Stop':
            file = open(self.log_dir)
            lines = file.readlines()

            if previous_lines != lines:
                previous_lines = lines
                self.ChatlogLines = lines
                print(lines[len(lines)-1])
                if not self.timer_thread.is_alive():
                    self.timer_thread.start()
                self.Check()

            sleep(int(self.ui.LE_check_timeout.text())/1000)

    def StartTimer(self):
        ahk = AHK()
        while self.ui.StartBTN.text() == 'Stop':

            line = ""

            for l in self.ChatlogLines:
                if ('[Викторина]' in l) and not("!" in l):
                    line = l

            if line != '':

                hour = int(line[1:3])
                minute = int(line[4:6])
                second = int(line[7:9])

                current_time = strftime('[%H:%M:%S]', localtime())

                current_hour = int(current_time[1:3])
                current_minute = int(current_time[4:6])
                current_second = int(current_time[7:9])

                timeToNext_h = current_hour - hour
                timeToNext_m = current_minute - minute
                timeToNext_s = current_second - second

                time_int = (int(self.ui.LE_quiz_timeout.text())//1000) - (timeToNext_h * 3600 + timeToNext_m*60 + timeToNext_s)

                if bool(self.ui.CB_beep.isChecked()):
                    if time_int == 60:
                        ahk.sound_play('source/beep.mp3')
                        sleep(1.5)
                    elif time_int == 10:
                        ahk.sound_play('source/beep.mp3')
                        ahk.sound_play('source/beep.mp3')
                        sleep(1.5)

                if time_int >= 0:
                    time_str = str(time_int // 60) + ':' + str(time_int % 60)
                    self.cur_time_str = time_str
                    self.ui.lcd_timer.display(time_str)
                sleep(0.05)










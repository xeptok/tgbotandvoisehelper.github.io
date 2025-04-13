
import random #импортировали рандомайзер
import speech_recognition as sr  #мы импортировали библиотеку,sr это название библиотеки
import pyttsx3 #импорт библиотеки
import datetime  #импорт библиотеки
from fuzzywuzzy import fuzz  #импорт библиотеки, неполный
from pyowm import OWM
from pyowm.utils.config import get_default_config
from os import system
import sys
import webbrowser
from psutil import virtual_memory as memoryfrom
import psutil
import platform
import wmi
import threading
from PyQt5 import QtWidgets,QtCore
import threading
import interface


owm_token = 'f47da0f2aef4fec305ea72336040dc0a'   #токен профиля на сайте погоды

class Assistant(QtWidgets.QMainWindow, interface.Ui_MainWindow, threading.Thread):   #создали класс
    def __init__(self):   # конструктор класса, обязательно с двумя нижними
        super().__init__()
        self.setupUi(self)
        self.btnStart.clicked.connect(self.start_thread)
        self.btnStop.clicked.connect(self.stop_thread)
        self.working = False

        #Глобальные переменные
        self.rec = sr.Recognizer()                        #\
        self.engine = pyttsx3.init()                      # } как будут записываться те или иные данные чтобы много не писать
        self.voices = self.engine.getProperty('voices')   #/
        self.assistantVoice = 'Artemiy' #голос озвучки
        self.myCity = 'ростов-на-дону'   #город
        self.names=['артем', 'артемий', 'ксеноморф', 'помощник', 'артём'] #разные обращения
        self.timeCMD = ['скажи время', 'сколько времени', 'который час', 'текущее время'] #команды на время
        self.ndels = ['ладно', 'ну', 'допустим', 'короче', 'пожалуйста'] # слова которые будут сбивать помощника
        self.cmds = {
            ('скажи время', 'который час', 'текущее время', 'время'): self.time,   #команды для запуска,пробелы для понимания команд
            ('привет','здравствуй','здарова ботяра'): self.hello,  # команды для запуска приветствия
            ('расскажи погоду', 'какая погода', 'погоду','какая сейчас погода'): self.weather, #команды для запуска погоды
            ('пока', ' вырубись', 'офнись'): self.quit, #команды для выключения бота
            ('бай бай', 'выбури компьютер', 'я спать'): self.shut, #команды для выключения компа,ноута
            ('перезагрузи', 'перезагрузи комп'): self.res, #команды для перезагрузки с подтверждением
            ('руина', 'руинь', 'делай'): self.rest, #команды для руина
            ('добавь задачу', 'добавь заметку', 'запиши задачу', 'запиши заметку'): self.task_planner, #команды для такс планера
            ('прочитай задачи', 'прочитай заметки'): self.task_list, #команды для запуска озвучки задач
            ('удали задачи', 'удали заметки', 'удали заметку', 'удали задачу'): self.task_cleaner, #команды для удаления задач
            ('память', 'количество памяти', 'сколько памяти', 'заполнение памяти'): self.disk_usage, #команды для проверки памяти
            ('данные системы', 'система', 'информация о системе'):self.system_info,

                    }

    def listen(self):   #фиганули функцию, для того чтобы программа распознавала голос
        text = ''   #наш n-ный текст
        with sr.Microphone() as source:  #использовали микрофон и вывели пользователю информацию на экран
            print('Скажите что-нибудь...')  #после вывода на экран можно говорить слова
            self.rec.adjust_for_ambient_noise(source) #приглушили звук с микрофона
            audio = self.rec.listen(source) #аудио-это звук из микрофона
            try:
                text = self.rec.recognize_google(audio,language = 'ru-RU') #текст будет распозноваться с помощью гугла? на русском языке
                text = text.lower()   #все буквы опускаются до строчного значения
            except sr.UnknownValueError:  #пропускаем непонятную ошибку
                pass

            if text != '':
                item = QtWidgets.QListWidgetItem()
                item.setTextAlignment(QtCore.Qt.AlignRight)
                item.setText('Вы: ' + '\n' + text)
                self.console.addItem(item)
                self.console.scrollToBottom()

            print(text)  #выводим текст
            return text  #возвращаем текст

    def cleaner(self,text):  #чистильщик от слов сбивающих работу
        cmd = ''
        for name in self.names: #проверка на обращение именно к помощнику
            if text.startswith(name):  #если сначало произносится его имя значит обращение к нему
                cmd = text.replace(name, '').strip()


        for i in self.ndels: # замена
            cmd = cmd.replace(i,'').strip() #замена слов паразитов на пустоту
            cmd = cmd.replace('  ',' ') #замена двух пробелов на один

        return cmd #возвращение cmd
    def recognizer(self): #выводит или говорит обработанный текст
        text = self.listen()
        cmd = self.cleaner(text)

        if cmd.startswith(('открой', 'запусти', 'найди', 'зайди на')):
            self.open(text)

        for tasks in self.cmds:
            for task in tasks:
                if fuzz.ratio(task,cmd) >= 80:   #проверка слов на совпадение на 80%
                    self.cmds[tasks]()
                    break

    def talk(self, speech):
        self.engine.setProperty('voice', 'ru')  # голос озвучки
        self.engine.setProperty('rate', 150)    # скорость речи
        self.engine.setProperty('volume',0.7)   #громкость озвучки
        self.engine.setProperty('stress_marker',True) # ударения

        for voice in self.voices:
            if voice.name == self.assistantVoice:   #если голос озвучки совпадает с указанным то
                self.engine.setProperty('voice',voice.id)

        if speech != '':
            item = QtWidgets.QListWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignLeft)
            item.setText('Артём: ' + '\n' + speech)
            self.console.addItem(item)
            self.console.scrollToBottom()

        self.engine.say(speech)
        self.engine.runAndWait() #"запускаем" речь
        print(speech)

    def time(self):    #функция для показа времени
        now = datetime.datetime.now() # показали текущее время
        text = 'Cейчас ' + str(now.hour) + ":" + str(now.minute)  #текущее время
        self.talk(text)    # говорит текущее время

    def hello(self):    #фразы приветствия, выбор рандомный
        text = ['Привет, чем могу помочь?',
                'Я могу заруинить тебе игру если забудешь меня выключить',
                'Здарова'
                ]
        say = random.choice(text)
        self.talk(say)

    def weather(self):  #все связанное с погодой
        confdict = get_default_config()
        confdict['language'] = 'ru'   #язык
        owm = OWM(owm_token, confdict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(self.myCity)
        weather = observation.weather
        temp = weather.temperature('celsius')['temp']  #в чем измеряется температура, реально
        feels = weather.temperature('celsius')['feels_like'] #в чем измеряется температура, как чувствуется
        temp = round(temp)
        feels = round(feels)
        status = weather.detailed_status
        wind = weather.wind()['speed']
        humidity = weather.humidity

        text = 'В городе ' + self.myCity + ' сейчас ' + str(status) + "\nТемпература " +\
           str(temp) + 'градусов по цельсию' + '\nВлажность составляет ' + str(humidity) +\
            '%' + '\nСкорость ветра ' + str(wind) + ' метров в секунду'  #текст погоды

        self.talk(text)

    def quit(self):   #функция выключения помощника
        text = ['пока',
                'увидимся',
                'до встречи нубик!',
                'БАЙ БАЙ',
                ''
                ]
        say = random.choice(text) #говорит рандомную фразу
        self.talk(say)
        self.engine.stop()
        sys.exit()

    def shut(self):   #выключение системы с подтверждением
        self.talk('объяснись?!')
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить')>60) or (fuzz.ratio(text,'подтверждаю')>60):
            self.talk('действие подтвержденно')
            system('shutdown /s /f /t 10 /c"выключаюсь"')
            self.quit()
        elif fuzz.ratio(text,'отмена')>60:
            self.talk('действие отменено')
        else:
            self.talk('давай начинай праздновать')


    def res(self): #перезагрузка с подтверждением
        self.talk('объяснись?!')
        text = self.listen()
        print(text)
        if (fuzz.ratio(text, 'подтвердить')>60) or (fuzz.ratio(text,'подтверждаю')>60):
            self.talk('действие подтвержденно')
            system('shutdown /r /f /t 10 /c"x"')
            self.quit()
        elif fuzz.ratio(text,'отмена')>60:
            self.talk('действие отменено')
        else:
            self.talk('давай начинай праздновать')

    def rest(self):   #                    !!!СИСТЕМА РУИНА!!!
        self.engine.stop()
        system('shutdown /r /f')

    def open(self, task):   #функция ссылок
        links = {
            ('YTE', 'ютуб', 'ютюб', 'ютьюб', 'youtube'):'https://www.youtube.com/',
            ('GGL', 'гугл', ' гугел', 'google'):'https://google.com',
            ('RR', 'рр', 'рири', 'р', 'r'): 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            ('WAT', 'мазохизм', 'боль'): 'https://warthunder.com/ru/',
            ('TW', 'твитч', 'твич', 'twitch'): 'https://www.twitch.tv/',
            ('MTW', 'лучший стример', 'стримики', 'стрим'): 'https://www.twitch.tv/xeptok',
            ('крюга','CrewGTw', 'крюгу'): 'https://www.youtube.com/@CrewGTW',
        }
        if 'и' in task:
            task = task.replace('и', '').replace('  ', '')
        task = task.split()
        for t in task:
            for vals in links:
                for word in vals:
                    if fuzz.ratio(word, t) > 75:
                        webbrowser.open(links[vals])
                        self.talk('открываю', + t)
                        break

    def task_planner(self):
        self.talk("Что добавить список задач?")
        task = self.listen()
        file = open('To-do-list.txt', 'a', encoding='utf-8')
        text = task+ '\n'
        file.write(text)
        file.close()
        self.talk(f'Задача {task} добавлена в список задач!')

    def task_list(self):
        try:
            file = open('To-do-list.txt', 'r', encoding='utf-8')
            tasks = file.read()
            file.close()
            if tasks == '':
                self.talk('Фаил пустой')
            else:
                text = 'Список задач:\n' + tasks
                self.talk(text)
        except:
            self.talk('Задач нет')

    def task_cleaner(self):
        file = open('To-do-list.txt', 'w', encoding='utf-8')
        file.write('')
        file.close()
        self.talk('Задачи удалены')

    def disk_usage(self):
        total, used, free, percent = psutil.disk_usage('/')
        total = total // (2**30)
        used = used // (2**30)
        free = free // (2**30)
        percent = round(percent)
        text = 'Всего ' + str(total) + ' гигабайт используется ' + str(used) + \
            ' гигабайт свободно ' + str(free) + ' Диск заполнен на ' + str(percent) + ' процентов'
        self.talk(text)

    def system_info(self):
        text = ''
        os_name = platform.system() + ' ' + platform.release()
        text += 'Операционная систвема: ' + os_name + '\n'

        proc_name = platform.processor()
        proc_cores = psutil.cpu_count(logical=False)
        proc_freq = psutil.cpu_freq().current
        text += 'Процессор: ' + proc_name +'\n'
        text += 'Количество ядер:' + str(proc_cores) +'\n'
        text += 'Частота процессора:' +str(proc_freq) + '\n'

        mem_info = psutil.virtual_memory()
        mem_total = round(mem_info.total / 2**20)
        mem_used = round(mem_info.used / 2**20)
        text += 'Оперативная память: Всего ' + str(mem_total) + ' МБ, Используется ' + \
            str(mem_used) + 'МБ\n'

        w = wmi.WMI(namespace='root\cimv2')
        gpu_info = w.query('SELECT * FROM Win32_VideoController')[0]
        gpu_name = gpu_info.name
        text += 'Видеокарта: ' +gpu_name+ '\n'
        hdd_info = psutil.disk_usage('/')
        hdd_free = round(hdd_info.free / 2**30)
        text += 'На жестком диске свободно '+str(hdd_free)+ 'ГБ\n'
        self.talk(text)


    def stop_thread(self):
        self.working = False
        self.quit()

    def start_thread(self):
        try:
            self.hello()
            self.working = True
            self.thread = threading.Thread(target=self.main)
            self.thread.start()
        except Exception as e:
            print('Error: ', e)
            print('Type: ', type(e))
            print('Traceback', sys.exc_info()[2])

    def main(self):
        while self.working:
            try:
                self.recognizer()
            except Exception as ex:
                print(ex)


if __name__ == '__main__':
    try:
        app = QtWidgets.QApplication(sys.argv)
        window = Assistant()
        window.show()
        sys.exit(app.exec_())
    except Exception as e:
        print('Error: ', e)
        print('Type: ', type(e))
        print('Traceback', sys.exc_info()[2])


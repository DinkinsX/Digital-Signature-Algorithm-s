import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Sign_ui import Ui_HASHS
from math import gcd
from miller import *

import sys
import math
import random
import rsaAlg
import hashlib
import DiffHell_prog
import Elgamal_prog
import Shamir_prog
import sign
import key

'''ГЛАВНОЕ ОКНО С ВЫБОРОМ АЛГОРИТМОВ'''
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_HASHS()
        self.ui.setupUi(self)
        self.ui.loadFile.clicked.connect(self.loadFileFunc)
        self.ui.SignFile.clicked.connect(self.downLoadSignFunc)

        self.ui.pushButton.clicked.connect(self.checkSign)
        self.ui.generateRSA.clicked.connect(self.RSA)
        self.ui.generateEl.clicked.connect(self.ElGamal)
        self.ui.generationDSA.clicked.connect(self.DSA)

        self.ui.action.triggered.connect(self.info)
        self.ui.action_2.triggered.connect(self.saveKeys)
        self.ui.action_3.triggered.connect(self.loadKeys)
        
        self.ui.butClearEl.clicked.connect(self.butClearEl)
        self.ui.butClearRSA.clicked.connect(self.butClearRSA)
        self.ui.clearDSA.clicked.connect(self.butClearDSA)

        self.ui.lineInfo.setText('Ожидается загрузка файла...')
        self.lenKey = 50

    def RSA(self):
        try:
            p = self.ui.pRSA.text()
            q = self.ui.qRSA.text()
            if p == '' or q == '':
                p = rsaAlg.generation_of_a_prime_number()
                q = rsaAlg.generate_second_number(p)
            else:
                pCheck = rsaAlg.TEST(int(p), 50)
                qCheck = rsaAlg.TEST(int(q), 50)
                if pCheck == False or qCheck == False:
                    self.mbox('p и q не являются простыми.')
                    return
                p = int(p)
                q = int(q)

            if p > q:
                tmp = p
                p = q
                q = tmp

            N = p*q      
            d = (p-1)*(q-1)
            s = rsaAlg.calculating_a_mutually_prime_number(d)
            e = rsaAlg.findReverseToE(s,d)
    
            self.ui.dRSA.setText(str(s))
            self.ui.pRSA.setText(str(p))
            self.ui.qRSA.setText(str(q))
            self.ui.nRSA.setText(str(N))
            self.ui.cRSA.setText(str(e))
            
        except:
            self.mbox('Произошла ошибка генерации ключей.\nПроверьте входные данные!')


    def ElGamal(self):
        try:
            p = self.ui.pEl.text()
            q = self.ui.qEl.text()
            if p == '' or q == '':
                p = rsaAlg.generation_of_a_prime_number_for_diff()
                while True:
                    q = rsaAlg.generation_of_a_prime_number_for_diff()
                    if DiffHell_prog.modular_pow(q, p - 1, p) == 1:
                        break
            else:
                pCheck = rsaAlg.TEST(int(p), 50)
                qCheck = rsaAlg.TEST(int(q), 50)
                if pCheck == False or qCheck == False:
                    self.mbox('p и q не являются простыми.')
                    return
                p = int(p)
                q = int(q)

            x, y = Elgamal_prog.generation_c_d(self.lenKey, int(p), int(q))
            self.ui.pEl.setText(str(p))
            self.ui.qEl.setText(str(q))
            self.ui.xEl.setText(str(x))
            self.ui.yEl.setText(str(y))     


        except:
            self.mbox('Произошла ошибка генерации ключей.\nПроверьте входные данные!')


    def DSA(self):
        loop = True
        
        while loop:
            k = random.randrange(2**(863), 2**(864))
            q = generateLargePrime(160)
            p = (k * q) + 1
            while not (isPrime(p)):
                k = random.randrange(2**(863), 2**(864))
                q = generateLargePrime(160)
                p = (k * q) + 1
            L = p.bit_length()
            t = random.randint(1, p-1)
            g = key.squareAndMultiply(t, (p-1) // q, p)
            
            if(L==1024 and L%64 == 0 and (gcd(p-1,q)) > 1 and key.squareAndMultiply(g,q,p) == 1):
                loop = False          
                a = random.randint(2,q-1)
                h = key.squareAndMultiply(g,a,p)
                self.ui.pDSA.setText(str(p)) 
                self.ui.qDSA.setText(str(q))
                self.ui.gDSA.setText(str(g))
                self.ui.xDSA.setText(str(h))
                self.ui.yDSA.setText(str(a))    

  
    def checkSign(self):
        self.mbox('Если поле пустое, подпись будет загружена\nиз файла signatured...txt')
        try:
            typeHash = str(self.ui.comboBoxShiphr.currentText())
            if typeHash == "RSA": 
                y = self.ui.lineHash.text()
                d = int(self.ui.dRSA.text())
                N = int(self.ui.nRSA.text())
                signKey = self.ui.lineSign.text()
                if signKey == '':
                    file = open('signaturedRSA.txt', 'r')
                    textFile = file.read()
                    file.close()
                    self.ui.lineSign.setText(textFile)
                    self.mbox('Подпись загружена.')
                signKey = int(self.ui.lineSign.text())

                signGet = DiffHell_prog.modular_pow(signKey, d, N)
                if hex(signGet)[2:] == y:
                    self.ui.lineInfo.setText('Подпись валидна')
                else:
                    self.ui.lineInfo.setText('Подпись невалидна')

            elif typeHash == "DSA": 
                p=int(self.ui.pDSA.text())
                q=int(self.ui.qDSA.text())
                g=int(self.ui.gDSA.text())
                h=int(self.ui.xDSA.text()) 
                signKey = self.ui.lineSign.text()
                if signKey == '':
                    file = open('signaturedDSA.txt', 'r')
                    textFile = file.read()
                    file.close()
                    self.ui.lineSign.setText(textFile)
                    self.mbox('Подпись загружена.')
                    signKey = self.ui.lineSign.text()

                c1, c2 = signKey.split(' ')
                c1, c2 = int(c1), int(c2)
                hasher = "0x" + self.ui.lineHash.text()
                t1 = int(hasher,0)

                inverseC2 = sign.computeInverse(c2,q)
                t1 = (t1*inverseC2)%q
                
                t2 = sign.computeInverse(c2,q)
                t2 = (t2*c1)%q
                
                valid1 = sign.squareAndMultiply(g,t1,p)
                valid2 = sign.squareAndMultiply(h,t2,p)
                valid = ((valid1*valid2)%p)%q
                if(valid == c1):
                    self.ui.lineInfo.setText('Подпись валидна')
                else:
                    self.ui.lineInfo.setText('Подпись невалидна')

            else:
                y = int(self.ui.yEl.text())
                p = int(self.ui.pEl.text())
                q = int(self.ui.qEl.text())
                h = self.ui.lineHash.text()

                signKey = self.ui.lineSign.text()
                if signKey == '':
                    file = open('signaturedEl.txt', 'r')
                    textFile = file.read()
                    file.close()
                    self.ui.lineSign.setText(textFile)
                    self.mbox('Подпись загружена.')
                    signKey = self.ui.lineSign.text()

                r, s = signKey.split(' ')
                r, s = int(r), int(s)
                if (DiffHell_prog.modular_pow(y, r, p) * DiffHell_prog.modular_pow(r,s,p)) % p == DiffHell_prog.modular_pow(q, int(h, 16), p):
                    self.ui.lineInfo.setText('Подпись валидна')
                else:
                    self.ui.lineInfo.setText('Подпись невалидна')


        except:
            self.mbox('Произошла ошибка проверки подписи.\nПроверьте входные данные!')


    def downLoadSignFunc(self):
        try:
            typeHash = str(self.ui.comboBoxShiphr.currentText())
            if typeHash == "RSA":
                hashText = self.ui.lineHash.text()
                N = int(self.ui.nRSA.text())
                e = int(self.ui.cRSA.text())
                signKey = pow(int(hashText, 16), e, N)
                self.ui.lineSign.setText(str(signKey))

                file = open('signaturedRSA.txt', 'w+')
                file.write(self.ui.lineSign.text())
                file.close()   
                self.mbox('Подпись находится в файле signaturedRSA.txt')    
                self.ui.lineInfo.setText('Подпись получена, вы можете проверить её прямо сейчас нажав на кнопку ниже.') 
            
            elif typeHash == "DSA":
                p=int(self.ui.pDSA.text())
                q=int(self.ui.qDSA.text())
                g=int(self.ui.gDSA.text())
                a=int(self.ui.yDSA.text())                 
                loop = True
                while loop:
                    r = random.randint(1,q-1)
                    c1 = sign.squareAndMultiply(g,r,p)
                    c1 = c1%q
                    hasher = "0x" + self.ui.lineHash.text()
                    hexOut = int(hasher,0)
                    c2 = hexOut + (a*c1)
                    Rinverse = sign.computeInverse(r,q)
                    c2 = (c2*Rinverse)%q
                    
                    if(c1 != 0 and c2 != 0):
                        loop = False
                
                self.ui.lineSign.setText(str(c1) + ' ' + str(c2))
                file = open('signaturedDSA.txt', 'w+')
                file.write(self.ui.lineSign.text())
                file.close()   
                self.mbox('Подпись находится в файле signaturedDSA.txt')    
                self.ui.lineInfo.setText('Подпись получена, вы можете проверить её прямо сейчас нажав на кнопку ниже.') 

            else:
                p = int(self.ui.pEl.text())
                q = int(self.ui.qEl.text())
                x = int(self.ui.xEl.text())
                hashText = self.ui.lineHash.text()
                while True:
                    k = random.randint(1, p - 1)
                    if Shamir_prog.egcd(k, p - 1)[0] == 1:
                        break
            
                r = DiffHell_prog.modular_pow(q, k, p)
                u = (int(hashText, 16) - x * r) % (p - 1)
                s = (Shamir_prog.invert(k, p - 1) * u) % (p - 1)
                self.ui.lineSign.setText(str(r) + ' ' + str(s))

                file = open('signaturedEl.txt', 'w+')
                file.write(self.ui.lineSign.text())
                file.close()   
                self.mbox('Подпись находится в файле signaturedEl.txt')    
                self.ui.lineInfo.setText('Подпись получена, вы можете проверить её прямо сейчас нажав на кнопку ниже.') 

        except:
            self.mbox('Произошла ошибка генерации подписи.\nПроверьте входные данные!')


    def loadFileFunc(self):
        try:
            inputPath = self.get_open_file_path()

            if inputPath == "":
                self.mbox('Вы не выбрали файл.')
                return

            typeHash = str(self.ui.comboBoxShiphr.currentText())
            if typeHash == "DSA":
                hashOut = sign.shaHash(inputPath)
                self.ui.lineHash.setText(hashOut) 
                self.ui.lineInfo.setText('Хэш файла получен, ожидаются ключи. Сгенерируйте или загрузите свои.') 
                self.ui.label_17.setText('Хэш SHA1:')
                self.mbox('Хэш получен.')
                
            else:
                m = hashlib.md5()
                with open(inputPath, 'rb') as f:
                    while True:
                        data = f.read(8192)
                        if not data:
                            break
                        m.update(data)

                self.ui.lineHash.setText(m.hexdigest()) 
                self.ui.lineInfo.setText('Хэш файла получен, ожидаются ключи. Сгенерируйте или загрузите свои.') 
                self.ui.label_17.setText('Хэш MD5:')
                self.mbox('Хэш получен.')

        
        except:
            self.mbox("Произошла ошибка кодировки файла.\nПопробуйте снова или загрузите\nдругой файл.")


    def saveKeys(self):
        try:
            typeHash = str(self.ui.comboBoxShiphr.currentText())
            if typeHash == "RSA":
                self.mbox('Ключи сохраняются в виде: "d N c"\nВ файле KeysRSA.txt')
                if self.ui.dRSA.text() == '' or self.ui.nRSA.text() == '' or self.ui.cRSA.text() == '':
                    self.mbox("Данные отсутствуют")
                    return
                
                file = open('keysRSA.txt', 'w+')
                file.write(self.ui.dRSA.text() + ' ' + self.ui.nRSA.text() + ' ' + self.ui.cRSA.text())
                file.close()
                self.mbox('Ключи сохранены.')

            elif typeHash == "DSA":
                self.mbox('Ключи сохраняются в виде: "p q g h"\nВ файле KeysDSA.txt')
                if self.ui.pDSA.text() == '' or self.ui.qDSA.text() == '' or self.ui.gDSA.text() == '' or self.ui.xDSA.text() == '':
                    self.mbox("Данные отсутствуют")
                    return

                file = open('keysDSA.txt', 'w+')
                file.write(self.ui.pDSA.text() + ' ' + self.ui.qDSA.text() + ' ' + self.ui.gDSA.text() + ' ' + self.ui.xDSA.text())
                file.close()   
                self.mbox('Ключи сохранены.') 

            else:
                self.mbox('Ключи сохраняются в виде: "p q y"\nВ файле KeysEl.txt')
                if self.ui.pEl.text() == '' or self.ui.qEl.text() == '' or self.ui.yEl.text() == '':
                    self.mbox("Данные отсутствуют")
                    return 

                file = open('keysEl.txt', 'w+')
                file.write(self.ui.pEl.text() + ' ' + self.ui.qEl.text() + ' ' + self.ui.yEl.text())
                file.close()    
                self.mbox('Ключи сохранены.')         

        except:
            self.mbox('Произошла ошибка сохранения.')


    def loadKeys(self):
        try:
            typeHash = str(self.ui.comboBoxShiphr.currentText())
            if typeHash == "RSA":   
                self.mbox('Ключи загружаются в виде: "d N c"\nВ файле KeysRSA.txt') 
                file = open('keysRSA.txt', 'r')
                textFile = file.read()
                file.close()

                listKeys = textFile.split()
                self.ui.dRSA.setText(listKeys[0])
                self.ui.nRSA.setText(listKeys[1])
                self.ui.cRSA.setText(listKeys[2])
                self.mbox('Ключи загружены.')

            elif typeHash == "DSA":
                self.mbox('Ключи загружаются в виде: "p q g h"\nВ файле KeysDSA.txt')
                file = open('keysDSA.txt', 'r')
                textFile = file.read()
                file.close()

                listKeys = textFile.split()
                self.ui.pDSA.setText(listKeys[0])
                self.ui.qDSA.setText(listKeys[1])
                self.ui.gDSA.setText(listKeys[2])
                self.ui.xDSA.setText(listKeys[3])
                self.mbox('Ключи загружены.')

            else:
                self.mbox('Ключи загружаются в виде: "p q y"\nВ файле KeysEl.txt') 
                file = open('keysEl.txt', 'r')
                textFile = file.read()
                file.close()

                listKeys = textFile.split()
                self.ui.pEl.setText(listKeys[0])
                self.ui.qEl.setText(listKeys[1])
                self.ui.yEl.setText(listKeys[2])
                self.mbox('Ключи загружены.')

        except:
            self.mbox('Произошла ошибка загрузки.')


    def info(self):
        self.mbox('1. Выберите алгоритм в верхнем выпадающем окне\n\n'
                  '2. Загрузите файл хэш которого хотите получить\n\n'
                  '3. Сгенерируйте или загрузите ключи. P и Q можно\n'
                  'ввести вручную. Если поля будут пустыми, P и Q сгенерируются автоматически\n\n'
                  '4. Получите ЭП. При нажатии ЭП сохранятся в файл signatured.txt\n\n'
                  '5. Проверьте ЭП. Если поле будет пустым, ЭП загрузится из файла signatured.txt\n\n'
                  'Прим. Если выбрать RSA или Эль-Гамаля - хэш MD5, иначе SHA1')         


    def butClearEl(self):
        self.ui.pEl.setText('')
        self.ui.qEl.setText('')
        self.ui.xEl.setText('')
        self.ui.yEl.setText('')
        self.ui.lineSign.setText('')


    def butClearRSA(self):
        self.ui.pRSA.setText('')
        self.ui.qRSA.setText('')
        self.ui.dRSA.setText('')
        self.ui.nRSA.setText('')
        self.ui.cRSA.setText('')  
        self.ui.lineSign.setText('')


    def butClearDSA(self):
        self.ui.pDSA.setText('') 
        self.ui.qDSA.setText('')
        self.ui.gDSA.setText('')
        self.ui.yDSA.setText('')
        self.ui.xDSA.setText('')   
        self.ui.lineSign.setText('')


    def get_open_file_path(self):
        return QFileDialog.getOpenFileName(self, "Открыть файл")[0]


    def mbox(self, body, title='Уведомляю вас'):
        dialog = QMessageBox(QMessageBox.Information, title, body)
        dialog.exec_()


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())
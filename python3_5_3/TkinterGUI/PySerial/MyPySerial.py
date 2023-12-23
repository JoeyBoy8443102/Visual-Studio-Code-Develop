'''
@ author: Joey
@ tools: VSCode
@ content: 實現串列埠通訊主類
@ date: 2023/11/21

'''

import tkinter
from tkinter import ttk
from SerialClass import SerialAchieve

class MainSerial:
    def __init__(self):
        # 定義串口變量
        self.port = None
        self.band = None
        self.check = None
        self.data = None
        self.stop = None
        self.myserial = None
    
        # 初始化視窗
        self.mainwin = tkinter.Tk()
        self.mainwin.title("串列埠調試工具")
        self.mainwin.geometry("600x400")

        # 標籤
        self.label1 = tkinter.Label(self.mainwin, text="串列埠:", font = ("宋體",15))
        self.label1.place(x=5, y=5)
        self.label2 = tkinter.Label(self.mainwin, text="鮑率:", font=("宋體", 15))
        self.label2.place(x=5, y=45)
        self.label3 = tkinter.Label(self.mainwin, text="校驗位:", font=("宋體", 15))
        self.label3.place(x=5, y=85)
        self.label4 = tkinter.Label(self.mainwin, text="數據位:", font=("宋體", 15))
        self.label4.place(x=5, y=125)
        self.label5 = tkinter.Label(self.mainwin,text = "停止位:",font = ("宋體",15))
        self.label5.place(x = 5,y = 165)

        # 文本顯示，清除發布數據
        self.label6 = tkinter.Label(self.mainwin, text="發送數據", font = ("宋體",15))
        self.label6.place(x=230, y=5)

        self.label7 = tkinter.Label(self.mainwin, text="接收數據", font=("宋體", 15))
        self.label7.place(x=230, y=200)

        # ComPort
        self.com1value = tkinter.StringVar()    # 視窗中自帶的文本，創建一個值
        self.combobox_port = ttk.Combobox(self.mainwin, textvariable=self.com1value, width=10, font = ("宋體",13))
        #輸入選定內容
        self.combobox_port["value"] = [""]  # 這裡選定

        self.combobox_port.place(x = 105, y = 5)    # 顯示

        # 鮑率
        self.bandvalue = tkinter.StringVar()    # 視窗中自帶的文本，創建一個值
        self.combobox_band = ttk.Combobox(self.mainwin, textvariable = self.bandvalue, width=10, font = ("宋體",13))
        # 輸入選定內容
        self.combobox_band["value"] = ["4800","9600","14400","19200","38400","57600","115200"]  # 這裡先選定
        self.combobox_band.current(6)   # 默認選中第6個
        self.combobox_band.place(x = 105, y = 45)

        # 校驗位
        self.checkvalue = tkinter.StringVar()   # 視窗中自帶的文本，創建一個值
        self.combobox_check = ttk.Combobox(self.mainwin, textvariable = self.checkvalue, width=10, font = ("宋體",13))
        # 輸入選定內容
        self.combobox_check["value"] = ["無校驗位"]  # 這裡先選定
        self.combobox_check.current(0)  #默認選中第0個
        self.combobox_check.place(x = 105, y = 85)  # 顯示

        # 數據位
        self.datavalue = tkinter.StringVar()    # 視窗中自帶的文本，創建一個值
        self.combobox_data = ttk.Combobox(self.mainwin, textvariable = self.datavalue, width=10, font = ("宋體",13))
        #輸入選定內容
        self.combobox_data["value"] = ["8", "9", "0"]    # 這裡先選定
        self.combobox_data.current(0)   #默認選中第0個
        self.combobox_data.place(x = 105, y = 125)  # 顯示

        # 停止位
        self.stopvalue = tkinter.StringVar()    # 視窗中自帶的文本，創建一個值
        self.combobox_stop = ttk.Combobox(self.mainwin, textvariable=self.stopvalue, width=10, font=("宋體", 13))
        # 輸入選定內容
        self.combobox_stop["value"] = ["1", "0"]  # 這裡先選定
        self.combobox_stop.current(0)  # 默認選中第0個
        self.combobox_stop.place(x=105, y=165)  # 顯示

        # 按鍵顯示，打開串列埠
        self.button_OK = tkinter.Button(self.mainwin, text = "打開串列埠", command=self.button_OK_click,
                                        font = ("宋體",13), width=10, height=1)
        self.button_OK.place(x = 5, y = 210)    #顯示控件

        # 關閉串列埠
        self.button_Cancel = tkinter.Button(self.mainwin, text = "關閉串列埠", command=self.button_Cancel_click,
                                            font = ("宋體",13), width=10, height=1)
        self.button_Cancel.place(x = 120, y = 210)    #顯示控件

        # 清除發送數據
        self.button_Cancel = tkinter.Button(self.mainwin, text="清除發送數據",command=self.button_clcSend_click,
                                            font = ("宋體",13), width=10, height=1)
        self.button_Cancel.place(x = 400, y = 2)    #顯示控件

        # 清除接收數據
        self.button_Cancel = tkinter.Button(self.mainwin, text="清除接收數據",command=self.button_clcRece_click,
                                            font = ("宋體",13), width=10, height=1)
        self.button_Cancel.place(x = 400, y = 197)    #顯示控件

        # 發送按鍵
        self.button_Send = tkinter.Button(self.mainwin, text="發送", command=self.button_Send_click,
                                          font = ("宋體",13), width=6, height=1)
        self.button_Send.place(x = 5, y = 255)  #顯示控件

        # 接收按鍵
        self.button_Send = tkinter.Button(self.mainwin, text="接收", command=self.button_Rece_click,
                                          font = ("宋體",13), width=6, height=1)
        self.button_Send.place(x = 5, y = 310)  #顯示控件


        # 顯示框
        # 實現記事本的功能組件
        self.SendDataView = tkinter.Text(self.mainwin, width = 40, height = 9, font = ("宋體",13))  # text實際上是一個文字編輯器
        self.SendDataView.place(x = 230, y = 35)    #顯示

        self.ReceDataView = tkinter.Text(self.mainwin, width = 40, height = 9, font = ("宋體",13))  # text實際上是一個文字編輯器
        self.ReceDataView.place(x = 230, y = 230)   # 顯示


        # 發送的內容
        test_str = tkinter.StringVar(value="Hello")
        self.entrySend = tkinter.Entry(self.mainwin, width=13, textvariable = test_str, font=("宋體",15))
        self.entrySend.place(x = 80, y = 260)   # 顯示

        # 獲取介面的參數
        self.band = self.combobox_band.get()
        self.check = self.combobox_check.get()
        self.data = self.combobox_data.get()
        self.stop = self.combobox_stop.get()
        print("鮑率:"+self.band)
        self.myserial = SerialAchieve(int(self.band), self.check, self.data, self.stop) # SerialClass.py 實際與Port連接

        # 處理串列埠值
        self.port_list = self.myserial.get_port()
        port_str_list = []  # 用來存儲切割好的串列埠
        for i in range(len(self.port_list)):
            # 將串列埠切割出來
            lines = str(self.port_list[i])
            str_list = lines.split(" ")
            port_str_list.append(str_list[0])
        self.combobox_port["value"] = port_str_list
        self.combobox_port.current(0)   # 默認選中第0個
        
        
    def show(self):
        self.mainwin.mainloop()

    def button_OK_click(self):
        '''
        @ 串口打開函數
        :return: 
        '''
        if self.port == None or self.port.isOpen() == False:
            self.myserial.open_port(self.combobox_port.get())
            print("打開串口成功")
        else:
            pass

    def button_Cancel_click(self):
        self.myserial.delete_port()
        print("關閉串口成功")

    def button_clcSend_click(self):
        self.SendDataView.delete("1.0","end")
    
    def button_clcRece_click(self):
        self.ReceDataView.delete("1.0","end")

    def button_Send_click(self):
        try:
            if self.myserial.port.isOpen() == True:
                print("開始發送數據")
                send_str1 = self.entrySend.get()
                self.myserial.insert(tkinter.INSERT, send_str1 + " ")
                print("發送成功")
            else:
                print("串列埠沒打開")
        except:
            print("發送失敗")
    def button_Rece_click(self):
        try:
            readstr = self.myserial.Read_data()
            self.ReceDataView.insert(tkinter.INSERT, readstr + " ")
        except:
            print("讀取失敗")

if __name__ == '__main__':
    my_ser1 = MainSerial()
    my_ser1.show()
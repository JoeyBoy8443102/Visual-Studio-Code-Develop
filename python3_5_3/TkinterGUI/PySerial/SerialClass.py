'''
@ author: Joey
@ tools: VSCode
@ content: 串口通訊實現類
@ data: 2023/11/21
'''
import serial
import serial.tools.list_ports

class SerialAchieve:
    def __init__(self, band = 115200, check = "無效驗位", data = 8, stop = 1):
        self.port = None
        # 獲取可用串列埠
        self.port_list = list(serial.tools.list_ports.comports())
        assert(len(self.port_list) != 0), "無可用串列埠"

        self.bandRate = band
        self.checkbit = check
        self.databit = data
        self.stopbit = stop

        # 讀寫的數據
        self.read_data = None
        self.write_data = None
    
        pass

    def show_port(self):
        for i in range(0, len(self.port_list)):
            print(self.port_list[i])

    def show_other(self):
        print("鮑率:" + self.bandRate)
        print("校驗位:" + self.checkbit)
        print("數據位:" + self.databit)
        print("停止位:" + self.stopbit)
    
    # 返回串列
    def get_port(self):
        return self.port_list
    
    # 打開串列
    def open_port(self, port): 
        self.port = serial.Serial(port, self.bandRate, timeout = None)

    def delete_port(self):
        if self.port != None:
            self.port.close()
            print("關閉串列埠完成")
        else:
            pass

    def Read_data(self):    # self.port.read(self.port.in_waiting) 表示全部接收串口中的数据
        self.read_data = self.port.read(self.port.in_waiting)   #讀取數據
        return self.read_data.decode("utf-8")
    
    def Write_data(self,data):
        if self.port.isOpen() == False:
            print("串列打開錯誤")
        else:
            self.port.write(data.encode("utf-8"))   # 返回的是寫入的字節數
'''
if __name__ == '__main__':
    myser = SerialAchieve()
    #myser.open_port("COM3")
    myser.delete_port()
    myser.show_port()'''
from aip import AipOcr
# from tkinter import *
import tkinter as tk
from tkinter.messagebox import askyesno
from tkinter.simpledialog import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.scrolledtext import ScrolledText

class App(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.title('OCR-kit-1.0')
        self.master.geometry('400x300+100+100')
        self.master.resizable(False, False)
        self.createWidgets()
        self.pack(side=tk.LEFT, expand=tk.YES, fill=tk.BOTH)

    def createWidgets(self):
        self.text = ScrolledText(self, width=20, height=12)
        self.text.config(font=('微软雅黑', 10, 'bold'))
        self.text.delete(1.0, tk.END)
        self.text.pack(side=tk.TOP, padx=3, pady=3, expand=tk.YES, fill=tk.BOTH)
        f2 = tk.Frame(self)
        self.btnOpen = tk.Button(f2, text='打开图片', command=self.openImg)
        self.btnOpen.pack(side=tk.LEFT, padx=3, pady=3, expand=tk.YES, fill=tk.BOTH)
        self.btnSave = tk.Button(f2, text='保存为txt文件', command=self.saveTxt)
        self.btnSave.pack(side=tk.RIGHT, padx=3, pady=3, expand=tk.YES, fill=tk.BOTH)
        f2.pack(side=tk.BOTTOM, padx=3, pady=3, expand=tk.YES, fill=tk.BOTH)

    def openImg(self):
        if self.text.get(1.0, tk.END) != '\n':
            question = askyesno('是否保存？','检测到文本框中有内容，是否保存该内容？\n'
                                            '不保存将覆盖原有内容，且过程不可逆')
            if question:
                self.saveTxt()
                return '保存成功'
        filename = askopenfilename(title='选择要进行OCR识别的图片',
                                    defaultextension = '.png',
                                    filetypes=[('png格式图片', '.png'),
                                            ('jpg格式图片', '.jpg'),
                                            ('所有文件', '*.*')])
        if filename:
            txt = self.getWord(filename)
            self.btnOpen.config({'text': '请稍后，图片处理中'})
            #self.btnOpen.config(text='请稍后，图片处理中')
            self.btnOpen.config({'state': tk.DISABLED})
            if txt:
                self.text.delete(1.0, tk.END)
                self.text.insert(1.0, txt)
            else:
                self.text.insert(1.0, '未获取到内容')
            self.btnOpen.config({'text': '打开图片'})
            self.btnOpen.config({'state': tk.NORMAL})
        else:
            self.text.insert(1.0, '请选择要输出的图片文件\n')
        
    def saveTxt(self):
        sfilename = asksaveasfilename(title='将图片内文字保存为文本文档',
                                    defaultextension='.txt',
                                    filetypes=[('保存文本', 'txt'),
                                                ('所有文件','*.*')])
        if sfilename:
            stxt = self.text.get(1.0, tk.END)
            try:
                with open(sfilename, 'w') as f:
                    f.write(stxt)
                messagebox.showinfo('提示', '文件保存成功')
            except Exception as e:      #这个绝了！
                messagebox.showinfo('提示', '出错了，可能原因是：{}'.format(str(e)))
        else:
            messagebox.showinfo('提示','未选择文件名称，保存失败')
            
    @staticmethod
    def getWord(filename=''):
        result = ''
        APP_ID = '16330283'
        API_KEY = 'lTzy5Z7UzV7gh2OXNDYfTUum'
        SECRET_KEY = '5nklyDnSUNVi0luWHpmd74PYfuiPKpRS'
        client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        image = open(filename, 'rb').read()
        message = client.basicGeneral(image)
        for i in message.get('words_result'):
            result += i['words']+'\n'
        return result
# main
window = tk.Tk()
app = App(window)
window.mainloop()
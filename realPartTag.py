import os

import PySide2
from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader

dirname = os.path.dirname(PySide2.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path


class MediRecordTagger:
    def __init__(self):
        self.data = []  # 原始数据
        self.sum = 0  # 原始数据总数
        self.num = 0  # 标记的对话序号

        # 加载UI
        self.ui = QUiLoader().load('realPartTag.ui')
        # 打开文件
        self.ui.button_openFile.clicked.connect(self.openFileDialog)
        # 保存标记文件
        self.ui.button_saveFile.clicked.connect(self.saveFile)
        # 按钮跳转到下一个病历对话
        self.ui.button_next_item.clicked.connect(self.dealNextLine)
        # 按钮跳转到上一个病历对话
        self.ui.button_last_item.clicked.connect(self.dealLastLine)
        # 提示框
        self.qmessagebox = QMessageBox()

    '''
    读取文件
    filepath:文件路径
    '''

    def open_file(self, filepath):
        with open(filepath, 'r', encoding="utf8") as f:
            data = f.readlines()
        self.sum = len(data)
        data_eval = []
        for i in range(self.sum):
            data_eval.append(eval(data[i]))
        return data_eval

    def getPartCon(self, part_name, con):
        part_con = ''
        for c in con:
            if c['part'] == part_name:
                part_con = part_con + c['utter'] + '\n'
        return part_con

    def displayUtters(self):
        self.num -= 1
        con = self.data[self.num]['content']
        chiefCp = self.getPartCon('1', con)
        nowH = self.getPartCon('2', con)
        pastH = self.getPartCon('3', con)
        phyExam = self.getPartCon('4', con)
        auxIR = self.getPartCon('5', con)
        preDiag = self.getPartCon('6', con)
        treatOp = self.getPartCon('7', con)

        self.ui.text_chiefCp_utters.setPlainText(chiefCp)
        self.ui.text_nowH_utters.setPlainText(nowH)
        self.ui.text_pastH_utters.setPlainText(pastH)
        self.ui.text_phyExam_utters.setPlainText(phyExam)
        self.ui.text_auxIR_utters.setPlainText(auxIR)
        self.ui.text_preDiag_utters.setPlainText(preDiag)
        self.ui.text_treatOp_utters.setPlainText(treatOp)

        self.ui.text_chiefCp_sm.setText(chiefCp)
        self.ui.text_nowH_sm.setText(nowH)
        self.ui.text_pastH_sm.setText(pastH)
        self.ui.text_phyExam_sm.setText(phyExam)
        self.ui.text_auxIR_sm.setText(auxIR)
        self.ui.text_preDiag_sm.setText(preDiag)
        self.ui.text_treatOp_sm.setText(treatOp)

        self.num += 1

    '''
    按钮打开文件
    '''

    def openFileDialog(self):
        # 生成文件对话框对象
        dialog = QFileDialog()
        # 设置文件过滤器，这里是任何文件，包括目录
        dialog.setFileMode(QFileDialog.AnyFile)
        # 设置显示文件的模式，这里是详细模式
        dialog.setViewMode(QFileDialog.Detail)
        if dialog.exec_():
            fileNames = dialog.selectedFiles()  # 文件名
            filepath = fileNames[0]
            self.data = self.open_file(filepath)
            # self.ui.text_numOfAll.setText(str(self.num + 1) + '/' + str(self.sum))
            self.displayUtters()
            self.num += 1

    # 保存标记文件
    def saveFile(self):
        path = self.ui.text_savePath.text()
        # 文件是否已存在
        if os.path.isfile(path):
            choice = QMessageBox.question(self.ui, '确认',  '是否覆盖原文件？')
            if choice == QMessageBox.Yes:
                pathList = []
                if '\\' in path:
                    pathList = path.split('\\')
                elif '/' in path:
                    pathList = path.split('/')
                print('/'.join(pathList[:-1]))
                if os.path.isdir('/'.join(pathList[:-1])):
                    with open(path, 'w', encoding="utf-8") as f:
                        for i in range(self.num):
                            f.write(str((self.data[i])) + '\n')
            if choice == QMessageBox.No:
                print('请更改文件名')
        # 创建新文件
        else:
            pathList = []
            if '\\' in path:
                pathList = path.split('\\')
            elif '/' in path:
                pathList = path.split('/')
            print('/'.join(pathList[:-1]))
            if os.path.isdir('/'.join(pathList[:-1])):
                with open(path, 'w', encoding="utf-8") as f:
                    for i in range(self.num):
                        f.write(str((self.data[i])) + '\n')

    def updateUtters(self):
        chiefCp = self.ui.text_chiefCp_sm.toPlainText()
        nowH = self.ui.text_nowH_sm.toPlainText()
        pastH = self.ui.text_pastH_sm.toPlainText()
        phyExam = self.ui.text_phyExam_sm.toPlainText()
        auxIR = self.ui.text_auxIR_sm.toPlainText()
        preDiag = self.ui.text_preDiag_sm.toPlainText()
        treatOp = self.ui.text_treatOp_sm.toPlainText()

        self.num -= 1
        self.data[self.num]['summary']['SUM1'] = chiefCp
        self.data[self.num]['summary']['SUM2'] = nowH
        self.data[self.num]['summary']['SUM3'] = pastH
        self.data[self.num]['summary']['SUM4'] = phyExam
        self.data[self.num]['summary']['SUM5'] = auxIR
        self.data[self.num]['summary']['SUM6'] = preDiag
        self.data[self.num]['summary']['SUM7'] = treatOp
        self.num += 1

    # 跳转到下一条病历
    def dealNextLine(self):
        if self.num < self.sum:
            self.updateUtters()
            self.displayUtters()
            # self.ui.text_numOfAll.setText(str(self.num + 1) + '/' + str(self.sum))
            self.num += 1
        else:
            self.qmessagebox.information(self.ui, "提示", "已到达最后一条数据")

    # 跳转到上一条病历
    def dealLastLine(self):
        if self.num > 1:
            self.num -= 2
            self.displayUtters()
            self.num += 1
        else:
            self.qmessagebox.information(self.ui, "提示", "已到达第一条数据")


app = QApplication([])
tagger = MediRecordTagger()
tagger.ui.show()
app.exec_()
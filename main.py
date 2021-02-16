import os
import fitz
import json
import PyPDF2
from time import sleep
import logging

basePath = '/Users/Manda/Seed Co-op Dropbox/IT/Ninox Printing Test'
scriptDirPath = os.path.abspath(os.path.dirname(__file__))

class File():
    
    def __init__(self, fileName):

        self.fileName = fileName
        self.barcode = None
        self.batchNum = None
        self.batchSize = None

    def __repr__(self):
        return f'{self.fileName} -> batchNum: {self.batchNum}, batchSize: {self.batchSize}'

    def extractFileInfo(self):
        fileInfoArr = self.fileName.split('.')[0].split('-')
        try:
            self.batchNum = fileInfoArr[0]
            self.batchSize = int(fileInfoArr[1])
            return True
        except:
            return False

    def checkForBarcode(self, barcodeDirPath):
        barcodeFile = f'{self.batchNum}.png'
        barcodeFiles = os.listdir(barcodeDirPath)
        if barcodeFile in barcodeFiles:
            self.barcode = barcodeFile
            return True
        else:
            return False

    def addBarcodeAndMove(self, inDirPath, outDirPath, barcodeDirPath, barcodeInfo):
        if self.barcode != None:
            inFilePath = f'{inDirPath}/{self.fileName}'
            outFilePath = f'{outDirPath}/{self.fileName}'
            barcodeFilePath = f'{barcodeDirPath}/{self.barcode}'
            x0 = barcodeInfo['X']
            y0 = barcodeInfo['Y']
            x1 = barcodeInfo['X'] + barcodeInfo['W']
            y1 = barcodeInfo['Y'] + barcodeInfo['H']
            barcodeRect = fitz.Rect(x0, y0, x1, y1)

            with fitz.open(inFilePath) as f:
                pageOne = f[0]
                pageOne.insertImage(barcodeRect, filename = barcodeFilePath)
                f.save(outFilePath)

            os.remove(inFilePath)
            os.remove(barcodeFilePath)

    def dupePdfPages(self, inDirPath, outDirPath):
        inPdfPath = f'{inDirPath}/{self.fileName}'
        outPdfPath = f'{outDirPath}/{self.fileName}'

        with open(inPdfPath, 'rb') as inPdf, open(outPdfPath, 'wb') as outPdf:
            pdfReader = PyPDF2.PdfFileReader(inPdf)
            pdfWriter = PyPDF2.PdfFileWriter()

            for i in range(self.batchSize):
                pdfWriter.addPage(pdfReader.getPage(0))

            pdfWriter.write(outPdf)

        os.remove(inPdfPath)

        print(f'completed -> {self}')

class Dir():

    ignoreFiles = ['.DS_Store']
    
    def __init__(self, inDirName, dupeDirName, printDirName, barcodeInfo):
        self.inDirName = inDirName
        self.dupeDirName = dupeDirName
        self.printDirName = printDirName
        self.barcodeInfo = barcodeInfo

        self.inDirPath = f'{basePath}/{inDirName}'
        self.dupeDirPath = f'{basePath}/{dupeDirName}'
        self.printDirPath = f'{basePath}/{printDirName}'
        self.barcodeDirPath = f'{basePath}/barcode'
        
        self.dirFiles = []

    def __repr__(self):
        return f'{self.inDirName} -> {self.dupeDirName} -> {self.printDirName}'

    def processFiles(self):
        self.getDirFiles()
        self.extractDirFilesInfo()
        self.checkDirFilesBarcodes()
        self.addBarcodesAndMove()
        self.dupePdfPages()

    def getDirFiles(self):
        dirFiles = os.listdir(self.inDirPath)
        for file in dirFiles:
            try:
                if file not in self.ignoreFiles:
                    filePath = f'{self.inDirPath}/{file}'
                    fileObj = File(file)
                    self.dirFiles.append(fileObj)
            except Exception as e:
                print(file)
                logException(e)

    def extractDirFilesInfo(self):

        toRemove = []

        for file in self.dirFiles:
            try:
                canExtractFileInfo = file.extractFileInfo()
                if not canExtractFileInfo:
                    toRemove.append(file)
            except Exception as e:
                logException(e)

        for file in toRemove:
            self.dirFiles.remove(file)

    def checkDirFilesBarcodes(self):

        toRemove = []

        for file in self.dirFiles:
            try:
                isBarcode = file.checkForBarcode(self.barcodeDirPath)
                if not isBarcode:
                    toRemove.append(file)

            except Exception as e:
                logException(e)

        for file in toRemove:
            self.dirFiles.remove(file)

    def addBarcodesAndMove(self):
        for file in self.dirFiles:
            try:
                file.addBarcodeAndMove(self.inDirPath, self.dupeDirPath, self.barcodeDirPath, self.barcodeInfo)
            except Exception as e:
                logException(e)

    def dupePdfPages(self):
        for file in self.dirFiles:
            try:
                file.dupePdfPages(self.dupeDirPath, self.printDirPath)
            except Exception as e:
                logException(e)

def logException(e):
    print(f'exception -> {e}')

    logFileName = 'logger.log'
    logFilePath = f'{scriptDirPath}/{logFileName}'

    logging.basicConfig(filename=logFilePath, encoding = 'utf-8', level = logging.DEBUG)
    logging.error(e, exc_info=1)

def main():

    with open(f'{scriptDirPath}/config.json', 'r') as f:
        config = json.load(f)

    prodConfig = config['prodConfig']

    for prodType in prodConfig:
        inDir = prodConfig[prodType]['inDir']
        dupeDir = prodConfig[prodType]['dupeDir']
        printDir = prodConfig[prodType]['printDir']
        barcodeInfo = prodConfig[prodType]['barcodeInfo']
        curDir = Dir(inDir, dupeDir, printDir, barcodeInfo)
        curDir.processFiles()

if __name__ == '__main__':

    print('printing & barcoding script started')

    while True:
        try:
            main()
            sleep(1)
        except Exception as e:
            logException(e)
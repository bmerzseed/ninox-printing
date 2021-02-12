import os
import fitz

class File():
    
    def __init__(self, fileName):

        self.fileName = fileName
        self.barcode = None
        self.batchNum = None
        self.batchSize = None

    def __repr__(self):
        return f'{self.fileName} -> batchNum: {self.batchNum}, batchSize: {self.batchSize}, barcode: {self.barcode}'

    def extractFileInfo(self):
        fileInfoArr = self.fileName.split('.')[0].split('-')
        self.batchNum = fileInfoArr[0]
        self.batchSize = fileInfoArr[1]

    def checkForBarcode(self, barcodeDirPath):
        barcodeFile = f'{self.batchNum}.png'
        barcodeFiles = os.listdir(barcodeDirPath)
        if barcodeFile in barcodeFiles:
            self.barcode = barcodeFile

    def addBarcodeAndMove(self, inDirPath, outDirPath, barcodeDirPath, barcodeInfo):
        if self.barcode != None:
            inFilePath = f'{inDirPath}/{self.fileName}'
            outFilePath = f'{outDirPath}/{self.fileName}'
            barcodeFilePath = f'{barcodeDirPath}/{self.barcode}'
            x0 = barcodeInfo['X']
            y0 = barcodeInfo['Y']
            x1 = barcodeInfo['X'] + barcodeInfo['W']
            y1 = barcodeInfo['Y'] + barcodeInfo['H']
            print(self, f'{x0=}, {y0=}, {x1=}, {y1=}')
            barcodeRect = fitz.Rect(x0, y0, x1, y1)

            with fitz.open(inFilePath) as f:
                pageOne = f[0]
                pageOne.insertImage(barcodeRect, filename = barcodeFilePath)
                f.save(outFilePath)

            # then remove in pdf/ in barcode files

    def dupePdfPages(self):
        pass

class Dir():

    basePath = '/Users/Manda/Seed Co-op Dropbox/IT/Ninox Printing Test'
    scriptDirPath = os.path.abspath(os.path.dirname(__file__))

    ignoreFiles = ['.DS_Store']
    
    def __init__(self, inDirName, dupeDirName, printDirName, barcodeInfo):
        self.inDirName = inDirName
        self.dupeDirName = dupeDirName
        self.printDirName = printDirName
        self.barcodeInfo = barcodeInfo

        self.inDirPath = f'{self.basePath}/{inDirName}'
        self.dupeDirPath = f'{self.basePath}/{dupeDirName}'
        self.printDirPath = f'{self.basePath}/{printDirName}'
        self.barcodeDirPath = f'{self.basePath}/barcode'
        
        self.dirFiles = []

    def __repr__(self):
        return f'{self.inDirName} -> {self.dupeDirName} -> {self.printDirName}'

    def processFiles(self):
        self.getDirFiles()
        self.extractDirFilesInfo()
        self.checkDirFilesBarcodes()
        self.addBarcodesAndMove()

    def getDirFiles(self):
        dirFiles = os.listdir(self.inDirPath)
        for file in dirFiles:
            try:
                if file not in self.ignoreFiles:
                    filePath = f'{self.inDirPath}/{file}'
                    fileObj = File(file)
                    self.dirFiles.append(fileObj)
            except Exception as e:
                logException(e)
                continue

    def extractDirFilesInfo(self):
        for file in self.dirFiles:
            try:
                file.extractFileInfo()
            except Exception as e:
                logException(e):
                    continue

    def checkDirFilesBarcodes(self):
        for file in self.dirFiles:
            try:
                file.checkForBarcode(self.barcodeDirPath)
            except Exception as e:
                logException(e)
                continue

    def addBarcodesAndMove(self):
        for file in self.dirFiles:
            try:
                file.addBarcodeAndMove(self.inDirPath, self.dupeDirPath, self.barcodeDirPath, self.barcodeInfo)
            except Exception as e:
                logException(e)
                continue

    def dupePdfPages(self):
        for file in self.dirFiles:
            try:
                file.dupePdfPages()
            except Exception as e:
                logException(e)
                continue

def logException(e):
    print(e)

def main():

    prodTypes = {
        'sm': {
            'inDir': 'smIn',
            'dupeDir': 'smToDupe',
            'printDir': 'smToPrint',
            'barcodeInfo' : {
                'H': 20,
                'W': 40,
                'X': 10,
                'Y': 25,
            },
        },
        'bk': {
            'inDir': 'bkIn',
            'dupeDir': 'bkToDupe',
            'printDir': 'bkToPrint',
            'barcodeInfo' : {
                'H': 15,
                'W': 30,
                'X': 45,
                'Y': 50,
            },
        }
    }

    for prodType in prodTypes:
        inDir = prodTypes[prodType]['inDir']
        dupeDir = prodTypes[prodType]['dupeDir']
        printDir = prodTypes[prodType]['printDir']
        barcodeInfo = prodTypes[prodType]['barcodeInfo']
        curDir = Dir(inDir, dupeDir, printDir, barcodeInfo)
        curDir.processFiles()
        print(curDir, curDir.dirFiles)

if __name__ == '__main__':
    main()

import os

basePath = '/Users/Manda/Seed Co-op Dropbox/It/Ninox Printing Test'

smPath = f'{basePath}/sm'
bkPath = f'{basePath}/bk'
barPath = f'{basePath}/barcode'

smFiles = os.listdir(smPath)
bkFiles = os.listdir(bkPath)
barFiles = os.listdir(barPath)

fileIgnoreList = ['.DS_Store']

dirArr = [smFiles, bkFiles]
dirType = ['sm', 'bk']

for fileDir, fileType in zip(dirArr, dirType):
    for file in fileDir:
        try:
            fileSplit = file.split('.')[0].split('-')
            batchNum = fileSplit[0]
            batchSize = fileSplit[1]
            
            barcodeFileName = f'{batchNum}.png'
    
            if barcodeFileName in barFiles:
                print('barcode found', barcodeFileName, fileType)
            else:
                print('no barcode', barcodeFileName, fileType)
                continue
            
        except Exception as e:
            if 'file' in file or file in fileIgnoreList:
                print(file)
                continue
            else:
                os.remove(file)
                

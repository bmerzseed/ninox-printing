import os
import fitz

basePath = os.path.abspath(os.path.dirname(__file__))

inPdfFile = '21581-26.pdf'
inBarFile = 'barcode.png'
outFile = 'out.pdf'

inPdfPath = f'{basePath}/{inPdfFile}'
inBarPath = f'{basePath}/{inBarFile}'
outPath = f'{basePath}/{outFile}'

# define position of barcode

barcodeH = 35
barcodeW = 3.6 * barcodeH
barcodeX = 175
barcodeY = 5

barcodeRect = fitz.Rect(barcodeX, barcodeY, barcodeX + barcodeW, barcodeY + barcodeH)

with fitz.open(inPdfPath) as f:
    pageOne = f[0]

    pageOne.insertImage(barcodeRect, filename = inBarPath)

    f.save(outPath)

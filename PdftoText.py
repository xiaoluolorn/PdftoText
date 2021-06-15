from pdfminer.pdfparser import PDFParser, PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import LTTextBoxHorizontal, LAParams
from pdfminer.pdfinterp import PDFTextExtractionNotAllowed
import logging
import time
# 不显示warning
logging.propagate = False
logging.getLogger().setLevel(logging.ERROR)

pdf_filename = "E:\\2020.pdf"
txt_filename = "E:\\2020.txt"

device = PDFPageAggregator(PDFResourceManager(), laparams=LAParams())
interpreter = PDFPageInterpreter(PDFResourceManager(), device)

doc = PDFDocument()
parser = PDFParser(open(pdf_filename, 'rb'))
parser.set_document(doc)
doc.set_parser(parser)
doc.initialize()
time_start=time.time()
# 检测文档是否提供txt转换，不提供就忽略
if not doc.is_extractable:
    raise PDFTextExtractionNotAllowed
else:
    with open(txt_filename, 'w', encoding="utf-8") as fw:
        print("num page:{}".format(len(list(doc.get_pages()))))
        for page in doc.get_pages():
            interpreter.process_page(page)
            # 接受该页面的LTPage对象
            layout = device.get_result()
            # 这里layout是一个LTPage对象 里面存放着 这个page解析出的各种对象
            # 一般包括LTTextBox, LTFigure, LTImage, LTTextBoxHorizontal 等等
            # 想要获取文本就获得对象的text属性，
            for x in layout:
                if isinstance(x, LTTextBoxHorizontal):
                    results = x.get_text()
                    fw.write(results)

time_end=time.time()
print('totally cost',time_end-time_start)

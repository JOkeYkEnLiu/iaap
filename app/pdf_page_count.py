#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage

def getPDFPages(PathToPDF):
    fp = open(PathToPDF,'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser)
    num_pages = 0
    for page in PDFPage.create_pages(document):
        num_pages += 1
    return num_pages
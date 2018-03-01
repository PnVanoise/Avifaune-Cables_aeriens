## -*- coding: utf-8 -*-
import cStringIO
import csv
import codecs

def utf_8_encoder(rows):
    for row in rows:
        new_row = []
        for value in row:
            if isinstance(value, unicode):
                value = value.encode('utf-8')
            new_row.append(value)
        yield new_row

class CSVRenderer(object):
    def __init__(self, info):
        pass

    def __call__(self, values, system):
        fout = cStringIO.StringIO()
        # write BOM so that Excel can open UTF8 file properly
        fout.write(codecs.BOM_UTF8)
        writer = csv.writer(fout, delimiter=';', quoting=csv.QUOTE_ALL)

        writer.writerows(utf_8_encoder(values))

        resp = system['request'].response
        resp.content_type = 'text/csv'
        resp.content_disposition = 'attachment;filename="export.csv"'
        return fout.getvalue()

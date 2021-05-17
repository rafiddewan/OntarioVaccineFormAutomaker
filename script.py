import os
import sys
from collections import OrderedDict

def _getFields(obj, tree=None, retval=None, fileobj=None):
    fieldAttributes = {'/FT': 'Field Type', '/Parent': 'Parent', '/T': 'Field Name', '/TU': 'Alternate Field Name',
                       '/TM': 'Mapping Name', '/Ff': 'Field Flags', '/V': 'Value', '/DV': 'Default Value'}
    if retval is None:
        retval = OrderedDict()
        catalog = obj.trailer["/Root"]
        if "/AcroForm" in catalog:
            tree = catalog["/AcroForm"]
        else:
            return None
    if tree is None:
        return retval

    obj._checkKids(tree, retval, fileobj)
    for attr in fieldAttributes:
        if attr in tree:
            obj._buildField(tree, retval, fileobj, fieldAttributes)
            break

    if "/Fields" in tree:
        fields = tree["/Fields"]
        for f in fields:
            field = f.getObject()
            obj._buildField(field, retval, fileobj, fieldAttributes)

    return retval

def get_form_fields(infile):
    infile = PdfFileReader(open(infile, 'rb'))
    fields = _getFields(infile)
    return OrderedDict((k, v.get('/V', '')) for k, v in fields.items())

def selectListOption(all_lines, k, v):
    all_lines.append('function setSelectedIndex(s, v) {')
    all_lines.append('for (var i = 0; i < s.options.length; i++) {')
    all_lines.append('if (s.options[i].text == v) {')
    all_lines.append('s.options[i].selected = true;')
    all_lines.append('return;') 
    all_lines.append('}')
    all_lines.append('}')
    all_lines.append('}')
    all_lines.append('setSelectedIndex(document.getElementById("' + k + '"), "' + v + '");')

def readList(fname):
    lst = []
    with open(fname, 'r') as fh:  
        for l in fh:
            lst.append(l.rstrip(os.linesep))
    return lst

def createBrowserScript(fl, fl_ext, items, pdf_file_name):
    if pdf_file_name and len(fl) > 0:
        of = os.path.splitext(pdf_file_name)[0] + '.txt'
        all_lines = []
        for k, v in items.items():
            print(k + ' -> ' + v)
            if (v in ['/Yes', '/On']):
                all_lines.append("document.getElementById('" + k + "').checked = true;\n");
            elif (v in ['/0'] and k in fl_ext):
                all_lines.append("document.getElementById('" + k + "').checked = true;\n");
            elif (v in ['/No', '/Off', '']):
                all_lines.append("document.getElementById('" + k + "').checked = false;\n");
            elif (v in [''] and k in fl_ext):
                all_lines.append("document.getElementById('" + k + "').checked = false;\n");
            elif (k in fl):
                selectListOption(all_lines, k, v)
            else:
                all_lines.append("document.getElementById('" + k + "').value = '" + v + "';\n");
        outF = open(of, 'w')
        outF.writelines(all_lines)
        outF.close()

def execute(args):
    try: 
        fl = readList('myview.ini')
        fl_ext = readList('myview_ext.ini')
        if len(args) == 2:
            pdf_file_name = args[1]
            items = get_form_fields(pdf_file_name)
            createBrowserScript(fl, fl_ext, items, pdf_file_name)
        else:
            files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.pdf')]
            for f in files:
                items = get_form_fields(f)
                createBrowserScript(fl, fl_ext, items, f)
    except BaseException as msg:
        print('An error occured... :( ' + str(msg))

if __name__ == '__main__':
    from pprint import pprint
    execute(sys.argv)
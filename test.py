import xml.etree.ElementTree as ET
import csv
import sys
import pandas as pd

def traverse_xml(element, path, data_dict):
    attribute_str_keys = [f"{v}={k}" for v, k in element.attrib.items()]
    print(f'{attribute_str_keys}')
    value = element.text.strip() if element.text else '-'
    #attribute_str_keys = attribute_str_keys.split()
    if value != "-":
        data_dict.setdefault(path, []).append(value)
    else:
        data_dict.setdefault(path, []).append("-")
    for attribute in attribute_str_keys:
        attrib = attribute
        keys, values = attrib.split("=") if attrib else ('-', '-')
        if values != "-":
            data_dict.setdefault(f"{path}.{keys}", []).append(values)
        else:
            data_dict.setdefault(f"{path}.{keys}", []).append("-")
    for child in element:
        currentpath = path + "." + child.tag
        traverse_xml(child, currentpath, data_dict)

original_dict = {}
new_dict = {}
data_dict = {}

xmlfiles = sys.argv[1:]  # Получаем все XML файлы из аргументов командной строки

for xmlfile in xmlfiles:
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    traverse_xml(root, root.tag, data_dict)
result_dict = data_dict.copy()
with open('output.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    for key, value in result_dict.items():
        writer.writerow([key] + value)

# Чтение и транспонирование CSV файла
data = []
with open('output.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file)
    for row in csv_reader:
        data.append(row)

# чтение файла Excel в объект DataFrame
pd.read_csv('output.csv', names=range(2000), on_bad_lines='warn', sep=",", header=None, index_col=None).T.to_csv('outputVM.csv', header=False, index=False)



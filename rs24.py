# TODO 1) обработка ошибок
# TODO  3) парс категориии и каталога
import csv
import os
import zipfile
from ftplib import FTP
from xml.etree import ElementTree
import glob

result = []
unit = {'PCE': 'шт', 'NMP': 'упак', 'MTR': 'м'}


# def connect_to_ftp_data():
#     file_name = "result.xml"
#     ftp = FTP()
#     ftp.connect(host='service.russvet.ru', port=21021)
#     ftp.login(user='Samoletdevelopment', passwd='Gn6pYJ8U')
#     ftp.cwd('pricat/ARCHIVE')
#     latest_file = ftp.nlst()[0]
#
#     download_data(ftp, latest_file, file_name)
#     gather_data(file_name)
#
#     ftp.quit()


def connect_to_ftp_structure():
    file_name = "structure.zip"

    ftp = FTP()
    ftp.connect(host='service.russvet.ru', port=21021)
    ftp.login(user='prodat', passwd='bT6tsv3')
    ftp.cwd('sklad/TVER')
    latest_file = ftp.nlst()[-1]

    download_data(ftp, latest_file, file_name)
    unzip_structure_file()

    ftp.quit()


def download_data(ftp, latest_file, file_name):
    with open(file_name, "wb") as file:
        ftp.retrbinary(f"RETR {latest_file}", file.write)
        file.close()


def unzip_structure_file():
    with zipfile.ZipFile('structure.zip', 'r') as zip_ref:
        zip_ref.extractall()




connect_to_ftp_structure()


# connect_to_ftp_data()


def gather_data(file_name):
    data = ElementTree.parse(file_name)
    product = data.findall("DocDetail")

    for item in product:
        title = item.find("ProductName").text  # Наименование товара
        price = float(item.find("RetailPrice").text)  # Базовая цена товара с НДС
        discount_price = float(item.find("CustPrice").text)  # Цена клиента с НДС
        product_link = "-1"  # Ссылка на товар
        inventory = float(item.find("SumQTY").text)  # Количество товара
        if inventory > 0:
            stock = 1  # Наличие
        else:
            stock = 0  # Наличие
        is_order = 1  # Возможность заказа
        article = item.find("SenderPrdCode").text  # Артикул товара
        id_site = 'RS24.ru'  # Сайт
        id_stock_name = "-1"  # Название акции
        id_unit = unit.get(item.find("UOM").text)  # Ед. измерения
        id_city = 'all'  # Город


#TODO CATEG
        # for file in glob.glob('PRODAT*.xml'):
        #     structure = ElementTree.parse(file)
        #     desc = structure.findall("DocDetail")
        #
        #     for rec in desc:
        #         id_catalog = item.find("ParentProdGroup").text
        #         id_category = item.find("ProductGroup").text

        result.append({'title': title, 'price': price, 'discount_price': discount_price,
                       'product_link': product_link,
                       'stock': stock, 'is_order': is_order, 'inventory': inventory, 'article': article,
                       'id_category': id_category, 'id_site': id_site, 'id_catalog': id_catalog,
                       'id_stock_name': id_stock_name, 'id_unit': id_unit, 'id_city': id_city})

# def result_to_csv(result):
#     keys = result[0].keys()
#     with open('data.csv', 'w', newline='') as output_file:
#         dict_writer = csv.DictWriter(output_file, keys)
#         dict_writer.writeheader()
#         dict_writer.writerows(result)
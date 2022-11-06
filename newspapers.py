import calendar
import os
import re
from datetime import date
from datetime import timedelta
from time import time
import PyPDF2
import pandas as pd
from constants import df
from constants import driver


# can use to ensure only files created in downloads folder after program execution are moved to invoices folder
def time_program_executed():
    return time()


# this value to be used when creating new folder and in a function when moving invoices from downloads to this folder
def get_last_saturday_date():
    today = date.today()
    offset = (today.weekday() - calendar.SATURDAY) % 7  # SATURDAY = 5 (Mon = 0, Sun = 6).
    # So if was tues would be 1-5 = -4. Then modulus -> -4%7 = 3
    last_sat_date = today - timedelta(days=offset)  # so if was tuesday would be taking 3
    # days away to get last Saturday's date
    last_sat_date_to_string = last_sat_date.strftime("%d.%m.%Y")  # convert to string that
    # can use to name folder putting invoices to
    return last_sat_date_to_string


#  checking a vertical list from a selected starting cell down to count every cell until reach a cell that is
#  1) empty or 2) is blank and just has space bar key presses - if a store is added or deleted will still work if use
#  this value to loop
def count_number_of_stores(first_store_row_num_excel, first_store_col_num_excel):
    number_of_stores = 0
    # Using a try/except catches exception if try to access a cell outside last cell with data which pandas
    # library reads to get an Index error
    try:
        is_cell_blank = False
        while not is_cell_blank:
            # check if cell just contains white spaces
            cell_value = df.iloc[first_store_row_num_excel, first_store_col_num_excel]

            merge_list_to_string = ""
            if not pd.isna(cell_value):
                make_list = cell_value.split()
                merge_list_to_string = " ".join(make_list)  # will remove blank spaces

            if pd.isna(cell_value):  # check if cell returns NaN
                is_cell_blank = True
            elif merge_list_to_string == "":  # check if cell is empty with no spaces
                is_cell_blank = True
            else:
                number_of_stores = number_of_stores + 1
                first_store_row_num_excel = first_store_row_num_excel + 1
    except IndexError:
        print("Index Error! Is program trying to access a blank cell outside range set by Pandas read function?")
    return number_of_stores


# get account numbers starting from the cell where the first account number is populated on Excel
def get_account_numbers(account_num_row, account_num_column, num_of_stores):
    account_numbers = []
    for x in range(num_of_stores):
        account_numbers.append(df.iloc[account_num_row, account_num_column])
        account_num_row = account_num_row + 1
    return account_numbers


# get passwords starting from the cell where the first password is populated on Excel
def get_passwords(password_num_row, password_num_column, num_of_stores):
    passwords = []
    for x in range(num_of_stores):
        passwords.append(df.iloc[password_num_row, password_num_column])
        password_num_row = password_num_row + 1
    return passwords


# get store names starting from the cell where the first store name is populated on Excel
def get_store_names(store_name_num_row, store_name_num_column, num_of_stores):
    store_name = []
    for x in range(num_of_stores):
        store_name.append(df.iloc[store_name_num_row, store_name_num_column])
        store_name_num_row = store_name_num_row + 1
    return store_name


def navigate_to_newspapers_website():
    driver.get("https://www.i-menzies.com/")


def open_folder_with_invoices(invoices_folder_path):
    os.startfile(os.path.realpath(invoices_folder_path))


# create path where want the merged pdf file to go (value to be passed into .write() function)
def get_path_of_merged_pdf(new_folder_for_invoices):
    merged_file_name = get_last_saturday_date() + " Merged Invoices.pdf"
    merged_file_path = os.path.join(new_folder_for_invoices, merged_file_name)
    return merged_file_path


#  merge pdf files and save them to relevant folder
def merge_pdfs_together(time_program_ran, downloads_folder, merged_file_path):
    merger = PyPDF2.PdfMerger()
    for root, dirs, files in os.walk(downloads_folder, topdown=True):
        for name in files:
            file_path = os.path.join(root, name)
            # if a file was modified (downloaded) after run move to newly created folder
            if os.path.getmtime(file_path) > time_program_ran:
                merger.append(file_path)
    merger.write(merged_file_path)  # merge all pdfs downloaded after program execution to this file path
    merger.close()


def find_missing_invoices(number_of_stores, account_numbers, store_names, path_of_merged_pdf):
    doc = PyPDF2.PdfFileReader(path_of_merged_pdf)
    stores_not_found = []
    text = ""

    #  extract all the data from the merged file to store in text variable
    for x in range(doc.getNumPages()):
        current_page = doc.getPage(x)
        text = text + current_page.extract_text()

    #  search by account number and if not found append it to list of stores not found
    for y in range(number_of_stores):
        if re.search(str(account_numbers[y]), text) is None:
            stores_not_found.append(store_names[y])

    #  print message showing missing stores
    if len(stores_not_found) > 0:
        print("Missing stores: " + str(stores_not_found))

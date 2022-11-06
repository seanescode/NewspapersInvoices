import os.path
import newspapers as np
import eason


def main():
    #  variables:
    path_to_downloads_folder = os.path.expandvars(r"%HOMEPATH%\Downloads")
    path_to_invoices_folder = os.path.expandvars(r"%HOMEPATH%\test python newspapers move")
    time_program_started = np.time_program_executed()
    number_of_stores = np.count_number_of_stores(1, 0)
    account_numbers = np.get_account_numbers(1, 2, number_of_stores)
    store_names = np.get_store_names(1, 0, number_of_stores)
    passwords = np.get_passwords(1, 3, number_of_stores)
    path_merged_pdf = np.get_path_of_merged_pdf(path_to_invoices_folder)
    #  functions:
    np.navigate_to_newspapers_website()
    eason.log_in_and_download_invoices(number_of_stores, account_numbers, passwords, path_to_downloads_folder)
    np.merge_pdfs_together(time_program_started, path_to_downloads_folder, path_merged_pdf)
    np.find_missing_invoices(number_of_stores, account_numbers, store_names, path_merged_pdf)
    np.open_folder_with_invoices(path_to_invoices_folder)


if __name__ == '__main__':
    main()

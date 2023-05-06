import os
import pandas as pd
import shutil

folder_path = './data'
to_be_cleaned_folder_path = os.path.join(folder_path, 'to_be_cleaned')
files = os.listdir(to_be_cleaned_folder_path)

csv_files = [file for file in files if file.endswith('.csv')]

old_folder_path = os.path.join(folder_path, 'old')
old_cleaned_folder_path = os.path.join(folder_path, 'old_cleaned')

if not os.path.exists(old_folder_path):
    os.makedirs(old_folder_path)

if not os.path.exists(old_cleaned_folder_path):
    os.makedirs(old_cleaned_folder_path)

all_data_cleaned = []

for csv_file in csv_files:
    data = pd.read_csv(os.path.join(to_be_cleaned_folder_path, csv_file), skiprows=4, encoding="ISO-8859-1")
    data = data.rename(columns=lambda x: x.strip())

    index_to_drop = data[data['Fecha de Transacción'] == 'Resumen de Estado Bancario'].index
    data_cleaned = data.drop(data.index[index_to_drop[0]:])

    data_cleaned.to_csv(os.path.join(to_be_cleaned_folder_path, csv_file[:-4] + '_cleaned.csv'), index=False)
    all_data_cleaned.append(data_cleaned)

    shutil.move(os.path.join(to_be_cleaned_folder_path, csv_file), os.path.join(old_folder_path, csv_file))

data_file_path = os.path.join(folder_path, 'data.csv')
if os.path.exists(data_file_path):
    existing_data = pd.read_csv(data_file_path)
    all_data_cleaned.insert(0, existing_data)

merged_data_cleaned = pd.concat(all_data_cleaned)

merged_data_cleaned = merged_data_cleaned.drop_duplicates(subset=['Fecha de Transacción', 'Referencia de Transacción'])

merged_data_cleaned.to_csv(data_file_path, index=False)

for cleaned_csv_file in os.listdir(to_be_cleaned_folder_path):
    if cleaned_csv_file.endswith('_cleaned.csv'):
        shutil.move(os.path.join(to_be_cleaned_folder_path, cleaned_csv_file), os.path.join(old_cleaned_folder_path, cleaned_csv_file))

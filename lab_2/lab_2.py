import pandas as pd
from datetime import datetime
from urllib.request import urlopen


def download():
    date_time = datetime.now()
    separated_date_time = date_time.strftime('%Y_%m_%d__%H_%M_%S')
    for index_r in range(1, 28):
        url = f'https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_TS_admin.php?country=UKR&provinceID={index_r}&year1=1981&year2=2023&type=Mean'
        vhi_url = urlopen(url)
        with open(f'dataset/_{separated_date_time}_vhi_id_{index_r}.csv', 'w') as out:
            dataset_s = vhi_url.read().decode('utf-8').replace('<br>', '').replace('<tt><pre>', '').replace(' ', '').split('\n')
            dataset_s.pop(-1)
            a = dataset_s.pop(0)
            a = a.split(':')[1].split(',')[0]
            out.write(f'{a}\n'+'\n'.join(dataset_s))
#download()

def read_csv_file():
    tuple_NNAA_to_LW = {1: 22, 2: 24,  3: 23, 4: 25,  5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10, 14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 0, 21: 17, 22: 18, 23: 6,  24: 1, 25: 2, 26: 7, 27: 5}
    frames = []

    for index_f in range(1, 28):
        with open(f'dataset/_2024_01_02__12_57_51_vhi_id_{index_f}.csv', "r") as dataset:
            df = dataset.readlines()
            df = [line.strip().split(',') for line in df]

            # Створюємо DataFrame з даних з кожного файлу
            df = pd.DataFrame(df[2:], columns=['year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
            df = df.astype(
                {'year': int, 'Week': int, 'SMN': float, 'SMT': float, 'VCI': float, 'TCI': float, 'VHI': float,
                 'empty': str})

            df['index_region'] = tuple_NNAA_to_LW[index_f]

            frames.append(df)

    # Об'єднуємо всі DataFrame в один DataFrame
    result_df = pd.concat(frames, ignore_index=True)

    return result_df


#Ряд VHI для області за рік, пошук екстремумів (min та max);
def min_max_VHI(year, index):
    a = read_csv_file()
    VHI = a[(a["year"] == year) & (a["index_region"] == index) & (a['VHI'] != -1.00)]

    return VHI['VHI'].max(), VHI['VHI'].min()
print("min_max_VHI: ",min_max_VHI(1982, 2))

#Ряд VHI за всі роки для області, виявити роки з екстремальними посухами, які торкнулися більше вказаного відсотка області;
def ext_drought(index):
    df = read_csv_file()
    data_year = df[(df["index_region"] == index) & (df['VHI'] != '-1.00')]
    year = data_year[(pd.to_numeric(data_year['VHI'], errors='coerce') < 15.00) & data_year['year']]
    return year['year']
print("extreme_drought: ", ext_drought(2))


# Аналогічно для помірних посух
def nor_drought(index):
    df = read_csv_file()
    data_year = df[(df["index_region"] == index) & (df['VHI'] != -1.00)]
    year = data_year[(data_year['VHI'] < 35.00) & data_year['year']]
    year = year[(year['VHI'] > 15.00) & year['year']]
    return year['year']
print("moderate_drought: ", nor_drought(2))


import argparse
import re

def get_name_file() -> str:
    """
    Функция для получения названия файла из командной строки
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('file', type=str, help='name_file.txt')
    arg = parser.parse_args()
    return arg.file

def read_file(file_name: str) -> str:
    """
    Функция для прочтения файла
    """
    with open(file_name, "r", encoding='utf-8') as file:
        text = file.read()
    return text

def get_dates(data: str) -> list:
    """
    Функция для изъятия дат 
    """
    pattern=r'Дата рождения: (\d{2}\.\d{2}\.\d{4})'
    birth_dates = re.findall(pattern, data)
    return birth_dates
    

def counting_people(dates: str) -> int:
    """
    Функция для подсчёта людей в возрасте от 30 до 40 лет с наличием корректировки в случае,
    если дня рождения в 2024 году не было
    
    current_day/current_month/current_year - текущая дата
    
    birth_day/birth_month/birth_year - дата рождения 
    """
    current_day = 29
    current_month = 11
    current_year = 2024
    count = 0
    
    for date_str in dates:
        birth_day, birth_month, birth_year = map(int, date_str.split('.'))
    
        age = current_year - birth_year
 
        if (current_month < birth_month) or (current_month == birth_month and current_day < birth_day):
            age -= 1
        
        if 30 <= age <= 40:
            count += 1
            
    return count

def main():
    file_name = get_name_file()
    form = read_file(file_name)
    dates = get_dates(form) 
    result = counting_people(dates)
    print(f"Количество людей возрастом от 30 до 40 лет: {result}")

if __name__ == "__main__":
    main()
    
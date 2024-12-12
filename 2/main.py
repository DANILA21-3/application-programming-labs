import argparse
import csv
import os
from icrawler.builtin import GoogleImageCrawler

def parse_args():
    """
    Создаёт парсер, в котором содержатся аргументы, возвращиющие ключеове слово/место хранения фото/файл для аннотаций
    """
    parser = argparse.ArgumentParser(description="Download images and create an annotation.")
    parser.add_argument("keyword", type=str, help="Keyword")
    parser.add_argument("file_for_images", type=str, help="Directory to save images")
    parser.add_argument("file_annotation", type=str, help="CSV file for annotations")

    return parser.parse_args()

def download_images(keyword: str, folder: str, count: int) -> None:
    """
    Загружает фото по ключевому слову в заданном количестве в заданное место
    
    google_crawler : объект для скачивания фото
    """
    try:
        google_crawler = GoogleImageCrawler(storage={'root_dir': folder})
        google_crawler.crawl(keyword, max_num=count, filters={})  
    except Exception as e:
        print(f"Error download: {e}")

def create_annotation(file_annotation: str, file_for_images: str) -> None:
    """
    Открывает файл в режиме записи и с помощью объекта записи проводит необходимые действия при помощи цикла
    
    writer : объект, который производит запись в файл
    """
    with open(file_annotation, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["absolute_path", "relative_path"])
        for filename in os.listdir(file_for_images):
            absolute_path = os.path.abspath(os.path.join(file_for_images, filename))
            relative_path = os.path.relpath(absolute_path, start=file_for_images)
            writer.writerow([absolute_path, relative_path])

class Iterator:
    """
    Класс обеспечивает удобное использование файла при его чтении
    
    __init__: производит инициализацию итератора и открывает файл для чтения с пропуском заголовка
    
    __iter__: возвращает текущее значение
    
    __next__: возвращает следующее значение
    """
    def __init__(self, annotation_file: str):
        self.items = []
        self.index = 0
        with open(annotation_file, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  
            self.items = list(reader)
    
    def __iter__(self):
        return self 
    
    def __next__(self):
        if self.index < len(self.items):
            result = self.items[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration



def main():
    args = parse_args()
    keyword = args.keyword
    file_for_images = args.file_for_images
    file_annotation = args.file_annotation
    
    download_images(keyword, file_for_images, 50)
    
    create_annotation(file_annotation, file_for_images)
    
    iterator = Iterator(file_annotation)
    for absolute_path, relative_path in iterator:
        print(f"absolute_path: {absolute_path}, relative_path: {relative_path}")

if __name__ == "__main__":
    main()

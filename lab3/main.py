import argparse
import cv2
import matplotlib.pyplot as plt

def arg_parser():
    """
    Создаёт парсер с аргументами, содержащими пути изображений и папки
    
    cmd : парсер содержащий аргументы с командной строки
    
    """
    cmd = argparse.ArgumentParser(description = "images")
    cmd.add_argument('folder_for_save', type=str , help="folder for communuication with image")
    cmd.add_argument('left_img', type=str , help="left image for split")
    cmd.add_argument('right_img', type=str , help="right image for split")
    return cmd.parse_args()

def get_img(directory:str):
    """
    Возвращает изображение по указанной директории
    
    directoty : директория возвращаемого изображения
    """
    image = cv2.imread(directory)
    if image is None:
        print(f"Error get")
        return None
    return image

def size_img(image):
    """
    возвращает размеры(высоту и ширину) изображения
    
    image : изображение, которое используется для возрвращения высоты и ширины
    """
    height, width = image.shape[:2]
    return height, width

def plot_histogram(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    colors = ('r', 'g', 'b')
    plt.figure(figsize=(16, 9))
    
    for i, color in enumerate(colors):
        hist = cv2.calcHist([image], [i], None, [256], [0, 256])
        plt.plot(hist, color=color)
        plt.xlim([0, 256])
    
    plt.title('Histogram')
    plt.xlabel('Bright')
    plt.ylabel('Count pixels')
    plt.legend(['Red', 'Green', 'Blue'])
   
    plt.show()

def split_img(img_left, img_right):
    """
    объединяет два изображения в одно по горизонтали
    
    img_left , img_right : изображения, которые соединяются в одно изображение
    """
    return cv2.hconcat([img_left, img_right])

def print_img(img_left, img_right, split_img):
    """
    Создаёт сетку(1 строка, 3 столбца) и выгружает в неё изображения в соответствующую ячейку
    
    img_left , img_right : изображения, которые соединяются в одно изображение
    split_img : изображение, полученное путём соединения из двух
    """
    plt.figure(figsize=(16, 9))
    
    plt.subplot(1, 3, 1)
    plt.imshow(cv2.cvtColor(img_left, cv2.COLOR_BGR2RGB))
    plt.title('left')
    plt.axis('off')
    
    plt.subplot(1, 3, 2)
    plt.imshow(cv2.cvtColor(img_right, cv2.COLOR_BGR2RGB))
    plt.title('right')
    plt.axis('off')
    
    plt.subplot(1, 3, 3)
    plt.imshow(cv2.cvtColor(split_img, cv2.COLOR_BGR2RGB))
    plt.title('result')
    plt.axis('off')
    
    plt.show()
    
def save_img(image, folder_for_save):
    """
    Сохраняет изображение по указанной директории
    
    image : сохраняемое изображение
    folder_for_save : директория для сохранения изображения
    """
    cv2.imwrite(f'{folder_for_save}/result.jpg', image)
    
def main():
    cmd = arg_parser()
    
    left_image = get_img(cmd.left_img)
    right_image = get_img(cmd.right_img)
    
    print(f"Size image{size_img(left_image)}")
    
    plot_histogram(left_image)
    
    result = split_img(left_image, right_image)
    
    print_img(left_image, right_image, result )
    
    save_img(result, cmd.folder_for_save)
    
if __name__ == "__main__":
    main()
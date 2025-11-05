import PyPDF2
import os

def get_page_size(pdf_path):
    """
    Получает размеры первой страницы PDF файла
    """
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if len(pdf_reader.pages) == 0:
                return None, None, "Файл не содержит страниц"
            
            # Получаем первую страницу
            first_page = pdf_reader.pages[0]
            
            # Получаем размеры страницы
            media_box = first_page.mediabox
            width = float(media_box.width)
            height = float(media_box.height)
            
            # Определяем длину и ширину (большая сторона - длина, меньшая - ширина)
            length = max(width, height)
            width = min(width, height)
            
            # Вычисляем соотношение
            ratio = length / width
            
            return length, width, ratio
            
    except Exception as e:
        return None, None, f"Ошибка при чтении файла: {str(e)}"

def main_console():
    """
    Консольная версия программы
    """
    print("Программа для анализа размеров страницы PDF файла")
    
    while True:
        pdf_path = input("Введите путь к PDF файлу (или 'quit' для выхода): ").strip()
        
        if pdf_path.lower() == 'quit':
            break
            
        if not os.path.exists(pdf_path):
            print("Ошибка: Файл не существует")
            continue
            
        if not pdf_path.lower().endswith('.pdf'):
            print("Ошибка: Файл должен быть в формате PDF")
            continue
        
        # Получаем размеры страницы
        length, width, ratio_or_error = get_page_size(pdf_path)
        
        # Выводим результат
        if length is not None and width is not None:
            print(f"Длина = {length:.2f} пунктов")
            print(f"Ширина = {width:.2f} пунктов")
            print(f"Отношение = {ratio_or_error:.4f}")
        else:
            print(f"Ошибка: {ratio_or_error}")
        
        print("-" * 50)

if __name__ == "__main__":
    main_console()
import PyPDF2
import os
from copy import deepcopy

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

### def determine_parts_count(ratio):
###     """
###     Определяет количество частей для разделения на основе соотношения сторон
###     """
###     if 0.69 <= ratio <= 0.72:
###         return 2, "по ширине страницы"
###     elif 0.46 <= ratio <= 0.48:
###         return 3, "по длинной стороне страницы"
###     elif 0.34 <= ratio <= 0.36:
###         return 4, "по длинной стороне страницы"
###     elif 0.27 <= ratio <= 0.29:
###         return 5, "по длинной стороне страницы"
###     elif 0.22 <= ratio <= 0.25:
###         return 6, "по длинной стороне страницы"
###     elif 0.19 <= ratio <= 0.21:
###         return 7, "по длинной стороне страницы"
###     elif 0.16 <= ratio <= 0.18:
###         return 8, "по длинной стороне страницы"
###     elif 0.15 <= ratio <= 0.16:
###         return 9, "по длинной стороне страницы"
###     elif 0.14 <= ratio <= 0.15:
###         return 10, "по длинной стороне страницы"
###     else:
###         return None, "не определено (соотношение не подходит под заданные диапазоны)"

def determine_parts_count(ratio):
    """
    Определяет количество частей для разделения на основе соотношения сторон
    """
    if 1.40 <= ratio <= 1.42:
        return 2, "по ширине страницы"
    elif 2.1 <= ratio <= 2.2:
        return 3, "по длинной стороне страницы"
    elif 2.8 <= ratio <= 2.9:
        return 4, "по длинной стороне страницы"
    elif 3.5 <= ratio <= 3.6:
        return 5, "по длинной стороне страницы"
    elif 4.2 <= ratio <= 4.3:
        return 6, "по длинной стороне страницы"
    elif 4.9 <= ratio <= 5.0:
        return 7, "по длинной стороне страницы"
    elif 5.6 <= ratio <= 5.7:
        return 8, "по длинной стороне страницы"
    elif 6.3 <= ratio <= 6.4:
        return 9, "по длинной стороне страницы"
    elif 7.0 <= ratio <= 7.1:
        return 10, "по длинной стороне страницы"
    else:
        return None, "не определено (соотношение не подходит под заданные диапазоны)"

def split_page(page, parts_count, split_direction):
    """
    Разделяет страницу на указанное количество частей
    """
    split_pages = []
    media_box = page.mediabox
    
    width = float(media_box.width)
    height = float(media_box.height)
    
    # Определяем ориентацию страницы
    is_landscape = width > height
    long_side = max(width, height)
    short_side = min(width, height)
    
    if split_direction == "по ширине страницы":
        # Разделяем по короткой стороне (ширине)
        part_width = short_side / parts_count
        for i in range(parts_count):
            new_page = deepcopy(page)
            if is_landscape:
                # Горизонтальная ориентация: width - длинная, height - короткая
                new_page.mediabox.lower_left = (0, i * part_width)
                new_page.mediabox.upper_right = (long_side, (i + 1) * part_width)
            else:
                # Вертикальная ориентация: height - длинная, width - короткая
                new_page.mediabox.lower_left = (i * part_width, 0)
                new_page.mediabox.upper_right = ((i + 1) * part_width, long_side)
            split_pages.append(new_page)
    else:
        # Разделяем по длинной стороне
        part_length = long_side / parts_count
        for i in range(parts_count):
            new_page = deepcopy(page)
            if is_landscape:
                # Горизонтальная ориентация
                new_page.mediabox.lower_left = (i * part_length, 0)
                new_page.mediabox.upper_right = ((i + 1) * part_length, short_side)
            else:
                # Вертикальная ориентация
                new_page.mediabox.lower_left = (0, i * part_length)
                new_page.mediabox.upper_right = (short_side, (i + 1) * part_length)
            split_pages.append(new_page)
    
    return split_pages

def save_split_pages(original_path, split_pages):
    """
    Сохраняет разделенные страницы как отдельные файлы и объединенный файл
    """
    base_name = os.path.splitext(original_path)[0]
    
    # Сохраняем отдельные части
    for i, page in enumerate(split_pages, 1):
        output_pdf = PyPDF2.PdfWriter()
        output_pdf.add_page(page)
        
        part_filename = f"{base_name}_часть_{i}.pdf"
        with open(part_filename, 'wb') as output_file:
            output_pdf.write(output_file)
        print(f"Создан файл: {part_filename}")
    
    # Сохраняем объединенный файл
    full_pdf = PyPDF2.PdfWriter()
    for page in split_pages:
        full_pdf.add_page(page)
    
    full_filename = f"{base_name}_полный.pdf"
    with open(full_filename, 'wb') as output_file:
        full_pdf.write(output_file)
    print(f"Создан объединенный файл: {full_filename}")

def main_console():
    """
    Консольная версия программы
    """
    print("Программа для анализа размеров страницы PDF файла")
    
    while True:
        pdf_path = input("\nВведите путь к PDF файлу (или 'quit' для выхода): ").strip()
        
        if pdf_path.lower() == 'quit':
            break
            
        if not os.path.exists(pdf_path):
            print("Ошибка: Файл не существует")
            continue
            
        if not pdf_path.lower().endswith('.pdf'):
            print("Ошибка: Файл должен быть в формате PDF")
            continue
        
        # Получаем размеры страницы
        length, width, ratio = get_page_size(pdf_path)
        
        # Выводим результат
        if length is not None and width is not None:
            print(f"Длина = {length:.2f} пунктов")
            print(f"Ширина = {width:.2f} пунктов")
            print(f"Отношение = {ratio:.4f}")
            
            # Определяем количество частей
            parts_count, split_direction = determine_parts_count(ratio)
            
            if parts_count:
                print(f"Рекомендуемое разделение: {parts_count} части(ей) {split_direction}")
                
                # Запрос подтверждения у пользователя
                response = input("Разделить страницу? (y/n): ").strip().lower()
                
                if response == 'y' or response == 'да':
                    try:
                        # Читаем исходный PDF
                        with open(pdf_path, 'rb') as file:
                            pdf_reader = PyPDF2.PdfReader(file)
                            first_page = pdf_reader.pages[0]
                            
                            # Разделяем страницу
                            split_pages = split_page(first_page, parts_count, split_direction)
                            
                            # Сохраняем результаты
                            save_split_pages(pdf_path, split_pages)
                            
                            print("Разделение завершено успешно!")
                            
                    except Exception as e:
                        print(f"Ошибка при разделении страницы: {str(e)}")
                else:
                    print("Разделение отменено пользователем.")
            else:
                print(split_direction)
        else:
            print(f"Ошибка: {ratio}")
        
        print("-" * 50)
        
        # Ожидание реакции пользователя перед следующим циклом
        input("Нажмите Enter для продолжения...")

if __name__ == "__main__":
    main_console()
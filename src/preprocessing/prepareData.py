import os
import re
import pandas as pd
from textwrap import dedent

def get_chaper_paths(folder) -> list[str]:
    book_titles = os.listdir(folder)
    chapter_paths = []

    for title in book_titles:
        book_path = os.path.join(folder, title)

        chapter_files = os.listdir(book_path)
        chapter_paths.extend([os.path.join(book_path, file) for file in chapter_files])

    return chapter_paths

def clean_markdown(text):
    """Loại bỏ các thẻ markdown từ văn bản."""
    if isinstance(text, str):
        text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)  # Loại bỏ **bold**
        text = re.sub(r'__(.*?)__', r'\1', text)  # Loại bỏ __bold__
        text = re.sub(r'\*(.*?)\*', r'\1', text)  # Loại bỏ *italic*
        text = re.sub(r'_(.*?)_', r'\1', text)  # Loại bỏ _italic_
        text = re.sub(r'`(.*?)`', r'\1', text)  # Loại bỏ `inline code`
        text = re.sub(r'~~(.*?)~~', r'\1', text)  # Loại bỏ ~~strikethrough~~
        text = re.sub(r'#+ (.*)', r'\1', text)  # Loại bỏ # headings
        text = re.sub(r'- \[ \] (.*)', r'\1', text)  # Loại bỏ - [ ] (unchecked checkbox)
        text = re.sub(r'- \[x\] (.*)', r'\1', text)  # Loại bỏ - [x] (checked checkbox)
        # Thêm các quy tắc khác nếu cần
        return text
    else:
        return ""

folder = "D:\\FPT\\AI\\Major5\\DPL302m\\Project\\StoryGen\\data"
path_summary = os.path.join(folder, "summary")
path_raw = os.path.join(folder,"raw")
path_reject = os.path.join(folder, "reject")
path_traning = os.path.join(folder, "training")
orpo_dataset_dict = {"prompt": [], "choose": [], "rejected": []}
failed_data = []

chapter_paths = get_chaper_paths(path_raw)

i = 1
for path in chapter_paths:
    book_title = path.split('\\')[-2]
    chapter_title = path.split('\\')[-1]
    print(f"Processing: {chapter_title} - {book_title}")

    processed_path_summary = os.path.join(path_summary, book_title, chapter_title)
    processed_path_raw = os.path.join(path_raw, book_title, chapter_title)
    processed_path_reject = os.path.join(path_reject, book_title, chapter_title)

    try:
        with open(processed_path_summary, 'r', encoding='utf-8') as f_summary, \
            open(processed_path_raw, 'r', encoding='utf-8') as f_raw, \
            open(processed_path_reject, 'r', encoding='utf-8') as f_reject:

            content = f_summary.read()
            prompt = f'''
                Dựa vào những ý chính theo dòng thời gian như sau:
                {content}
                Lưu ý: Mỗi gạch đầu dòng là một ý. 
                        
                Viết thành 1 chương truyện hoàn chỉnh
                '''
            prompt = dedent(prompt)

            orpo_dataset_dict["prompt"].append(prompt)
            orpo_dataset_dict["choose"].append(f_raw.read())
            # Làm sạch markdown trước khi lưu
            cleaned_reject = clean_markdown(f_reject.read()) 
            orpo_dataset_dict["rejected"].append(cleaned_reject)

    except FileNotFoundError:
        print(f"WARNING: Missing file for {chapter_title} - {book_title}. Adding to failed data.")
        failed_data.append({"book_title": book_title, "chapter_title": chapter_title})


# Create dataframe and save
df = pd.DataFrame(orpo_dataset_dict)
path_orpo_dataset = os.path.join(path_traning, "orpo_dataset.csv")
df.to_csv(path_orpo_dataset, index=False)

# Save failed data if any
if failed_data:
    path_failed_data = os.path.join(path_traning, "failed_data.csv")
    pd.DataFrame(failed_data).to_csv(path_failed_data, index=False)

    


   
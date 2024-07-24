import os
import re
import pandas as pd
from textwrap import dedent
import pandas as pd
from sklearn.model_selection import train_test_split



# def get_chaper_paths(folder) -> list[str]:
#     book_titles = os.listdir(folder)
#     chapter_paths = []

#     for title in book_titles:
#         book_path = os.path.join(folder, title)

#         chapter_files = os.listdir(book_path)
#         chapter_paths.extend([os.path.join(book_path, file) for file in chapter_files])

#     return chapter_paths

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


def split_books():
    root = os.getcwd()
    path_to_books = os.path.join(root, 'data/raw')
    
    book_titles = os.listdir(path_to_books)
    df = pd.DataFrame({'title': book_titles}) 
    df['n_chapters'] = df['title'].apply(lambda x: len(os.listdir(os.path.join(path_to_books, x))))
    
    train_path = os.path.join(root, 'data', 'train.csv')
    test_path = os.path.join(root, 'data', 'test.csv')

    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)
    train_df.reset_index(inplace=True, drop=True)
    test_df.reset_index(inplace=True, drop=True)

    train_df.to_csv(train_path)
    test_df.to_csv(test_path)


def get_chapters():

    root = os.getcwd()
    path_to_raw = os.path.join(root, 'data', 'raw')
    book_titles = os.listdir(path_to_raw)
    all_chapters = []
    
    for title in book_titles:
        path_to_book = os.path.join(path_to_raw, title)
        chapters = os.listdir(path_to_book)
        chapters = [os.path.join(title, chap) for chap in chapters]
        all_chapters.extend(chapters)

    return all_chapters

def get_content(path_to_chapter):
    try:
        with open(path_to_chapter) as file:
            return clean_markdown(file.read())
    except:
        return 'Empty'
def create_preference_dataset():
    chapters = get_chapters()
    df = pd.DataFrame({'chapter_title': chapters})

    root = os.getcwd()
    path_to_raw = os.path.join(root, 'data', 'raw')
    df['chosen'] = df['chapter_title'].apply(lambda x: get_content(os.path.join(path_to_raw, x)))
    
    path_to_reject = os.path.join(root, 'data', 'reject')
    df['rejected'] = df['chapter_title'].apply(lambda x: get_content(os.path.join(path_to_reject, x)))

    path_to_summary = os.path.join(root, 'data', 'summary')
    df['summary'] = df['chapter_title'].apply(lambda x: get_content(os.path.join(path_to_summary, x)))
    df['prompt'] = df['summary'].apply(lambda x: f'''
Dựa vào bản tóm tắt của chương truyện theo dòng thời gian sau: 

    {x}  

Tưởng tượng bạn là một tiểu thuyết gia với 20 năm kinh nghiệm viết tiểu thuyết và đã xuất bản hơn 100 cuốn tiểu thuyết bán chạy nhất mọi thời đại.
Hãy tận dụng hết khả năng của bạn và viết một chương truyện hoàn hảo.             
''')

    path_to_save = os.path.join(root, 'data', 'processed', 'preference.csv')
    df.to_csv(path_to_save)

if __name__=='__main__':
    create_preference_dataset()
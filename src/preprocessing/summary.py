from gradio_client import Client
from textwrap import dedent
import os
client = Client("Qwen/Qwen2-72B-Instruct")
result = client.predict(
		query='''hello''',
		history=[],
		system="You are a helpful assistant.",
		api_name="/model_chat"
)
print(result)
# RAW_DATA_PATH = '/home/tandattran772/persional_project/StoryGen/data/raw'

# files = os.listdir(RAW_DATA_PATH)

# print(files)

def get_chaper_paths() -> list[str]:
    book_titles = os.listdir(RAW_DATA_PATH)
    chapter_paths = []

    for title in book_titles:
        book_path = os.path.join(RAW_DATA_PATH, title)
        chapter_files = os.listdir(book_path)
        chapter_paths.extend([os.path.join(book_path, file) for file in chapter_files])

    return chapter_paths

def get_prompt(chapter_path : str) -> str:
    content = ''
    with open(chapter_path) as file:
        content = file.read() 

    prompt = f'''
            Đọc và tóm tắc những ý chính của chương truyện theo dòng thời gian theo cấu trúc sau:
            """
                - ý 1   
                - ý 2
                ... 
            """
            Lưu ý: Mỗi gạch đầu dòng là một ý. 
                    
            Dưới đây là nội dung chương truyện:
            """
                {content}
            """
            '''
    
    return(dedent(prompt))    

def summarize(prompt : str) -> str:
    client = Client("Qwen/Qwen2-72B-Instruct")  
    result = client.predict(
		query=prompt,
		history=[],
		system="Bạn là một tiểu thuyết gia",
		api_name="/model_chat"
    )
    histories = result[1]
    respond = histories[0][1]
    return respond

# prompt = get_prompt('/home/tandattran772/persional_project/StoryGen/data/raw/Cuốn Theo Chiều Gió/Chương 20.txt')

# print(summary(prompt))

if __name__=='__main__':
    RAW_DATA_PATH = '/home/tandattran772/persional_project/StoryGen/data/raw'
    PROCESSED_DATA_PATH = '/home/tandattran772/persional_project/StoryGen/data/processed'
    chapter_paths = get_chaper_paths()
    for path in chapter_paths:
        book_title = path.split('/')[-2]
        chapter_title = path.split('/')[-1]
        
        # prompt = get_prompt(path)
        # summary = summarize(prompt)

        processed_book_dir = os.path.join(PROCESSED_DATA_PATH, book_title)
        if not os.path.exists(processed_book_dir):
            os.makedirs(processed_book_dir)

        processed_chapter_path = os.path.join(processed_book_dir, chapter_title)
        if not os.path.exists(processed_chapter_path):
            try:
                print(f'Process {book_title} {chapter_title}')
                prompt = get_prompt(path)
                summary = summarize(prompt)
                with open(processed_chapter_path, 'w', encoding='utf-8') as f:
                        f.write(summary)
                        print(f'{processed_chapter_path}')  
            except:
                print(f'Can not process {book_title} {chapter_title}')            
        else:
            print(f"There exists {processed_chapter_path}")              
        # break
        


# ver Thanh
from gradio_client import Client
from textwrap import dedent
import os
client = Client("Qwen/Qwen2-72B-Instruct")
result = client.predict(
		query='''hello''',
		history=[],
		system="You are a helpful assistant.",
		api_name="/model_chat"
)
print(result)
# RAW_DATA_PATH = '\\home\\tandattran772\\persional_project\\StoryGen\\data\\raw'

# files = os.listdir(RAW_DATA_PATH)

# print(files)

def get_chaper_paths() -> list[str]:
    book_titles = os.listdir(RAW_DATA_PATH)
    chapter_paths = []

    for title in book_titles:
        book_path = os.path.join(RAW_DATA_PATH, title)
        chapter_files = os.listdir(book_path)
        chapter_paths.extend([os.path.join(book_path, file) for file in chapter_files])

    return chapter_paths

def get_prompt(chapter_path : str) -> str:
    content = ''
    with open(chapter_path, encoding='utf-8') as file:
        content = file.read() 

    prompt = f'''
            Đọc và tóm tắc những ý chính của chương truyện theo dòng thời gian theo cấu trúc sau:
            """
                - ý 1   
                - ý 2
                ... 
            """
            Lưu ý: Mỗi gạch đầu dòng là một ý. 
                    
            Dưới đây là nội dung chương truyện:
            """
                {content}
            """
            '''
    
    return(dedent(prompt))    

def summarize(prompt : str) -> str:
    client = Client("Qwen/Qwen2-72B-Instruct")  
    result = client.predict(
		query=prompt,
		history=[],
		system="Bạn là một tiểu thuyết gia",
		api_name="/model_chat"
    )
    histories = result[1]
    respond = histories[0][1]
    return respond

# prompt = get_prompt('\\home\\tandattran772\\persional_project\\StoryGen\\data\\raw\\Cuốn Theo Chiều Gió\\Chương 20.txt')

# print(summary(prompt))

if __name__=='__main__':
    RAW_DATA_PATH = 'D:\\FPT\\AI\\Major5\\DPL302m\\Project\\StoryGen-main\\data\\raw'
    PROCESSED_DATA_PATH = 'D:\\FPT\\AI\\Major5\\DPL302m\\Project\\StoryGen-main\\data\\processed'
    chapter_paths = get_chaper_paths()
    for path in chapter_paths:
        book_title = path.split('\\')[-2]
        chapter_title = path.split('\\')[-1]
        
        # prompt = get_prompt(path)
        # summary = summarize(prompt)

        processed_book_dir = os.path.join(PROCESSED_DATA_PATH, book_title)
        if not os.path.exists(processed_book_dir):
            os.makedirs(processed_book_dir)

        processed_chapter_path = os.path.join(processed_book_dir, chapter_title)
        if not os.path.exists(processed_chapter_path):
            try:
                print(f'Process {book_title} {chapter_title}')
                prompt = get_prompt(path)
                summary = summarize(prompt)
                with open(processed_chapter_path, 'w', encoding='utf-8') as f:
                        f.write(summary)
                        print(f'{processed_chapter_path}')  
            except:
                print(f'Can not process {book_title} {chapter_title}')            
        else:
            print(f"There exists {processed_chapter_path}")              
        # break

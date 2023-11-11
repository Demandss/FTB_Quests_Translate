from deep_translator import GoogleTranslator
import re
import os

# 対象のフォルダパス
folder_path = "chapters"
# フォルダ内のすべてのファイルを取得
files = os.listdir(folder_path)
# .snbt ファイルのリスト
snbt_files = [file for file in files if file.endswith(".snbt")]

# 翻訳エンジンを選択
translator = GoogleTranslator(source='en', target='ja')

# 書き換えたい項目を追加するときはここに従って追加する。
# 正規表現による検索条件
pattern = r'(description|subtitle):\s*\[([^\]]*)\]'

# 置換する関数
def replace_function(match):
    # マッチした部分を取得し、カンマで分割してリストに変換
    text_list = [text.replace("\t","").strip('"') for text in match.group(2).split('\n')]
    translate_list =[]
    for eng in text_list:
        ja = ""
        ja = translator.translate(eng)
        translate_list.extend([ja,eng])
    
    # 新しいテキスト
    new_text = f'{match.group(1)}: [' + ''.join(f'"{new_text}"\n' for new_text in translate_list) + ']'
    
    return new_text

for snbt_file in snbt_files:
# ファイルのパス
    file_path = rf"{folder_path}/{snbt_file}"

    # ファイルの読み取り
    with open(file_path, "r",encoding="utf-8") as file:
        # ファイルの内容を読み込む
        content = file.read()

    # マッチした部分を置換
    result_text = re.sub(pattern, replace_function, content)

    # フォルダが存在しない場合は作成
    if not os.path.exists(f"changed_{folder_path}"):
        os.makedirs(f"changed_{folder_path}")


    # 書き込みモードでファイルを開く
    with open(f"changed_{file_path}", "w", encoding="utf-8") as output_file:
        # 修正されたテキストをファイルに書き込む
        output_file.write(result_text)




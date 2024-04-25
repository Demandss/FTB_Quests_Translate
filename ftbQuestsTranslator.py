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
translator = GoogleTranslator(source='en', target='ru')

# 書き換えたい項目を追加するときはここに従って追加する。
# 正規表現による検索条件
desc_pattern = r'description:\s*\[([^\]]*)\]'

# 置換する関数
def replace_desc(match):
    # マッチした部分を取得し、カンマで分割してリストに変換
    text_list = [text.replace("\t","")[1:-1] for text in match.group(1).split('\n')]
    translate_list =[]
    for eng in text_list:
        ru = ""
        if eng:#空の文字列でない場合
            if eng[0]=="{" and eng[-1]=="}":#画像の場合
                pass
            else:#画像でない場合
                ru = translator.translate(eng)

        translate_list.extend([ru])
    
    # 新しいテキスト
    new_text = f'description: [' + ''.join(f'\n"{new_text}"' for new_text in translate_list) + ']'

    print(f"    text:{new_text}")
    
    return new_text

for snbt_file in snbt_files:
# ファイルのパス
    print(snbt_file)
    file_path = rf"{folder_path}/{snbt_file}"

    # ファイルの読み取り
    with open(file_path, "r",encoding="utf-8") as file:
        # ファイルの内容を読み込む
        content = file.read()

    # マッチした部分を置換
    desc_text = re.sub(desc_pattern, replace_desc, content)

    # フォルダが存在しない場合は作成
    if not os.path.exists(f"changed_{folder_path}"):
        os.makedirs(f"changed_{folder_path}")

    # 書き込みモードでファイルを開く
    with open(f"changed_{file_path}", "w", encoding="utf-8") as output_file:
        # 修正されたテキストをファイルに書き込む
        output_file.write(desc_text)

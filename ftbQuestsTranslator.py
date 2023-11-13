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
desc_pattern = r'description:\s*\[([^\]]*)\]'
sub_pattern = r'subtitle:\s*(.*)'

# 置換する関数
def replace_desc(match):
    # マッチした部分を取得し、カンマで分割してリストに変換
    text_list = [text.replace("\t","")[1:-1] for text in match.group(1).split('\n')]
    translate_list =[]
    for eng in text_list:
        if eng and eng[0]=="{" and eng[-1]=="}":#画像の場合
            ja = ""
        else:#画像でない場合
            ja = translator.translate(eng).replace("'","").replace('"',"").replace("\\","")
        translate_list.extend([ja,eng])
    
    # 新しいテキスト
    new_text = f'description: [' + ''.join(f'"{new_text}"\n' for new_text in translate_list) + ']'
    
    return new_text
def replace_sub(match):
    # マッチした部分を取得し、カンマで分割してリストに変換
    eng = match.group(1).replace("\t","")[1:-1]

    ja = translator.translate(eng).translate(eng).replace("'","").replace('"',"").replace("\\","")

    
    # 新しいテキスト
    new_text = f'subtitle: "{ja} {eng}"'
    
    return new_text

for snbt_file in snbt_files:
# ファイルのパス
    file_path = rf"{folder_path}/{snbt_file}"

    # ファイルの読み取り
    with open(file_path, "r",encoding="utf-8") as file:
        # ファイルの内容を読み込む
        content = file.read()

    # マッチした部分を置換
    desc_text = re.sub(desc_pattern, replace_desc, content)
    result_text = re.sub(sub_pattern, replace_sub, desc_text)

    # フォルダが存在しない場合は作成
    if not os.path.exists(f"changed_{folder_path}"):
        os.makedirs(f"changed_{folder_path}")


    # 書き込みモードでファイルを開く
    with open(f"changed_{file_path}", "w", encoding="utf-8") as output_file:
        # 修正されたテキストをファイルに書き込む
        output_file.write(result_text)




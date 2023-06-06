import os
import shutil

def move(path='download'):
    """
    Move os arquivos do extras para a pasta Download
    """
    source = "rfb/extras"
    
    files = os.listdir(source)
    print(files)
    for fname in files:
        shutil.copy2(os.path.join(source,fname), path)
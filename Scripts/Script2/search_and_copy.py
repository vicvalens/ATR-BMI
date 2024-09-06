import os
import shutil

def search_and_copy(directory):
    
    source=""
    for filename in os.listdir(directory):
        if filename.endswith(".csv") and 'fishing' in filename:
            source = os.path.join(directory, filename)
            break
    else:
        print('No CSV file containing "fishing" found in the directory')
    return source

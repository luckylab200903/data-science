def read_files(file_paths):
    file_contents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            file_contents.append(file.read())
    return file_contents

# List of file paths
file_paths = ['StopWords_Auditor.txt', 'StopWords_Currencies.txt', 'StopWords_DatesandNumbers.txt','StopWords_Generic.txt','StopWords_GenericLong.txt','StopWords_Geographic.txt','StopWords_Names.txt']

file_contents = read_files(file_paths)

final_content = []

# Concatenate contents of all files and convert to lowercase
for content in file_contents:
    final_content.extend(content.lower().split())  # Split content into words, convert to lowercase, and add them to final_content

print(final_content)

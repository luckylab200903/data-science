from pathlib import Path
import nltk
import syllables
import os
import pandas as pd
import string
import re



## Function to read positive words from the dictionary ##
def positive_text():
    with open(r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\MasterDictionary\positive-words.txt", "r") as f:
        text = f.read()
    return text

positive_contents = positive_text()
positive_words_list = positive_contents.split()

## Function to read negative words from the dictionary ##
def negative_text():
    with open(r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\MasterDictionary\negative-words.txt", "r") as f:
        text = f.read()
    return text

negative_contents = negative_text()
negative_words_list = negative_contents.split()

# Function to read STOPWORDS different files

def read_files(file_paths):
    file_contents = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            file_contents.append(file.read())
    return file_contents
file_paths = [r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_Auditor.txt', r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_Currencies.txt',
        r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_DatesandNumbers.txt',r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_Generic.txt',r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_GenericLong.txt',r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_Geographic.txt',r'C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\StopWords\StopWords_Names.txt']

file_contents = read_files(file_paths)

stopwords = []

for content in file_contents:
    stopwords.extend(content.lower().split()) 


def read_text(file_path, stopwords_set):
    with open(file_path, 'r',encoding="utf-8") as f:
        text = f.read()
        words = text.split()
        words_without_stopwords = [word for word in words if word.lower() not in stopwords_set]
        text = ' '.join(words_without_stopwords)  
    return text
file_path = r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\urldataextract\urldataextract\spiders\files\blackassign0001.txt"
cleaned_text = read_text(file_path, stopwords)

def remove_stop_words(text, stop_words):
    filtered_text = [word for word in text.split() if word.lower() not in stop_words]
    return filtered_text

final_text = remove_stop_words(cleaned_text, stopwords)


## function to grap positive words present in the text file and also the dictionary provided in masterdictionary ##
def grab_positive_words(final_text, positive_words_list):
    positive_words_in_text = [word for word in final_text if word.lower() in positive_words_list]
    return positive_words_in_text


positive_words = grab_positive_words(final_text, positive_words_list)

## function to grap negative words present in the text file and also the dictionary provided in masterdictionary ##

def grab_negative_words(final_text, negative_words_list):
    negative_words_in_text = [word for word in final_text if word.lower() in negative_words_list]
    return negative_words_in_text


negative_words = grab_positive_words(final_text, negative_words_list)


final_dictionary=positive_words+negative_words



##  Function to remove stopwords ##

def remove_stop_words(text, stop_words):
    filtered_text = [word for word in text.split() if word.lower() not in stop_words]
    return filtered_text

## Function to count sentences ##
def count_sentences(text):
    sentences = nltk.sent_tokenize(text)
    num_sentences = len(sentences)
    return num_sentences

## Function to remove the , . and other puncuations to get the refined text file ##
def tokenize(final_text):
    ignore_chars = set(string.punctuation) - {',', '.'}
    tokens = [token for word in final_text for token in nltk.word_tokenize(word) if token not in ignore_chars]
    
    return tokens

token_final = tokenize(final_text)

## Function to get the positive score ##

def positive_count(token_final, positive_words):
    positive_tokens = [word for word in token_final if word in positive_words]
    return positive_tokens

positive_tokens = positive_count(token_final, positive_words)

## Function to get the negative score ##

def negative_count(token_final, positive_words):
    negative_tokens = [word for word in token_final if word in negative_words]
    return negative_tokens


negative_tokens = negative_count(token_final, negative_words)



## Function to calculate fog index ##

def calculate_fog_index(average_sentence_length, percentage_of_complex_words):
    fog_index = 0.4 * (average_sentence_length + percentage_of_complex_words)
    return fog_index

## Function to get the list of complex words present in my file##

def complex_word(text_final):
    complex_words =set()
    for word in text_final.split():
        if syllables.estimate(word) == 2:
            complex_words.add(word)
    return complex_words
complex_count=complex_word(cleaned_text)


## Function to calculate the character count in the text file##
def word_length(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()
        char_count = sum(1 for char in content if char != ' ')
        return char_count
    
##Function to calculate the personal pronoun I have included all the pronouns##
def personal_pronoun(file_path):
    with open(file_path, "r", encoding='utf-8') as f:
        response = f.read()
        pronoun_count = len(re.findall(r'\b(I|you|he|she|it|we|they|me|him|her|us|them|myself|yourself|himself|herself|itself|ourselves|yourselves|themselves|mine|yours|his|hers|its|ours|theirs)\b', response, re.IGNORECASE))
        return pronoun_count
pronoun_count = personal_pronoun(file_path)

##Function to calculate the count of syllables present in a single word##
def count_syllables(word):
    vowels = "aeiouy"
    count = 0
    endings = ["es", "ed"]
    if any(word.endswith(e) for e in endings):
        word = word[:-2] 
    for i in range(len(word)):
        if word[i] in vowels and (i == 0 or word[i - 1] not in vowels):
            count += 1
    if word.endswith('e') and count > 1:
        count -= 1
    
    return max(count, 1)  
##Function to calculate the total syllables present in different files and text present in the files##
def calculate_syllables_from_file(file_path):
    with open(file_path, "r", encoding='utf-8') as file:
        text = file.read()
        words = text.split()
        syllable_count_per_word = {word: count_syllables(word) for word in words}
        return syllable_count_per_word


syllable_count_per_word = calculate_syllables_from_file(file_path)

syllables_dict = {} 
total_syllables = 0
for word, syllable_count in syllable_count_per_word.items():
    syllables_dict[word] = syllable_count
    total_syllables += syllable_count

##Function to process single file ##
def process_file(file_path, stopwords):
    cleaned_text = read_text(file_path, stopwords)
    final_text = remove_stop_words(cleaned_text, stopwords)
    positive_words = grab_positive_words(final_text, positive_words_list)
    negative_words = grab_negative_words(final_text, negative_words_list)
    token_final = tokenize(final_text)
    positive_tokens = positive_count(token_final, positive_words)
    negative_tokens = negative_count(token_final, negative_words)
    num_sentences = count_sentences(cleaned_text)
    word_count = len(final_text)
    average_sentence_length = word_count / num_sentences
    percentage_of_complex_words = len(complex_word(cleaned_text)) / word_count
    fog_index = calculate_fog_index(average_sentence_length, percentage_of_complex_words)
    character_count = word_length(file_path)
    average_word_length = character_count / word_count
    positive_word_count = len(grab_positive_words(final_text, positive_words_list))
    negative_word_count = len(grab_negative_words(final_text, negative_words_list))
    complex_count = len(complex_word(cleaned_text))
    personal_pro = personal_pronoun(file_path)
    syllables=calculate_syllables_from_file(file_path)
    subjective_score = (positive_word_count + negative_word_count) / (word_count + 0.000001)
## Value it is returning ##
    return {
        "num_sentences": num_sentences,
        "word_count": word_count,
        "average_sentence_length": average_sentence_length,
        "fog_index": fog_index,
        "character_count": character_count,
        "average_word_length": average_word_length,
        "positive_score": len(positive_tokens),
        "negative_score": len(negative_tokens),
        "polarity_score": (len(positive_tokens) - len(negative_tokens)) / (len(positive_tokens) + len(negative_tokens) + 0.00001),
        "subjective_score": subjective_score,
        "percentage_complex_words": percentage_of_complex_words,
        "complex_count": complex_count,
        "personal_pronoun": personal_pro,
        "avg_word_length":average_word_length,
        "syllables":syllables
    }

path = r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\urldataextract\urldataextract\spiders\files"
dir_list = os.listdir(path)

websites_list = dir_list  

base_path = r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\urldataextract\urldataextract\spiders\files"
excel_file_path = r"C:\Users\KESHAV KUMAR SINGH\Desktop\internshala\internshala\urldataextract\urldataextract\spiders\output.xlsx"  
websites_list = os.listdir(base_path)


data = []
## Looping over different files to get the desired output##

for website in websites_list:
    file_path = os.path.join(base_path, website)
    result = process_file(file_path, stopwords)
    data.append({
        "File": website,
        "POSITIVE SCORE": result["positive_score"],
        "NEGATIVE SCORE": result["negative_score"],
        "POLARITY SCORE": result["polarity_score"],
        "SUBJECTIVITY SCORE": result["subjective_score"],
        "AVERAGE SENTENCE LENGTH": result["average_sentence_length"],
        "PERCENTAGE OF COMPLEX WORDS": result["percentage_complex_words"] * 100,
        "Fog Index": result["fog_index"],
        "Average word length": result["average_word_length"],
        "COMPLEX WORD COUNT": result["complex_count"],
        "WORD COUNT": result["word_count"],
        "SYLLABLE PER WORD": result.get("syllables", 0),
        "PERSONAL PRONOUN": result["personal_pronoun"],  
        "AVERAGE WORD LENGTH": result["average_word_length"],
    })

## Convert the list of dictionaries to a DataFrame ##
df = pd.DataFrame(data)

## Save the DataFrame to an Excel file ##
df.to_excel(excel_file_path, index=False)

print("Data saved to Excel file:", excel_file_path)






















































































































































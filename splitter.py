from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy
import json
# nlp = spacy.load("en_core_web_sm")


def chunk_split(text, chunk_size=50, chunk_overlap=20):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)

# def sentence_split(text):
#     doc = nlp(text)
#     return [sent.text for sent in doc.sents]


def load_json(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data


def process_json(data):
    new_data = []
    for entry in data:
        description = entry['description']
        chunks = chunk_split(description)
        for chunk in chunks:
            new_entry = {
                'title': entry['title'],
                'code': entry['code'],
                'chunk': chunk
            }
            new_data.append(new_entry)
    return new_data


def save_json(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)


if __name__ == '__main__':
    data = load_json('short_test.json')
    processed_data = process_json(data)
    print(processed_data)
    save_json(processed_data, 'processed_short.json')
    print('Data processing complete.')

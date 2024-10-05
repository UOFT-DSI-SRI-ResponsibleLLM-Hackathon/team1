from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy
import json
nlp = spacy.load("en_core_web_sm")


class TextSplitter:
    def __init__(self, chunk_size=100, chunk_overlap=0, raw_data=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if raw_data:
            self.raw_data = raw_data
        self.processed_data = None
        self.chunks = None
        self.descriptions = None

    def chunk_split(self, text):
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return splitter.split_text(text)

    def sentence_split(self, text):
        doc = nlp(text)
        return [sent.text for sent in doc.sents]

    def load_json(self, file_name):
        with open(file_name, 'r') as file:
            self.raw_data = json.load(file)

    def process_json(self):
        new_data = []
        all_chunks = []
        for entry in self.raw_data:
            description = entry['description']
            chunks = self.sentence_split(description)
            all_chunks.extend(chunks)
            for chunk in chunks:
                new_entry = {
                    'title': entry['title'],
                    'code': entry['code'],
                    'chunk': chunk
                }
                new_data.append(new_entry)
        self.processed_data = new_data
        self.chunks = all_chunks

    def save_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.processed_data, file)

    def get_descriptions(self):
        descriptions = []
        for entry in self.raw_data:
            title = entry["title"]
            code = entry["code"]
            description = entry['description']
            combined_info = code + title + description
            descriptions.append(combined_info[:512])
        self.descriptions = descriptions


if __name__ == '__main__':
    splitter = TextSplitter(chunk_size=50, chunk_overlap=20)
    splitter.load_json('short_test.json')
    splitter.process_json()
    splitter.save_json('processed_short.json')

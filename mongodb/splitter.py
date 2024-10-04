from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
import nltk

nltk.download('punkt_tab')


class TextSplitter:
    def __init__(self, chunk_size=100, chunk_overlap=0, raw_data=None):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        if raw_data:
            self.raw_data = raw_data
        self.processed_data = None
        self.chunks = None

    def chunk_split(self, text):
        splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
        return splitter.split_text(text)

    # def sentence_split(self, text):
    #     doc = nlp(text)
    #     return [sent.text for sent in doc.sents]
    
    def sentence_split(self, text, max_sentences=1):
        """
        Split text into chunks of a maximum number of sentences.
        """
        sentences = nltk.sent_tokenize(text)
        return [' '.join(sentences[i:i+max_sentences]) for i in range(0, len(sentences), max_sentences)]

    def load_json(self, file_name):
        with open(file_name, 'r') as file:
            self.raw_data = json.load(file)

    def process_json(self):
        new_data = []
        all_chunks = []
        index = 0
        for entry in self.raw_data:
            description = entry['description']
            chunks = self.sentence_split(description)
            all_chunks.extend(chunks)
            for chunk in chunks:
                new_entry = {
                    'index': index,
                    'title': entry['title'],
                    'code': entry['code'],
                    'chunk': chunk,
                    'description': description
                }
                new_data.append(new_entry)
                index += 1
        self.processed_data = new_data
        self.chunks = all_chunks

    def save_json(self, file_name):
        with open(file_name, 'w') as file:
            json.dump(self.processed_data, file)


if __name__ == '__main__':
    splitter = TextSplitter(chunk_size=50, chunk_overlap=20)
    splitter.load_json('short_test.json')
    splitter.process_json()
    splitter.save_json('processed_short.json')

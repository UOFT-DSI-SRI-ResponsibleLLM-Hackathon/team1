from langchain.text_splitter import RecursiveCharacterTextSplitter
import spacy


def chunk_split(text, chunk_size=500, chunk_overlap=50):
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return splitter.split_text(text)


nlp = spacy.load("en_core_web_sm")

def sentence_split(text):
    doc = nlp(text)
    return [sent.text for sent in doc.sents]


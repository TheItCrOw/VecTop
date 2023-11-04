# see: https://huggingface.co
from transformers import AutoTokenizer, MarianMTModel
import requests
import spacy
import pytextrank
import re
import json
import psycopg
import sys
import traceback


class translator:

    def __init__(self):
        self.nlp = spacy.load("de_core_news_sm")

    def clean_text(self, text):
        # We want to cleanup the text a bit.
        text = text.replace("\n", "").replace("\r", "")
        text = re.sub(' +', ' ', text)
        return text

    def translate_german_to_english(self, text):
        text = self.clean_text(text)
        # https://huggingface.co/Helsinki-NLP/opus-mt-de-en
        src = "de"  # source language
        trg = "en"  # target language

        model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # We tokenize the text and translate each sentence in the
        # opus-mt model.
        tokens = self.nlp(text)
        result = ""
        for sentence in tokens.sents:
            sentence = str(sentence)
            batch = tokenizer(sentence, return_tensors="pt")

            generated_ids = model.generate(**batch)
            result += tokenizer.batch_decode(generated_ids,
                                             skip_special_tokens=True)[0]
            result += " "
        return result

    def translate_english_to_german(self, text):
        self.text = clean_text(text)
        # https://huggingface.co/Helsinki-NLP/opus-mt-de-en
        src = "en"  # source language
        trg = "de"  # target language

        model_name = f"Helsinki-NLP/opus-mt-{src}-{trg}"
        model = MarianMTModel.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        batch = tokenizer(text, return_tensors="pt")

        generated_ids = model.generate(**batch)
        return tokenizer.batch_decode(generated_ids,
                                      skip_special_tokens=True)[0]

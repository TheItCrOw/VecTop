<div align="center">
  <img src="https://github.com/TheItCrOw/VecTop/assets/49918134/17060134-5891-464b-be97-47c095d4a719"/>
  <hr/>
  <h1>Vector Database for Topic Extraction using Contextualized Word Embeddings</h1>
</div

[![License](https://img.shields.io/badge/Status-Under%20construction-red)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# About

VecTop is a corpus of contextualized word embeddings labeled with topics and sub-topics. The cosine similarity predicts the topic and sub-topic labels by identifying the topics that are most closely related to the text that is being extracted from. It is therefore possible to automatically extract the topics of an unkown text and label it. 

# Language Support

I use Cross-Lingual Word Embeddings which offer usages for multiple languages. As off now, VecTop supports the following languages:<br/>
:green_circle: German <br/>
:green_circle: English <br/>

# Topics

The following topics and their subtopics are used by VecTop to label texts (german | english):

* Politik | Politics :classical_building:
  <details>
    <summary>Subtopics</summary>
      Bundesregierung | Federal Government <br/>
      Bundestag | Parliament <br/>
  </details>
* Ausland | Foreign :earth_asia:
  <details>
    <summary>Subtopics</summary>
  USA <br/>
  Europa | Europe <br/>
  Nahost | Middle East <br/>
  Globale Gesellschaft | Global Society <br/>
  Asien | Asia <br/>
  Afrika | Africa <br/>
  </details>
* Panorama :sunrise_over_mountains:
  <details>
    <summary>Subtopics</summary>
  Justiz & Kriminalität | Law & Crime <br/>
  Leute | People <br/>
  Gesellschaft | Society <br/>
  Bildung | Education <br/>
  </details>
* Sport :football:
  <details>
    <summary>Subtopics</summary>
  Ergebnisse & Tabellen | Results and Tables <br/>
  Liveticker <br/>
  Fußball | Soccer <br/>
  Bundesliga <br/>
  Champions League <br/>
  Formel 1 | Formular 1 <br/>
  Wintersport | Winter Sports <br/>
  </details>
* Wirtschaft | Economy :moneybag:
  <details>
    <summary>Subtopics</summary>
  Börse | Stock Market <br/>
  Verbraucher & Service | Consumers & Service <br/>
  Versicherungen | Insurance <br/>
  Unternehmen & Märkte | Companies & Markets <br/>
  Staat & Soziales | State & Social <br/>
  </details>
* Wissenschaft | Science :telescope:
  <details>
    <summary>Subtopics</summary>
  Klimakrise | Global Warming <br/>
  Mensch | Human <br/>
  Natur | Nature <br/>
  Technik | Technology <br/>
  Weltall | Space <br/>
  Medizin | Medicine <br/>
  </details>
* Netzwelt | Network World :globe_with_meridians:
  <details>
    <summary>Subtopics</summary>
  Netzpolitik | Network Politics <br/>
  Web <br/>
  Gadgets <br/>
  Games <br/>
  Apps <br/>
  </details>
* Kultur | Culture :world_map:
  <details>
    <summary>Subtopics</summary>
  Kino | Cinema <br/>
  Musik | Music <br/>
  TV <br/>
  Literatur | Literature <br/>
  </details>
* Leben | Life :couple:
  <details>
    <summary>Subtopics</summary>
  Reise | Trip <br/>
  Stil | Style <br/>
  Gesundheit | Health <br/>
  Familie | Family <br/>
  Psychologie | Psychology <br/>
  </details>

# German Corpus V1
![german_v1_channels](https://github.com/TheItCrOw/VecTop/assets/49918134/01602db2-2a1f-4406-9157-cfe6855ce136)

Version 1 of the German Summarized Spiegel Embeddings Corpus is now available for download and usage. This version contains >200k articles (2017-10-01 -> 2023-10-23) which have been firstly summarized with TextRank and then embedded with OpenAI's ```text-embedding-ada-002```. Testing VecTop on 100 speeches of the German Parliament to extract topics showed a **98%** correctness on main topics and **93%** correctness on subtopics.

## Usage

* [Download](https://www.kaggle.com/datasets/kevinbnisch/vectordb-for-topic-extraction-with-word-embeddings/data) the Corpus
* Import the .sql into a PostgresSQL database with the [pgVector](https://github.com/pgvector/pgvector) extension installed.
  - You can of course import the corpus into any DB of your liking, just make sure the DB can handle vectors.
  - As an alternative, the corpus can also be downloaded as a .csv file.
* Clone the repository ```git clone https://github.com/TheItCrOw/VecTop.git```
* Install the requirements ```pip install -r requirements.txt```
* See ```in_medias_res.py``` for an example and usage of the ```vectop.py``` class.
  - Change the ```get_connection_string()``` and ```get_openai_api_key()``` to return your personal connection string and openAI api key. The connection string has to be a PostgresSQL connectionstring format: ```postgresql://user:pw@host:port/database```
* Extract Topics!

🟥 **This is a first version of the VecTop corpus which hasn't been evaluated thoroughly yet.** 🟥

# English Corpus V1

Coming soon.



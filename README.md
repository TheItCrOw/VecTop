<div align="center">
  <img src="https://github.com/TheItCrOw/VecTop/assets/49918134/17060134-5891-464b-be97-47c095d4a719"/>
  <hr/>
  <h1>Vector Database for Topic Extraction using Contextualized Word Embeddings</h1>
</div

[![License](https://img.shields.io/badge/Status-Under%20construction-red)]()
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

# About

VecTop is a corpus of contextualized word embeddings labeled with topics and sub-topics. The cosine similarity predicts the topic and sub-topic labels by identifying the topics that are most closely related to the text that is being inserted. It is therefore possible to automatically extract the topics of an unkown text and label it.

**Right now, the corpus currently only contains german text and embeddings, but I plan to add support for topic extraction in English as well.**

# Topics

The following topics and their subtopics are used by VecTop to label texts (german | english):

* Politik | Politics
  <details>
    <summary>Subtopics</summary>
      Bundesregierung | Federal Government <br/>
      Bundestag | Parliament <br/>
  </details>
* Ausland | Foreign
  <details>
    <summary>Subtopics</summary>
  USA <br/>
  Europa | Europe <br/>
  Nahost | Middle East <br/>
  Globale Gesellschaft | Global Society <br/>
  Asien | Asia <br/>
  Afrika | Africa <br/>
  </details>
* Panorama
  <details>
    <summary>Subtopics</summary>
  Justiz & Kriminalität | Law & Crime <br/>
  Leute | People <br/>
  Gesellschaft | Society <br/>
  Bildung | Education <br/>
  </details>
* Sport
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
* Wirtschaft | Economy
  <details>
    <summary>Subtopics</summary>
  Börse | Stock Market <br/>
  Verbraucher & Service | Consumers & Service <br/>
  Versicherungen | Insurance <br/>
  Unternehmen & Märkte | Companies & Markets <br/>
  Staat & Soziales | State & Social <br/>
  </details>
* Wissenschaft | Science <br/>
  <details>
    <summary>Subtopics</summary>
  Klimakrise | Global Warming <br/>
  Mensch | Human <br/>
  Natur | Nature <br/>
  Technik | Technology <br/>
  Weltall | Space <br/>
  Medizin | Medicine <br/>
  </details>
* Netzwelt | Network World
  <details>
    <summary>Subtopics</summary>
  Netzpolitik | Network Politics <br/>
  Web <br/>
  Gadgets <br/>
  Games <br/>
  Apps <br/>
  </details>
* Kultur | Culture
  <details>
    <summary>Subtopics</summary>
  Kino | Cinema <br/>
  Musik | Music <br/>
  TV <br/>
  Literatur | Literature <br/>
  </details>
* Leben | Life
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

Version 1 of the German Summarized Spiegel Embeddings Corpus is now available for download and usage. This version contains >200k articles which have been firstly summarized with TextRank and then embedded with OpenAI's ```text-embedding-ada-002```. Testing VecTop on 100 speeches of the German Parliament to extract topics showed a **98%** correctness on main topics and **93%** correctness on subtopics.

## Usage

* Download the Corpus
* Import the .csv into a PostgresSQL database with the [pgVector](https://github.com/pgvector/pgvector) extension installed.
* Clone the repository ```git clone https://github.com/TheItCrOw/VecTop.git```
* Install the requirements ```pip install -r requirements.txt```
* See ```in_medias_res.py``` for an example and usage of the ```vectop.py``` class
  - Change the ```get_connection_string()``` and ```get_openai_api_key()``` to return your personal connection string and openAI api key. The connection string has to be a PostgresSQL connectionstring format: ```postgresql://user:pw@host:port/database```
* Extract Topics!

🟥 This is a first version of the VecTop corpus which hasn't been evaluated thoroughly yet. 🟥

# English Corpus V1

Coming soon.



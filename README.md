<div align="center">
  <img src="https://github.com/TheItCrOw/VecTop/assets/49918134/6b65222e-04ee-4fba-8c97-79dcf272cc8a"/>
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

# Corpus

I'm constantly expanding the VecTop corpus. As of right now, I've scraped Spiegel-Online articles and their categories as a basis for labeled texts. I utilize OpenAI's text-embedding-ada-002 for word embedding. These vectors are stored in a PostgresSQL database with the extension for vector databases included. **Currently, the corpus has approximately 1 million word embeddings, each representing a fragment of text alongside annotated topics.**



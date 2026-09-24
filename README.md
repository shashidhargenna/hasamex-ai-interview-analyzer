# Hasamex AI Engineer Technical Case Study

## Overview

This project is my solution for the Hasamex AI Engineer technical case study.

The application analyzes three expert interviews about the European robotic surgery market and uses the provided interview guide to generate insights from the transcripts.

The main focus of the application is to provide answers that are grounded in the interview data and can be traced back to the original transcripts through exact quotes, expert names, markets, and timestamps.

## Problem Statement

The case study requires analyzing three expert-call transcripts along with an interview guide.

The application is designed to:

- Answer the questions provided in the interview guide
- Extract supporting quotes from the transcripts
- Show the timestamps for the supporting evidence
- Identify common themes across the interviews
- Identify differences and disagreements between experts
- Allow users to ask additional questions across all three transcripts

## Features

## Interview Guide Analysis

The application answers the six questions provided in the interview guide.

For each question, it provides:

- A concise answer
- Supporting evidence
- Expert name
- Market
- Timestamp
- Exact transcript quote
- Segment ID

### Ask Across Transcripts

Users can ask their own questions about the three expert interviews.

For example:

** What are the main barriers to robotic surgery adoption?

The system retrieves relevant transcript segments and generates an answer using the retrieved evidence.

The supporting transcript segments are also displayed so that the answer can be traced back to the source.

### Themes & Differences

The application analyzes the interview evidence to identify:

- Common themes
- Differences between expert perspectives
- Differences in expected adoption
- Differences in decision-making timelines

The analysis is based on the information retrieved from the transcripts.

# Architecture

The application uses a simple Retrieval-Augmented Generation (RAG) architecture.

Expert Transcript Files
        |
        v
Timestamp-aware Ingestion
        |
        v
Transcript Segmentation
        |
        v
LangChain Documents
        |
        v
OpenAI Embeddings
        |
        v
Pinecone Vector Database
        |
        v
Semantic Retrieval
        |
        v
Filter Interviewer Segments
        |
        v
GPT-4o-mini
        |
        v
Answer + Supporting Evidence


The basic flow is:

1. Read and parse the transcripts.
2. Split the transcripts into timestamp-based segments.
3. Convert the segments into LangChain documents.
4. Generate embeddings using OpenAI.
5. Store the embeddings in Pinecone.
6. Retrieve relevant transcript segments for a user question.
7. Filter out interviewer segments.
8. Provide the retrieved evidence to GPT-4o-mini.
9. Return the answer together with supporting transcript evidence.

## Technology Stack

* Python
* LangChain
* OpenAI
* Pinecone
* Streamlit
* Python Dotenv

## Models

Embedding model

 text-embedding-3-small

Language model

 gpt-4o-mini



## Project Structure

 AI_CASE_STUDY_ASSIGNMENT/
│
├── data/
│   ├── Interview_Guide.txt
│   ├── Transcript_1_France.txt
│   ├── Transcript_2_Germany.txt
│   └── Transcript_3_UK.txt
│
├── src/
│   ├── chunking.py
│   ├── embeddings.py
│   ├── guide_analysis.py
│   ├── ingestion.py
│   ├── models.py
│   ├── qa.py
│   ├── retrieval.py
│   └── theme_analysis.py
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
└── test_*.py

### source Data

The application works with three expert interviews:

* France
* Germany
* United Kingdom

The project also contains the interview guide provided as part of the case study.

The transcript files are stored in the data/ directory.

Setup

1. Clone the Repository
  git clone <YOUR_GITHUB_REPOSITORY_URL>
  cd AI_CASE_STUDY_ASSIGNMENT

2. Create a Virtual Environment
   python -m venv .venv

Windows: .venv\Scripts\activate
linux/macos : source .venv/bin/activate

3. Install Dependencies
  pip install requirements.txt

## Environment Variables

Create a .env file in the project root.

Add the following:
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_INDEX_NAME=assignmenthasmex

## Running the Application

Start the Streamlit application using:

>> streamlit run app.py


After starting the application, Streamlit will provide a local URL where the application can be opened in a browser.


## Conclusion

This project provides a simple RAG-based workflow for analyzing the three expert interviews.

The application combines semantic retrieval with transcript-grounded generation while preserving the original expert, market, timestamp, and quote information needed to verify the generated insights.

The implementation is designed to be simple, traceable, and aligned with the requirements of the Hasamex AI Engineer technical case study.


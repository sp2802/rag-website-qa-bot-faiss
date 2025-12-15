# RAG-Based Website Q&A Bot

## Project Overview

This project implements an end-to-end Retrieval Augmented Generation (RAG) system that answers user questions strictly based on the content of a crawled website.

The system crawls the FastAPI documentation website, processes and indexes its content, and exposes REST APIs that allow users to ask questions and receive grounded, source-backed answers.

---

## Website Used for Crawling

https://fastapi.tiangolo.com

---

## Project Architecture

Crawl -> Clean -> Chunk -> Embed -> Vector DB -> Retrieve -> Answer

---

## Setup Instructions

1. Create virtual environment
python -m venv venv

2. Activate environment
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)

3. Install dependencies
pip install -r requirements.txt

4. Run server
python run.py

---

## Demo Questions

- What is FastAPI?
- What are the main features of FastAPI?
- How does FastAPI handle data validation?
- What is ASGI and how does FastAPI use it?
- Who is the Prime Minister of India?

---

## Technologies Used

Python, FastAPI, FAISS, Sentence Transformers, BeautifulSoup

# TheSocraticTutor
The Socratic tutor leverages Google AI and Cloud Suite to be able to provide a fast, smart, and scalable AI tutor solution for teachers and students worldwide. 
AI Document Platform

This project is a Flask-based web app for uploading PDF documents and querying them using Google’s AI Search Widget.

Features

Upload PDF textbooks and course materials.

Query your knowledge base using the AI Search Widget.

Reset the knowledge base.

Real-time indexing with Google Cloud Storage.

Prerequisites

Python 3.9+

Flask

Google Cloud credentials for your Data Store

ngrok (for local testing with AI Widget)

Setup & Run

Clone the repository

git clone <your-repo-url>
cd <your-repo-folder>


Install dependencies

pip install -r requirements.txt


Run the Flask app locally

flask run


By default, it runs on http://127.0.0.1:5000.

Expose local app via ngrok (required for AI widget)

ngrok http 5000


Copy the https:// URL from ngrok.

Add it to allowed origins in your Google Gen App Builder widget configuration.

Open the app

Access the app in your browser via the ngrok URL.

Upload PDFs and use the search widget.

Usage

Upload documents: Click or drag PDFs into the left panel and click “Upload Document”.

Query knowledge base: Click the search bar on the right panel to launch the AI Search Widget.

Reset knowledge base: Click “Reset Knowledge Base” to clear all uploaded documents.

Notes

Keep ngrok running while testing locally.

Each ngrok session generates a new URL; update the widget allowed origins if the URL changes.

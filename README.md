# FastAPI OCR Project (hw_4nov)

Hello :) This pet-project demonstrates how to build a robust and scalable OCR (Optical Character Recognition) system using FastAPI, Docker, and Celery. With this project, you can easily upload documents, extract text from them using OCR, and store the extracted text in a database.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Installation](#installation)
 
## Project Overview

The FastAPI OCR Project is designed to provide a seamless and efficient way to process and analyze documents using OCR technology. It utilizes FastAPI for building the API, Docker for containerization, and Celery for task queueing and asynchronous processing.

## Features

- **Document Upload:** Users can upload documents to the server, which are then stored and processed.
- **OCR Text Extraction:** The project employs OCR techniques to extract text from uploaded documents.
- **Database Storage:** Extracted text is stored in a PostgreSQL database for easy retrieval and analysis.
- **Asynchronous Processing:** Celery is used to offload time-consuming OCR tasks, ensuring smooth performance.
- **API Endpoints:** A set of well-defined API endpoints allows users to interact with the system.


### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fastapi-ocr-project.git
   cd fastapi-ocr-project

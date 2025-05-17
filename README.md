# Semantic Router for Student Support Services

This project implements a two-layer semantic router designed to classify student queries and route them to appropriate support resources within NYU’s EG-UY 1004 curriculum. It supports both academic assistance and mental health services by leveraging natural language understanding.

## Project Overview

The router identifies and categorizes free-text student queries into one of several domains:
- Progress Reporting
- Problem Solving
- Material Information
- Mental Health Support

Queries are classified using OpenAI embeddings and matched against a curated set of utterances. A rerouting system ensures fallback handling and semantic reshaping when misclassifications or ambiguities occur.

## Evolution of the Project

### Iteration 1: Basic Semantic Routing
- Built using `semantic-router` and `OpenAIEncoder`
- Defined four core support routes and a single-layer routing mechanism
- Implemented rerouting logic with query reshaping and context preservation
- Delivered static responses for each route to simulate expert guidance

### Iteration 2: Modular Two-Layer Router
- Refactored into a modular class-based system using asynchronous handlers
- Integrated backend services for dynamic document retrieval via vector similarity search
- Added OpenAI-powered response generation using Langchain
- Organized all utterances and prompts into clean, modular components

## My Contributions

- Designed and implemented the rerouting system with context tracking and reshaping
- Built the full first iteration router with all expert logic and fallback mechanisms
- Led the transition to the two-layer architecture with asynchronous support
- Integrated the router with a vector database and GPT-based response generation system

## Skill Utlization

- Python 3
- semantic-router
- OpenAI GPT (via Langchain)
- Vector similarity search
- AsyncIO, logging, modular architecture

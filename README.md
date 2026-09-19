# Nugen Job Intelligence

A domain aligned resume and job description evaluation system built using Nugen Intelligence, FastAPI, Streamlit, and deterministic validation.

## Problem

General language models can sometimes infer skills that are not explicitly supported by a resume.

For example:

A candidate may list Python, while the model incorrectly assumes experience with Django or Flask.

The objective of this project was to build a more evidence based resume evaluation system that reduces unsupported skill assumptions.

## Solution

The system combines:

1. A domain aligned Nugen model
2. Domain specific training documents
3. Custom benchmark questions
4. Prompt based evaluation
5. Deterministic Python validation
6. FastAPI backend
7. Streamlit frontend

## Architecture

```text
Resume + Job Description
          |
          v
Nugen Domain Aligned Model
          |
          v
AI Based Analysis
          |
          v
Deterministic Skill Validation
          |
          v
Matched / Missing Skills
          |
          v
Recommendations
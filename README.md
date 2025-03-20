# Multi-Agent LLM System Failure Educator

This project implements an AI agent designed to educate users on why multi-agent LLM systems fail. The system includes:

- **Comprehensive Taxonomy:** A complete taxonomy of 14 failure modes organized into 3 categories, based on the MASFT taxonomy from UC Berkeley.
- **Interactive Demonstrations:** Realistic example scenarios that show how each failure mode manifests in practice.
- **PhD-Level Analysis:** Detailed, expert-level analysis on the causes of these failure modes.
- **Solution Recommendations:** Both tactical and structural solutions to address each failure mode.

The development of this repository was inspired by the paper "Why Do Multi-Agent LLM Systems Fail?". To read the entire paper, visit https://arxiv.org/pdf/2503.13657

## Features

* Interactive GUI for exploring AI multi-agent failure modes and solutions
* Comprehensive database of failure modes organized by category
* Detailed demos, PhD-level analysis, and solutions for each failure mode
* Natural language query interface
* SQLite database tracking of user interactions and preferences
* Rich educational content based on MASFT taxonomy from UC Berkeley research

## Directory Structure

```
Multi-Agents LLMs Failure/
├── app.py                 # Main application using a Tkinter GUI
├── agent.py               # AI Agent implementation
├── database.py             # SQLite database manager for storing interaction data
├── data/
│   └── failure_modes.json # JSON database with MASFT taxonomy data
├── educator.db             # SQLite database for storing user interactions
├── .windsurfrules         # Windsurf rules for the project (empty file)
└── README.md              # This README file
```

## Setup and Running

1. **Python Environment:**
   
   Create and activate a virtual environment:
   
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

2. **Install Dependencies:**
   
   This project uses only the standard Python library (Tkinter for GUI).

3. **Run the Application:**
   
   ```bash
   python app.py
   ```

   The application window will open, allowing you to interact with the AI agent.

   ![image](https://github.com/user-attachments/assets/c1ba9f31-80f4-48bd-81e0-f223b678e04d)
   ![image](https://github.com/user-attachments/assets/1ccb12da-b981-49cf-beae-6d9385de53fb)
   ![image](https://github.com/user-attachments/assets/ba32d349-ca31-4fda-82e2-4ed5e75ea8fe)
   ![image](https://github.com/user-attachments/assets/3f455701-c272-4f17-8ab4-0a07c1b1b77e)


## Usage Instructions

- **Interactive Mode:** Use the query box to ask about specific failure modes (e.g., "Show me an example of information withholding") or categories (e.g., "Explain inter-agent misalignment").
- **Categories Tab:** Browse through the failure categories and see detailed descriptions and associated failure modes.
- **Failure Modes Tab:** Select a category and a failure mode to view its description, demonstration, PhD-level analysis, and proposed solutions.

## Project Guidelines

- **Embedded Database:** The project includes an embedded JSON database for failure modes directly in the project directory.
- **Directory Structure:** Files are organized by their respective roles, following the project guidelines.
- **Future Enhancements:** You can extend the database by updating `data/failure_modes.json` with more failure modes or more detailed information.

## Acknowledgments

This system is based on the Multi-Agent System Failure Taxonomy (MASFT) from UC Berkeley research.

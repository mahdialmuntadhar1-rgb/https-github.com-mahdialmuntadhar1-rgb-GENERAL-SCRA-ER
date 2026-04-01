# Iraq University Data Platform - Admin Control

This project is a dual-interface data management system for the Iraq University Platform.

## 1. Python Desktop Application (Local)
The main control application is built with **Python 3.11+** and **CustomTkinter**. It provides a robust desktop interface for importing, validating, and approving data before pushing it to your Supabase production database.

### Setup & Run (Local)
1.  **Install Python 3.11+**
2.  **Clone/Download** this project.
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment:**
    -   Copy `.env.example` to `.env`.
    -   Fill in your `SUPABASE_URL` and `SUPABASE_KEY`.
5.  **Run the App:**
    ```bash
    python main.py
    ```

## 2. Web Admin Portal (Preview)
Since desktop GUIs cannot be rendered in a browser, I have provided a **Web-based Admin Portal** in the AI Studio preview window. It uses the same Supabase backend architecture.

### Supabase Setup
1.  Create a new project on [Supabase](https://supabase.com).
2.  Go to the **SQL Editor**.
3.  Copy the contents of `supabase_schema.sql` from this project and run it.
4.  Go to **Project Settings > API** to get your URL and Anon Key.
5.  Add these keys to the **Secrets** panel in AI Studio:
    -   `VITE_SUPABASE_URL`
    -   `VITE_SUPABASE_ANON_KEY`

## Features
-   **Import Center:** Supports CSV, Excel, and JSON files.
-   **Validation:** Automated checks for phones, emails, and URLs.
-   **Review Queue:** Approve or reject raw data before it hits production.
-   **Supabase Sync:** Real-time synchronization with your cloud database.
-   **Safe Defaults:** Missing fields are marked as `NOT VERIFIED` to prevent data corruption.

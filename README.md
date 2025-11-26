# EcoCycle ID

EcoCycle ID is a hyper-local, privacy-first waste exchange platform connecting waste providers (households, restaurants) with waste seekers (maggot farmers, poultry farmers, composters). This is an MVP (Minimum Viable Product) built with Streamlit.

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd ensec
    ```

2.  **Install dependencies:**
    Make sure you have Python 3.9+ installed.
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set up your Gemini API Key:**
    Create a file named `.streamlit/secrets.toml` and add your Google Gemini API key to it:
    ```toml
    [gemini]
    api_key = "YOUR_API_KEY_HERE"
    ```

4.  **Initialize the database:**
    The application will automatically create and initialize the `ecocycle.db` file on its first run.

5.  **Run the Streamlit app:**
    ```bash
    streamlit run main.py
    ```

    The app should now be open and accessible in your web browser!

## ✨ Features

*   **Waste Providers**: Can upload a picture of their organic waste, get it analyzed by AI for suitability, and post it on the platform.
*   **Waste Seekers**: Can view a map of available waste, filtered by their needs (e.g., for maggots, compost, or livestock feed).
*   **Privacy-First**: Household locations are automatically "jittered" (slightly randomized) to protect user privacy.
*   **AI-Powered Analysis**: Uses Google's Gemini 2.5 Flash to analyze waste images, estimating weight, composition, and suitability for various upcycling purposes.

## 🛠️ Tech Stack

*   **Frontend**: Streamlit
*   **Mapping**: Folium & Streamlit-Folium
*   **AI**: Google Gemini 2.5 Flash
*   **Database**: SQLite
*   **Image Processing**: Pillow
*   **Python**: 3.9+

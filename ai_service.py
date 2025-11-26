import streamlit as st
import google.generativeai as genai
from PIL import Image
import json
import io

# --- Configuration ---
try:
    # Use Streamlit's secrets management for the API key
    GEMINI_API_KEY = st.secrets["gemini"]["api_key"]
    genai.configure(api_key=GEMINI_API_KEY)
except (KeyError, FileNotFoundError):
    st.error("🚨 Gemini API Key not found. Please add it to your `.streamlit/secrets.toml` file.")
    st.stop()


# --- System Prompt ---
SYSTEM_PROMPT = """
You are an expert in Organic Waste Upcycling, Animal Feed, and Composting. Your task is to analyze an image and determine if it contains organic waste suitable for upcycling.

**Instructions:**
1.  Analyze the provided image.
2.  **First, determine if the image contains organic waste** (food scraps, vegetable peels, leftovers, garden waste, etc.).
3.  If it is **NOT** organic waste (e.g., it's a person, car, electronic, landscape, purely inorganic trash like plastic bottles, or a blank image), set `is_organic_waste` to `false` and provide a `rejection_reason`.
4.  If it **IS** organic waste:
    a. Identify the main visible components.
    b. Estimate the weight of the waste in kilograms.
    c. Determine its suitability for various upcycling methods based on the components.
    d. Provide a safety warning if you spot any contaminants or problematic materials (e.g., plastic, excessive oil, spicy foods for animals).
    e. Suggest a practical handling tip for the user.
5.  Return the analysis ONLY in a valid JSON format.

**JSON Output Structure:**
{
  "is_organic_waste": true,
  "rejection_reason": null,
  "main_composition": "<Identified main components, e.g., 'Nasi, Sayuran, Tulang Ayam'>",
  "estimated_weight_kg": <float, e.g., 1.5>,
  "suitability_tags": ["<List of suitable uses. Choose from: 'Maggot BSF', 'Ayam/Unggas', 'Ikan Lele', 'Pupuk Kompos', 'Biogas'>"],
  "safety_warning": "<Any safety concerns, e.g., 'Mengandung plastik, pisahkan sebelum diolah' or 'Aman'>",
  "handling_tip": "<A practical tip>"
}

**Example for invalid image:**
{
  "is_organic_waste": false,
  "rejection_reason": "Gambar ini terlihat seperti laptop, bukan limbah organik.",
  "main_composition": "N/A",
  "estimated_weight_kg": 0,
  "suitability_tags": [],
  "safety_warning": "N/A",
  "handling_tip": "N/A"
}
"""

# --- AI Model ---
MODEL = genai.GenerativeModel('gemini-2.5-flash')

def analyze_waste_multipurpose(image: Image.Image) -> dict:
    """
    Analyzes a waste image using the Gemini Pro Vision model.

    Args:
        image: A PIL Image object of the waste.

    Returns:
        A dictionary containing the structured analysis from the AI,
        or an error dictionary if the analysis fails.
    """
    st.write("🤖 Menganalisis gambar sampah...")
    try:
        # For Gemini Pro Vision, the prompt and image are sent together
        prompt_parts = [SYSTEM_PROMPT, image]
        response = MODEL.generate_content(prompt_parts)

        # Clean up the response to get a clean JSON string
        raw_text = response.text
        clean_json_str = raw_text.strip().replace('```json', '').replace('```', '').strip()
        
        # Parse the JSON string into a Python dictionary
        analysis_result = json.loads(clean_json_str)
        
        st.write("✅ Analisis AI selesai.")
        return analysis_result

    except json.JSONDecodeError:
        st.error("🚨 Gagal memproses respons dari AI. Format JSON tidak valid.")
        st.write("Raw response from AI:", response.text)
        return {"error": "JSON Decode Error", "raw_text": response.text}
    except Exception as e:
        st.error(f"🚨 Terjadi kesalahan saat menghubungi AI: {e}")
        return {"error": str(e)}

def image_to_blob(image: Image.Image) -> bytes:
    """Converts a PIL Image to a bytes blob."""
    with io.BytesIO() as output:
        image.save(output, format="PNG")
        contents = output.getvalue()
    return contents

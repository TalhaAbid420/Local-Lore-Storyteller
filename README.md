# Local-Lore Storyteller 🏰📖

An interactive generative AI application that transforms local historical facts, regional folklore, and cultural context into vivid, custom-tailored stories. Powered by the Google GenAI SDK and Streamlit, this project demonstrates a complete deployment pipeline utilizing containerized environments.

🚀 **[Live Demo on Hugging Face Spaces](https://talhabid420-local-lore-storyteller.hf.space)**

---

## 🌟 Features

*   **Cultural Preservation:** Generates narratives rooted deeply in accurate regional histories, localized idioms, and custom settings.
*   **Multimodal Asset Ingestion:** Supports context pairing using direct text instructions alongside structured payload inputs.
*   **Production API Pipeline:** Utilizes the state-of-the-art `google-genai` client orchestration layer to securely manage asynchronous text generation.
*   **Streamlined UI:** A clean, responsive interface engineered using Streamlit for low-latency configuration and presentation.

## 🛠️ Tech Stack & Architecture

*   **Frontend Interface:** Streamlit 
*   **AI Engine:** Google Gemini Pro API (`gemini-2.5-flash`)
*   **Core SDK:** Google GenAI Python Library (`google-genai`)
*   **Deployment & Virtualization:** Docker + Hugging Face Spaces Container

---

## ⚙️ Local Development Setup

To run this project locally, ensure you have **Python 3.10+** installed, along with a valid API Key from [Google AI Studio](https://aistudio.google.com/).

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR_USERNAME/local-lore-storyteller.git](https://github.com/YOUR_USERNAME/local-lore-storyteller.git)
cd local-lore-storyteller

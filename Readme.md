# 🌿 EcoLens — AI-Powered Nature Explorer

**Discover nature. Understand biodiversity. Touch grass.**

EcoLens is an AI-powered web application that helps people explore the natural world through photographs. Upload an image of a flower, tree, soil, pond, or other natural object, and EcoLens analyzes its visual features and provides nature-related information, identification suggestions, and personalized outdoor missions.

Built with Python, Streamlit, OpenCV, and open-source AI models, EcoLens combines computer vision with environmental education to encourage people to spend more time outdoors.

## ✨ Features

- **📸 Image Upload & Camera:** Upload a JPG or PNG image or capture a photograph directly using your camera.
- **🤖 AI Nature Identification:** Uses image-classification models to recognize broad nature categories and suggest possible flower or tree identities.
- **🔬 Scientific Names:** Displays scientific names when a species can be identified and matched to a reliable information entry.
- **📖 Nature Knowledge:** Learn about flowers, trees, soil types, ponds, lakes, rivers, forests, and other natural subjects.
- **🎨 Image Analysis:** Uses OpenCV to analyze greenery, sky or water, earth tones, brightness, texture, and dominant colours.
- **💡 Nature Suggestions:** Get practical ideas for observing plants, discovering biodiversity, and exploring local environments.
- **🌱 Touch Grass Missions:** Receive personalized outdoor activities that encourage observation and reduce screen time.
- **📊 Touch Grass Score:** A visual score based on image characteristics and identification results.
- **📱 Responsive Interface:** A nature-inspired interface designed for a clean and accessible experience.

## 🎯 Project Motivation

Technology often keeps people looking at screens instead of noticing the natural world around them.

EcoLens uses AI as a bridge between digital discovery and outdoor exploration. Instead of only identifying an object, it encourages users to observe its surroundings, learn about its ecological role, and complete small real-world nature missions.

The project supports the idea that AI can be used not only for productivity but also for environmental awareness and meaningful offline experiences.

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Streamlit | Interactive web application |
| OpenCV | Image processing and visual analysis |
| NumPy | Numerical and array operations |
| Pillow | Image loading and processing |
| Hugging Face Transformers | AI image classification |
| PyTorch | Deep-learning model inference |
| Git and GitHub | Version control and collaboration |
| Streamlit Community Cloud | Web deployment |

## 🧠 How It Works

1. **Upload:** The user uploads a nature photograph or captures one using the camera.
2. **Preprocessing:** Pillow loads the image, while OpenCV analyzes colour, texture, and other visual properties.
3. **Category Recognition:** An AI model predicts a broad category, such as flower, tree, soil, or water-related habitat.
4. **Specialized Identification:** Where supported, a second model suggests a more specific flower or tree identity.
5. **Knowledge Matching:** EcoLens uses its information database to display descriptions, scientific names when verified, identification clues, and useful facts.
6. **Outdoor Mission:** The app generates suggestions and activities relevant to the detected category.
7. **Touch Grass Score:** The application calculates a score from selected image features and identification reliability.

## 🏗️ Project Structure

```text
EcoLens/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

- `app.py` — Main Streamlit application, image analysis, AI inference, and nature information.
- `requirements.txt` — Python dependencies required to run the application.
- `README.md` — Project documentation.
- `.gitignore` — Files excluded from version control.
- `.streamlit/config.toml` — Optional Streamlit theme configuration.

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or a compatible Python version supported by the selected dependencies.
- Git.
- An internet connection for downloading AI model weights on the first run.

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd EcoLens
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your actual GitHub repository URL.

### 2. Create a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use Command Prompt instead:

```cmd
.venv\Scripts\activate.bat
```

### 3. Install dependencies

Create `requirements.txt` with the packages used by the application:

```text
streamlit
numpy
Pillow
opencv-python-headless
transformers
torch
```

Then install them:

```bash
python -m pip install -r requirements.txt
```

For a reproducible deployment, test a compatible set of package versions in your environment and pin those versions after successful testing.

### 4. Run EcoLens locally

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

```text
http://localhost:8501
```

## ☁️ Deployment

EcoLens can be deployed using Streamlit Community Cloud.

1. Push the project files to a GitHub repository.
2. Visit [Streamlit Community Cloud](https://share.streamlit.io/).
3. Sign in with GitHub.
4. Create a new app and select your EcoLens repository.
5. Choose the deployment branch, usually `main`.
6. Set the main file path to `app.py`.
7. Deploy the application.

The first deployment may take longer because Python dependencies and model weights need to be downloaded. Model size, memory availability, and CPU resources can affect startup and inference time.

## 🌍 Example Use Cases

- Identify possible flower and tree types from photographs.
- Learn about plant characteristics and ecological importance.
- Explore soil appearance and understand why laboratory testing may be needed.
- Discover the plants and animals associated with ponds and other habitats.
- Encourage children and students to explore nature through guided observation.
- Promote outdoor activities and environmental awareness.

## ⚠️ Limitations

- AI predictions are suggestions, not guaranteed identifications.
- Some flower and tree species may be missing from the supported model classes or information database.
- Scientific names should be treated as unconfirmed when the species match is uncertain.
- Soil type cannot be reliably established from a photograph alone; laboratory testing is recommended for agricultural decisions.
- The Touch Grass Score is an application-defined indicator, not a scientific measure of biodiversity or environmental quality.
- Model downloads and inference may be slower on free hosting resources.

## 🔮 Future Improvements

- Add a dedicated plant-identification model with broader regional species coverage.
- Expand the flower, tree, and wildlife knowledge databases.
- Add verified scientific-name references and source links.
- Improve confidence calibration and communicate uncertainty more clearly.
- Include location-aware native plant recommendations with user consent.
- Add biodiversity logs, observation history, and outdoor challenge tracking.
- Optimize model loading and inference for limited hosting resources.

## 🌱 Hacktoberfest Connection

EcoLens supports the idea of using open-source AI to encourage people to disconnect from their screens and reconnect with the outdoors.

It combines AI-powered discovery with practical, offline nature missions, helping users turn a photograph into an opportunity to learn about the environment around them.

## 🤝 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Make and test your changes.
4. Submit a pull request with a clear explanation of the improvement.

Ideas for contributions include additional plant species, improved AI models, better accessibility, new nature missions, and performance optimizations.

## 📄 License

Add a `LICENSE` file to the repository and specify the license you choose for EcoLens. Check the licenses of any third-party models, datasets, and dependencies before redistributing or deploying them.

---

**EcoLens — Less scrolling, more exploring. 🌿**

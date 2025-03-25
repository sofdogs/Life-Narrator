# Life-Narrator
## 🛠️ Setup Instructions

To get started with Life Narrator locally, follow these steps:

---

### 1. Clone the repository and set up a virtual environment

```bash
git clone https://github.com/your-username/Life-Narrator.git
cd Life-Narrator
python3 -m pip install virtualenv
python3 -m virtualenv venv
source venv/bin/activate
```

### 2. Install Dependencies 
```bash
pip install -r requirements.txt
```
### 3. Create accounts and set environment vars 
You'll need API keys from: 
- OpenAI
- ElevenLabs
- Replicate

Once you have your API tokens, set them in your terminal 
```bash
export OPENAI_API_KEY=<your-openai-token>
export ELEVENLABS_API_KEY=<your-elevenlabs-token>
```

Next, create a custom voice in ElevenLabs. Then: 
```bash
export ELEVENLABS_VOICE_ID=<your-voice-id>
```

### 4. Run the app 
In one terminal, start the webcam capture: 
```bash
python capture.py
```
In a different terminal, start the narrator: 
```bash
python narrator.py
```


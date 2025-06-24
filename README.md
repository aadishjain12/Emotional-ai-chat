# Emotional AI Chat 🤖💬

An interactive AI chatbot project that combines emotional tone control with a persistent 3D avatar powered by Ready Player Me. The bot can be customized with different personalities, speaks responses aloud, and dynamically reacts to emotions via animations and styles.

## 🚀 Features

- 🌈 Emotion-based agent creation (Friendly, Witty, Sad, Professional)
- 🧑‍🚀 Persistent Ready Player Me avatar integration
- 🎭 Avatar reacts visually to selected emotion
- 🗣️ Real-time Text-to-Speech for assistant replies
- 💬 Full conversation history with assistant
- 🌐 Backend powered by Flask (deployed on Railway)
- 🖼️ Frontend ready for deployment (Vercel optional)

## 🛠 Technologies Used

- HTML/CSS/JavaScript
- Flask (Python backend)
- OpenAI API
- Ready Player Me (Avatar iframe)
- Web Speech API (TTS)
- Railway (Deployment)

## 📁 Project Structure

```
/project-root
├── app.py                  # Flask backend
├── templates/
│   └── index.html          # Main UI
├── static/                 # (Optional) styles, JS, images
├── .env                    # Contains your OpenAI API key (DO NOT COMMIT)
├── requirements.txt
├── Dockerfile              # For Railway deployment
└── README.md
```

## 🔐 Environment Variables

Create a `.env` file in your root folder:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 🚀 Deployment Instructions

### 📦 Backend on Railway

1. Push code to GitHub
2. Go to [https://railway.app](https://railway.app)
3. Create new project → Deploy from GitHub repo
4. Set Environment Variable: `OPENAI_API_KEY`
5. Expose port 5000

### 🌐 Frontend on Vercel (Optional)

1. Create a `/frontend` folder with `index.html`
2. Deploy to Vercel
3. Connect to Railway backend via full URL

## 🧠 Credits

Built by [Aadish Jain](https://github.com/aadishjain12)  
Voice + Emotion + Avatar Integration by ❤️ ChatGPT

## 📸 Preview

> _(Include a GIF or screenshot of the app if possible)_

---

**MIT License**

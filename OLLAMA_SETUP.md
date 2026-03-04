# Running Local LLM with Ollama (Zero Cost)

## Quick Start

### 1. Install Ollama

Visit [ollama.com](https://ollama.com) and download the installer for your OS:

- **Windows**: Download `.exe` and run the installer
- **macOS**: Download `.dmg` and install
- **Linux**: Run `curl https://ollama.ai/install.sh | sh`

### 2. Pull a Model (One-Time)

After installing Ollama, pull a model in terminal/PowerShell:

```bash
ollama pull mistral
```

**Available Models:**

- **mistral** (4GB) - Faster, stronger reasoning (RECOMMENDED)
- **llama2** (3.5GB) - General purpose, balanced performance
- **neural-chat** (4GB) - Optimized for chatting
- **dolphin-mixtral** (26GB) - Most capable, requires 32GB+ RAM
- **tinyllama** (637MB) - Fastest, runs on low-end hardware

You can also try:

```bash
ollama pull mistral
ollama pull neural-chat
```

### 3. Run Ollama Server

Start the Ollama server (runs in background):

**Windows:**

- Ollama starts automatically when installed
- Check system tray icon that it's running
- Or manually run: Press `Win` + `R`, type `ollama serve`

**macOS/Linux:**

```bash
ollama serve
```

The server runs at `http://localhost:11434` by default.

### 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The `requirements.txt` includes all RAG dependencies.

### 5. Run Your RAG Application

Use the local Ollama API endpoint at `http://localhost:11434`

---

## Model Recommendations

| Model       | Size  | Speed  | Quality  | Use Case             |
| ----------- | ----- | ------ | -------- | -------------------- |
| tinyllama   | 637MB | ⚡⚡⚡ | ⭐       | Lightweight, testing |
| llama2      | 3.5GB | ⚡⚡   | ⭐⭐⭐   | Best balance         |
| mistral     | 4GB   | ⚡⭐   | ⭐⭐⭐⭐ | Fastest quality      |
| neural-chat | 4GB   | ⭐     | ⭐⭐⭐⭐ | Best for chat        |

---

## Switching Models in Your Code

Switch between models by running:

```bash
ollama pull mistral
ollama pull neural-chat
```

---

## Performance Tips

1. **First Run Slower**: Model loads into RAM on first use (~30 sec)
2. **Keep Ollama Running**: Don't close the terminal/app running `ollama serve`
3. **Adjust Temperature**:
   - `temperature=0.1` - Deterministic, good for Q&A
   - `temperature=0.7` - Balanced (default)
   - `temperature=1.0` - Creative responses
4. **GPU Acceleration**: If Ollama detects NVIDIA GPU, it auto-uses it
5. **Reduce Chunk Size**: If responses are slow, use smaller context windows

---

## Troubleshooting

**Error: Connection refused (http://localhost:11434)**

- Make sure Ollama is running: `ollama serve`
- Check firewall isn't blocking port 11434

**Model won't download**

- Check internet connection
- Try a smaller model first: `ollama pull tinyllama`
- Models download to `~/.ollama/models` (space needed!)

**Slow responses**

- Running large model on CPU? Try `tinyllama`
- Close other apps to free RAM
- Reduce `max_tokens` parameter

**Out of Memory**

- Use smaller model: `ollama pull tinyllama`
- Close other applications
- Increase system RAM or decrease context size

---

## Cost Comparison

| Service          | Cost                     | Speed       | Privacy    |
| ---------------- | ------------------------ | ----------- | ---------- |
| Groq             | $0.30 per hour           | ⚡⚡⚡ Fast | ❌ Cloud   |
| OpenAI           | $0.01-0.10 per 1K tokens | ⚡⭐ Medium | ❌ Cloud   |
| **Ollama Local** | **$0 (free!)**           | ⭐ Variable | ✅ Private |

With Ollama, your data never leaves your computer!

---

## Next Steps

1. ✅ Install Ollama from ollama.com
2. ✅ Run `ollama pull llama2`
3. ✅ Run `ollama serve` in terminal
4. ✅ Update your Python environment: `pip install -r requirements.txt`
5. ✅ Run your notebook - it will now use local Ollama!

**No API keys. No billing. No rate limits. Just local LLM power! 🚀**

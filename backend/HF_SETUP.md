# Enabling Hugging Face model responses

This project can use the Hugging Face Inference API to produce richer AI replies. If you want the backend to call the HF model instead of local fallbacks, set the `HF_API_KEY` environment variable.

1. Get an API key
   - Sign in to Hugging Face and create an access token (Settings → Access Tokens). Copy the token.

2. Local (PowerShell) temporary session

```powershell
$env:HF_API_KEY = "hf_xxx_your_token_here"
python backend/app.py
```

3. Persist across sessions (PowerShell)

```powershell
setx HF_API_KEY "hf_xxx_your_token_here"
# Restart terminal for changes to take effect
```

4. Using a .env file (optional)

- The project includes `backend/.env.example`. You can copy it to `.env` and include a line like:

```
HF_API_KEY=hf_xxx_your_token_here
```

- Note: the current `app.py` reads `HF_API_KEY` from `os.getenv`. If you use a `.env` file, ensure you load it (e.g., via `python-dotenv`) or set the env var in your shell.

5. Troubleshooting
   - If the backend returns the local fallback responses, check the console logs for HF API errors (rate limits, invalid key, or network issues).
   - Increase `timeout` or verify network access if requests time out.

That's it — once `HF_API_KEY` is set, the backend will attempt to use the Hugging Face model for chat replies and fall back to local answers when necessary.

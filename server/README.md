# Express Route to Postman Collection Backend (Gemini-powered)

## Setup

```bash
cd server
pip install -r requirements.txt
```

### Set your Gemini API key

Export your Google Gemini API key (get it from Google AI Studio):

```bash
export GEMINI_API_KEY=your_api_key_here
```

## Run

```bash
uvicorn main:app --reload
```

## Endpoint

### POST /generate-postman

**Body:**
```json
{
  "repoUrl": "https://github.com/org/repo"
}
```

**Returns:**
- `postman_collection.json` file for download

## How it works
- Clones the repo
- Loads relevant Express files (controllers, routes, app.js, DTOs)
- Sends code to Gemini API to extract endpoints
- Builds a valid Postman v2.1 collection
- Returns the file for download 

---

## How to Fix

### 1. **Check Available Models**
You should list the available models for your API key/project. Here’s how you can do it in Python:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
models = genai.list_models()
for m in models:
    print(m)
```
This will print all available models and their IDs.

---

### 2. **Update the Model Name**
- The correct model name for Gemini Pro is often `"models/gemini-1.0-pro-latest"` or similar (not just `"gemini-pro"`).
- Replace this line in your code:
  ```python
  model = genai.GenerativeModel("gemini-pro")
  ```
  with:
  ```python
  model = genai.GenerativeModel("models/gemini-1.0-pro-latest")
  ```
  or whatever model name is listed from the code above.

---

### 3. **Check API Version**
- Make sure you are using the latest version of the `google-generativeai` library (`pip install --upgrade google-generativeai`).
- Some models are only available in certain regions or for certain API keys.

---

### 4. **Documentation Reference**
- [Google Generative AI Python SDK Docs](https://ai.google.dev/docs/python-sdk/get-started)
- [Model List Reference](https://ai.google.dev/models/gemini)

---

## Next Steps

1. **List your available models** using the code above.
2. **Update the model name** in your backend to match an available model that supports `generate_content`.
3. **Test again**.

Would you like me to update your backend code to use the correct model name once you provide it, or should I add a model listing utility for you? 
from fastapi import FastAPI, Request
import requests
import subprocess
import json
import os

app = FastAPI()

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

@app.post("/ask")
async def ask(request: Request):
    data = await request.json()
    user_query = data["query"]

    prompt = f"""
    You are an assistant that writes and executes Python
    to perform tasks such as analyzing or filtering data.
    The user asked: {user_query}
    Return only the python code that can be directly executed. without any prefix python etc.
    only the code. the output will be directly executed.
    """

    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        headers={"Content-Type": "application/json"},
        json={
            "model": "phi",
            "prompt": prompt,
            "stream": False  # Important: disable streaming for simple calls
        }
    )

    # Parse Ollama response
    print(f"{response}")
    res_json = response.json()
    code = res_json.get("response", "").strip("` \n")

    # Save to a temporary file
    with open("/tmp/script.py", "w") as f:
        f.write(code)

    # Execute safely
    try:
        result = subprocess.run(
            ["python3", "/tmp/script.py"],
            capture_output=True,
            text=True,
            timeout=10
        )
        output = result.stdout or result.stderr
    except Exception as e:
        output = f"Execution error: {e}"

    return {"code": code, "result": output}

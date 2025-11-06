import requests

print("🤖 AI Agent CLI (type 'exit' to quit)")
while True:
    query = input("\n> ")
    if query.lower() == "exit":
        break
    try:
        resp = requests.post("http://localhost:8000/ask", json={"query": query})
        data = resp.json()
        print("\n💻 Code generated:\n", data["code"])
        print("\n📊 Result:\n", data["result"])
    except Exception as e:
        print("Error:", e)

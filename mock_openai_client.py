from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="dummy"
)
content = client.files.content("file-abc123")
print(content.write_to_file("tmp.txt"))
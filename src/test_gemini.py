from ai_analyzer import client, MODEL_NAME


response = client.models.generate_content(
    model=MODEL_NAME,
    contents="Explain anomaly detection in one sentence."
)

print(response.text)
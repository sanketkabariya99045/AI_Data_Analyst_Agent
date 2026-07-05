import requests

url = "http://127.0.0.1:8000/api/upload"

with open(r"D:\SMS_Spam_Classifier\spam.csv", "rb") as f:
    files = [
        ("files", ("spam.csv", f, "text/csv"))
    ]

    response = requests.post(url, files=files)

print(response.status_code)
print(response.text)
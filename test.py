import requests

headers = {
    'Content-Type': 'application/json'
}
requestResponse = requests.get("https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol=FSLR&apikey=U4UFMVF87NKSHS2Y")
print(requestResponse.json())
import json

with open("response.json", "r", encoding="UTF-8") as file:
    response=json.load(file)

print("totalResults",response['pageInfo']['totalResults'])
print("fetchedResults",len(response['items']))
for item in response['items']:
    print(item['id'],item['snippet']['title'],item['contentDetails']['itemCount'])

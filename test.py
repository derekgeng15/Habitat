import requests

BASE = 'http://127.0.0.1:5000/'

requests.post(BASE + 'database/test', {'description' : 'test post', 'users' : 'derek, tejas, pradyun'})
requests.put(BASE + 'database/test/posts', {'title':'Test Title 2', 'content': 'i do not like pradyun', 'userID' : 0})

print(requests.get(BASE + 'database/test/posts').json())
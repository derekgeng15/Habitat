import requests

BASE = 'http://127.0.0.1:5000/'

requests.post(BASE + 'database/test')
requests.put(BASE + 'database/test/posts', {'title':'Test Title 2', 'content': 'i do not like pradyun'})

print(requests.get(BASE + 'database/test/posts').json())
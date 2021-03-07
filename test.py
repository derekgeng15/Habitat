import requests

BASE = 'http://127.0.0.1:5000/'

requests.post(BASE + 'database/Meditation', {'description' : 'this is a habitat for meditation/yoga', 'users' : 'derek, tejas, pradyun'})
requests.put(BASE + 'database/Meditation/posts', {'title' : 'Finally got my license as a certified yoga teacher!', 'content' : "After such as long time, i've finally become a certified yoga teacher! This moment was around 3 years in the waiting due to my injuries", 'userID': 0})
print(requests.get(BASE + 'database/Meditation/posts').json())
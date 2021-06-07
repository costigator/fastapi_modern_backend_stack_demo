import requests
import json
import uuid
from passlib.context import CryptContext

print("Generating random users. The password hashing process takes some time, please wait...")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

result = requests.get("https://randomuser.me/api/?results=1000")

random_users = json.loads(result.content)

users = []
for random_user in random_users['results']:
    user = {}
    user['_id'] = str(uuid.uuid4())
    user['name'] = random_user['name']['first'] + " " + random_user['name']['last']
    user['email'] = random_user['email']
    user['login'] = {}
    user['login']['username'] = random_user['login']['username']
    user['login']['password'] = pwd_context.hash(random_user['login']['password'] )
    user['birthday'] = random_user['dob']['date'][:10]
    user['disabled'] = False

    users.append(user)

f = open("users.json", "a")
f.write(json.dumps(users, indent=4))
f.close()

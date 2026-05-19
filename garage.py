# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# BUCKET_NAME = "video"

# # 1. Trouver l'ID du bucket
# r = requests.get(f"{GARAGE_ADMIN_URL}/v2/bucket?list")
# buckets = r.json()

# bucket_id = None
# for b in buckets:
#     r2 = requests.get(f"{GARAGE_ADMIN_URL}/v2/bucket?id={b['id']}")
#     info = r2.json()
#     if info.get("localAliases") and BUCKET_NAME in str(info.get("localAliases", [])):
#         bucket_id = b['id']
#         break
#     if info.get("globalAliases") and BUCKET_NAME in info.get("globalAliases", []):
#         bucket_id = b['id']
#         break

# print(f"Bucket ID trouvé : {bucket_id}")

# # 2. Rendre le bucket public en lecture
# if bucket_id:
#     r3 = requests.put(
#         f"{GARAGE_ADMIN_URL}/v2/bucket",
#         json={
#             "bucketId": bucket_id,
#             "websiteAccess": {"enabled": False},
#             "corsRules": [],
#             "quotas": {"maxSize": None, "maxObjects": None},
#             "anonymousAccess": {"read": True, "write": False, "owner": False}
#         }
#     )
#     print(f"Status: {r3.status_code}")
#     print(r3.json())


# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"

# r = requests.get(f"{GARAGE_ADMIN_URL}/v2/bucket?list")
# print(r.status_code)
# print(r.json())




# import requests

# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"
# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"

# r = requests.get(
#     f"{GARAGE_ADMIN_URL}/v1/bucket?list",
#     headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
# )
# print(r.json())




# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"

# bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# r = requests.put(
#     f"{GARAGE_ADMIN_URL}/v1/bucket",
#     headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
#     json={
#         "bucketId": bucket_id,
#         "anonymousAccess": {"read": True, "write": False, "owner": False}
#     }
# )
# print(r.status_code)
# print(r.json())







# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"

# bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# # Voir les infos actuelles du bucket
# r = requests.get(
#     f"{GARAGE_ADMIN_URL}/v1/bucket?id={bucket_id}",
#     headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
# )
# print(r.status_code)
# print(r.json())




# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"

# bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# r = requests.put(
#     f"{GARAGE_ADMIN_URL}/v1/bucket/website",
#     headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
#     json={
#         "bucketId": bucket_id,
#         "websiteAccess": True,
#         "indexDocument": "index.html",
#         "errorDocument": "error.html"
#     }
# )
# print(r.status_code)
# print(r.text)






# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"
# bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# r = requests.put(
#     f"{GARAGE_ADMIN_URL}/v1/bucket",
#     headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
#     json={
#         "bucketId": bucket_id,
#         "websiteAccess": {
#             "enabled": True,
#             "indexDocument": "index.html",
#             "errorDocument": "error.html"
#         }
#     }
# )
# print(r.status_code)
# print(r.json())








# import requests

# GARAGE_ADMIN_URL = "http://192.168.1.66:3903"
# ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"
# bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# # Tester les endpoints possibles
# endpoints = [
#     ("PUT", f"/v1/bucket?id={bucket_id}"),
#     ("POST", f"/v1/bucket?id={bucket_id}"),
#     ("PUT", f"/v1/bucket/{bucket_id}"),
#     ("PUT", f"/v1/bucket/{bucket_id}/website"),
#     ("POST", f"/v1/bucket/{bucket_id}/website"),
# ]

# for method, path in endpoints:
#     r = requests.request(
#         method,
#         f"{GARAGE_ADMIN_URL}{path}",
#         headers={"Authorization": f"Bearer {ADMIN_TOKEN}"},
#         json={"websiteAccess": {"enabled": True, "indexDocument": "index.html", "errorDocument": "error.html"}}
#     )
#     print(f"{method} {path} → {r.status_code}")







import requests

GARAGE_ADMIN_URL = "http://192.168.1.69:3903"
ADMIN_TOKEN = "e7bf856dd82c03051e8916abf05d58924a7c9d87a4b21d0165636b118bb40867"
bucket_id = "a1cc42ead7dfc10ec53e0aca921ffa9c204f95fd3d76c32a4b95374999de8015"

# Vérifier l'état actuel du bucket
r = requests.get(
    f"{GARAGE_ADMIN_URL}/v1/bucket?id={bucket_id}",
    headers={"Authorization": f"Bearer {ADMIN_TOKEN}"}
)
print(r.json())
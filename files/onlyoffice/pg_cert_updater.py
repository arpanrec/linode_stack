import json
import os

default_json_file: str = "/etc/onlyoffice/documentserver/default.json"
print(f"Updating default.json file:: {default_json_file}")
pg_ca: str = open("/tmp/pg_ca.pem", "r", encoding="utf-8").read()
print(f"Reading pg_ca: {pg_ca}")
pg_cert: str = open("/tmp/pg_cert.pem", "r", encoding="utf-8").read()
print(f"Reading pg_cert: {pg_cert}")
pg_key: str = open("/tmp/pg_key.pem", "r", encoding="utf-8").read()
print(f"Reading pg_key: {pg_key}")
current_json = json.loads(open(default_json_file, "r", encoding="utf-8").read())
print(f"Reading current_json: {current_json}")
current_json["services"]["CoAuthoring"]["requestDefaults"]["rejectUnauthorized"] = False
current_json["services"]["CoAuthoring"]["sql"]["pgPoolExtraOptions"]["ssl"] = {
    "rejectUnauthorized": False,
    "ca": pg_ca,
    "cert": pg_cert + pg_ca,
    "key": pg_key,
}

print(f"Writing updated current_json: {current_json}")
with open(default_json_file, "w", encoding="utf-8") as f:
    json.dump(current_json, f, ensure_ascii=False, indent=4)
print(f"Changing permissions of {default_json_file}")
os.chmod(default_json_file, 0o666)

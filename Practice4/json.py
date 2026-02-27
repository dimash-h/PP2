import json

with open("sample-data.json", "r") as f:
    data = json.load(f)

#заголовок
print("Interface Status")
print("=" * 80)
print("DN".ljust(50), "Description".ljust(20), "Speed".ljust(7), "MTU")
print("-" * 50, "-" * 20, "-" * 6, "-" * 6)

#строки
for item in data["imdata"]:
    attrs = item["l1PhysIf"]["attributes"]

    dn = attrs["dn"]
    descr = attrs["descr"]
    speed = attrs["speed"]
    mtu = attrs["mtu"]

    print(dn.ljust(50), descr.ljust(20), speed.ljust(7), mtu)
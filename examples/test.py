from fortress_sdk_python import Client

fortress = Client(
    org_id="myOrgId",
    api_key="myApiKey",
)
response = fortress.create_database("sdk_test")
if response.success:
    print("Database created")


response = fortress.connect("sdk_text")
conn = response.cursor()
result = conn.execute(
    "CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)"
)
result = conn.execute("INSERT INTO test (name) VALUES ('test')")
result = conn.execute("SELECT * FROM test")

for row in result.fetchall():
    print(row)

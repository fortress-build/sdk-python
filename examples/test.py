from fortress_sdk_python import Client

fortress = Client(
    org_id="orgId",
    api_key="apiKey",
)

response = fortress.create_database("sdk_test")
if response.success:
    print("Database created")
else:
    print(f"Database creation failed: {response.message}")

conn = fortress.connect("sdk_test")
conn.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)")
conn.execute("INSERT INTO test (name) VALUES ('test')")
conn.commit()

result = conn.execute("SELECT * FROM test;").fetchall()
for row in result:
    print(row)

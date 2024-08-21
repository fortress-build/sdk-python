from fortress_sdk_python import Fortress

# Initialize the Fortress client
fortress = Fortress(
    org_id="orgId",
    api_key="apiKey",
)

# Create a database
response = fortress.create_database(alias="Client 1")
if response.success:
    print("Database created")
else:
    print(f"Database creation failed: {response.message}")

# Create a tenant (if you do not provide a database_id, a new database will be created)
response = fortress.create_tenant(
    tenant_name="client1",
    alias="Client 1",
    database_id=response.id,
)
if response.success:
    print("Tenant created")
else:
    print(f"Tenant creation failed: {response.message}")

# List all databases
response = fortress.list_databases()
if response.success:
    for database in response.databases:
        print(database.id, database.alias, database.date_created)

# List all tenants
response = fortress.list_tenants()
if response.success:
    for tenant in response.tenants:
        print(tenant.name, tenant.alias, tenant.database_id, tenant.date_created)

# Connect to the tenant's database
conn = fortress.connect_tenant("client1")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO test (name) VALUES ('Alice')")
conn.commit()

result = cursor.execute("SELECT * FROM test").fetchall()
for row in result:
    print(row)

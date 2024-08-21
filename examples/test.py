from fortress_sdk_python import Fortress

# Initialize the Fortress client
fortress = Fortress(
    org_id="orgId",
    api_key="apiKey",
)

# Create a database
database_id = None
try:
    database_id = fortress.create_database(alias="Client 1")
except Exception as e:
    print(f"Database creation failed: {e}")

# Create a tenant (if you do not provide a database_id, a new database will be created)
try:
    fortress.create_tenant(
        tenant_id="client1",
        alias="Client 1",
        database_id=database_id,
    )
except Exception as e:
    print(f"Tenant creation failed: {e}")

# List all databases
try:
    databases = fortress.list_databases()
    for database in databases:
        print(database.id, database.alias, database.created_date)
except Exception as e:
    print(f"Database listing failed: {e}")

# List all tenants
try:
    tenants = fortress.list_tenants()
    for tenant in tenants:
        print(tenant.id, tenant.alias, tenant.database_id, tenant.created_date)
except Exception as e:
    print(f"Tenant listing failed: {e}")

# Connect to the tenant's database
conn = None
try:
    conn = fortress.connect_tenant("client1")
except Exception as e:
    print(f"Database connection failed: {e}")


cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name TEXT)")
cursor.execute("INSERT INTO test (name) VALUES ('Alice')")
conn.commit()

result = cursor.execute("SELECT * FROM test").fetchall()
for row in result:
    print(row)

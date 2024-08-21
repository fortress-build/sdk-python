# Fortress Python SDK

Welcome to the Fortress Python SDK. This SDK provides a way for you to leverage the power of the Fortress platform in your Python applications.

## Installation

You can install the SDK using pip. Simply run the following command:

```bash
pip install fortress-sdk-python
```

## Quick Start

Here is a quick example to get you started with the SDK:

```python
from fortress_sdk_python import Fortress

# Initialize the client with your API key
client = Fortress(org_id='your_org_id', api_key='your_api_key')

# Connect to a database
conn = client.connect_tenant(tenant_name='client1')
cursor = conn.cursor()

# Execute a query to fetch all rows from a table
results = cursor.execute('SELECT * FROM your_table_name').fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()
```

## Documentation

Below is a list of the available functionality in the SDK. Using the SDK you can create a new tenants and point them to existing or new databases. You can also easily route data requests based on tenant names. For more detailed information, please refer to the [Fortress API documentation](https://docs.fortress.build).

Database Management:

- `create_database(database_name: str, alias: str)`: Creates a new database.
- `delete_database(database_name: str)`: Deletes to a database.
- `list_databases()`: Lists all databases.
- `connect_database(database_id: str)`: Connects to a database and turns into SQL connection.

Tenant Management:

- `create_tenant(tenant_name: str, alias: str, database_id: str = "")`: Creates a new tenant.
- `delete_tenant(tenant_name: str)`: Deletes a tenant.
- `list_tenants()`: Lists all tenants.
- `connect_tenant(tenant_name: str)`: Connects to a tenant and turns into SQL connection.

## Configuration

To use the SDK, generate an API key from the Fortress dashboard to initialize the client. Also, provide the organization ID, which is available under the API Keys page on the platform website.

## License

This SDK is licensed under the MIT License.

## Support

If you have any questions or need help, don't hesitate to get in touch with our support team at founders@fortress.build.

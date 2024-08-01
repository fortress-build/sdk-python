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
from fortress_sdk_python import Client as FortressClient

# Initialize the client with your API key
client = FortressClient(org_id='your_org_id', api_key='your_api_key')

# Connect to a database
conn = client.connect(database_name='your_database_name')
cursor = conn.cursor()

# Execute a query
cursor.execute('SELECT * FROM your_table_name')

# Fetch the results
results = cursor.fetchall()

# Print the results
for row in results:
    print(row)

# Close the connection
conn.close()
```

## Documentation

Below is a list of the available functionality in the SDK.

- `create_database(database_name: str)`: Creates a new database.
- `delete_database(database_name: str)`: Connects to a database.
- `list_databases()`: Lists all databases.
- `connect(database_name: str)`: Connects to a database and turns a LibsqlConnection object.

## Configuration

To use the SDK, generate an API key from the Fortress dashboard to initialize the client. Also, provide the organization ID, which is available under the API Keys page on the platform website.

## License

This SDK is licensed under the MIT License.

## Support

If you have any questions or need help, don't hesitate to get in touch with our support team at founders@fortress.build.

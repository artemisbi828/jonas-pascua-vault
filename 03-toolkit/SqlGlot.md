To migrate from MSSQL to Snowflake using SQLGlot, you should treat your SQL as data that requires a transformation pipeline. The "ideal workflow" avoids string replacement (which is brittle) and instead uses the AST Transformation pattern.
Here is the high-fidelity, clinical workflow for your local environment.
1. The Core Ingredients
To work efficiently, prepare these three components on your local machine:
 * The Source Directory: A folder containing your .sql files (MSSQL/T-SQL).
 * The Mapping Manifest: A JSON or YAML file containing your object translations.
 * The Transpiler Script: A Python script using sqlglot.exp and sqlglot.parse_one.
2. High-Level Concrete Workflow
Step 1: Define the Mapping Manifest
Create a file named mapping.json. This acts as your source of truth for 1:1 object replacement (e.g., renaming legacy tables to new Snowflake schemas).
{
  "tables": {
    "dbo.old_users": "raw_db.legacy.users",
    "sales.orders": "analytics.sales.orders_v2"
  },
  "columns": {
    "user_id": "id",
    "created_at": "creation_timestamp"
  }
}

Step 2: Build the Transformer Function
SQLGlot uses a transform method that visits every node in the AST. For a traditional developer, think of this as a "Trigger" that fires whenever the parser hits a specific object type.
import sqlglot
from sqlglot import exp, parse_one

# Load your mapping
MAPPING = {
    "old_users": "users",
    "sales.orders": "orders_v2"
}

def migrate_objects(node):
    # Target Table nodes for renaming
    if isinstance(node, exp.Table):
        table_name = node.sql()
        if table_name in MAPPING:
            # Replace node with the mapped value
            return parse_one(MAPPING[table_name], read=None)
    
    # Target specific T-SQL patterns like bracketed identifiers
    if isinstance(node, exp.Identifier) and node.args.get("quoted"):
        # Snowflake prefers double quotes or upper case; SQLGlot handles this via dialect
        pass
        
    return node

Step 3: Execute the Pipeline
This script reads your T-SQL, converts it to a Snowflake-compatible AST, applies your mapping, and outputs the final Snowflake SQL.
sql_tsql = "SELECT TOP 10 user_id FROM dbo.old_users WHERE status = 1"

# 1. Parse T-SQL into an AST
expression = parse_one(sql_tsql, read="tsql")

# 2. Apply the mapping transformation
transformed_expression = expression.transform(migrate_objects)

# 3. Generate Snowflake SQL
# SQLGlot automatically pivots 'TOP 10' to 'LIMIT 10' for Snowflake
snowflake_sql = transformed_expression.sql(dialect="snowflake", pretty=True)

print(snowflake_sql)

3. The Pivot: Strategic Advantages
 * Syntax Correction: Notice in Step 3 that SQLGlot didn't just rename the table; it realized Snowflake doesn't support SELECT TOP. It moved the logic to a LIMIT clause automatically.
 * Schema Qualification: You can use the transformation to inject database.schema prefixes to every table if your MSSQL code was "schema-lite."
 * Data Type Mapping: If you have DATETIMEOFFSET in MSSQL, SQLGlot will pivot the type to TIMESTAMP_TZ for Snowflake during transpilation.
Pro-Tip for Local Efficiency:
Install the sqlglot CLI to quickly test snippets without writing Python:
sqlglot-rewrite --read tsql --write snowflake "SELECT TOP 10 * FROM x"

What does your current object naming convention look like? (If you provide a few examples of your MSSQL object names vs. your intended Snowflake names, I can refine the mapping logic for you).

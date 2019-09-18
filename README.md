# descriptor_schema
This is an example of using descriptor protocol to support object schemas for NoSQL DBs
What it can do:
1.It allows to set public/required attributes. This is very useful when you want to use this schema to enable output to the end users
2.It supports type check. If you try to assign any value that doesn't match described in schema - this will give you a ValueError
3.It supports conversion to_dict which is used for NoSQL dbs like DynamoDB or MongoDB.

# DjangoSandboxStuff

In this project, I'm using the django-rest-framework to create an API a client can GET, POST, PUT, and PATCH JSON payloads.
The API is using a [Product model](backend.api.models.py) that describes the contents of the product objects. 
This schema serves as the table for the products. The current version (04.07.23) lets the client:
- Create a new product
- List all existing products
- Fully / Partially update an existing product

The next step would be to add a level of authentication. This way, the products will have users assigned to them and the CRUD operations will only work on the products that the user is assigned to. With this implementation, the intention is for:
- Users to only view / delete / update their assigned products
- Not be allowed to view / delete / update products not assigned to them / assigned to other users
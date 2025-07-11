# DjangoSandboxStuff

This project references the course found [here](https://www.youtube.com/watch?v=c708Nf0cHrs). I'm using the django-rest-framework to create an RESTful API.

To test this project, simply clone this repository to your local, `cd` into `backend` and run
```shell
python manage.py runserver 8080
```

In another terminal, you can call the different requests by doing a `cd` into `py_client` and running one of the files, e.g.
```shell
python get_all.py
```

However, the most reasonable file to run would be `create_user.py` as the requests will all need authentication. Once you've created your user, your API Token will appear in the `.env` file.

---
### Running Tests

To run the tests, in the CLI:
```shell
python -m unittest tests/<file_name>
```
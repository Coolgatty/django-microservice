# django-CI-CD 

## Local Installation

### Requirements

This app requires `Docker`, `Docker Compose` and it uses `pyenv` with `pipenv`. Once you installed all of this, you can follow the next steps.

### Installation

* Go to the app folder and write in the console:

    ```
    pipenv shell
    ```

* Install all the dependencies with:

    ```
    pipenv install -r requirements.txt
    ```

* Go back to the root and setup your `.env` file using the `.env.default`.

* Using `Docker Compose` build the image with:

    ```
    docker-compose build
    ```

    *Note*: If you have problems with the database permissions, you need to use before `docker-compose run db chmod -R 777 /var/lib/postgresql/data`.

* Run the migrations with:

    ```
    docker-compose run web python manage.py migrate
    ```

* Run with `Docker Compose` using:

    ```
    docker-compose up
    ```

And that's all, now you can see the template on your browser in `localhost`.
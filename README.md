# MetaGenScope Server

> MetaGenScope server application.

## Getting Started

This readme documents how to run and test the MetaGenScope server as a standalone application. `metagenscope-server` is part of [`metagenscope-main`](https://github.com/bchrobot/metagenscope-main) and should usually be run as part of the complete stack.

### Prerequisites

You will also need to have PostgreSQL running locally with the following databases:

```sql
CREATE DATABASE metagenscope_prod;
CREATE DATABASE metagenscope_dev;
CREATE DATABASE metagenscope_test;
```

And plugins:

```sql
\c metagenscope_prod;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_dev;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
\c metagenscope_test;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

All local interactions with the server (developing, running, testing) should be done in a virtual environment:

```sh
$ python3.6 -m venv env  # Create the environment (only need be performed once)
$ source env/bin/activate  # Activate the environment
```

Set application configuration:

```sh
# Environment: development | testing | staging | production
$ export APP_SETTINGS=development
$ export SECRET_KEY=my_precious
$ export DATABASE_URL=postgres://username:password@localhost:5432/metagenscope_dev
$ export DATABASE_TEST_URL=postgres://username:password@localhost:5432/metagenscope_test
```

### Running Locally

Spin up server (runs on `http://127.0.0.1:5000/`):

```sh
$ python manage.py runserver
```

## Testing

The entry point to test suite tools is the `Makefile`.

### Linting

Code quality is enforced using pylint, pycodestyle, and pydocstyle. The rules are defined in `.pylintrc`.

These tools may be run together using:

```sh
$ make lint
```

### Running Test Suite

To run the test suite (will execute  `lint` prior to running tests):

```sh
$ make test
```

You may also run tests checking their coverage:

```sh
$ make cov
```

## Conntinuous Integration

The test suite is run automatically on CircleCI for each push to Github. You can skip this behavior for a commit by appending `[skip ci]` to the commit message.

### Custom Docker Postgres Image

CircleCI does not allow running commands on secondary containers (eg. the database). This means we cannot enable `uuid-ossp` on a stock postgres image and have to use our own. Fortunately, we already have a custom image -- we just have to build and publish it on Docker Hub. This only needs to be done when changes have been made to `./app/db/Dockerfile`.

Build and tag the image:

```sh
$ export COMMIT_SHA=`git rev-parse HEAD`
$ docker build -t imagebuildinprocess .
$ docker tag imagebuildinprocess "metagenscope/postgres:${COMMIT_SHA::8}"
```

Push the image:

```sh
$ docker login
$ docker push "metagenscope/postgres:${COMMIT_SHA::8}"
```

Clean up:

```sh
$ docker rmi imagebuildinprocess "metagenscope/postgres:${COMMIT_SHA::8}"
```

## Contributing

Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository][project-tags].

## Release History

See [`CHANGELOG.md`](CHANGELOG.md).

## Authors

* **Benjamin Chrobot** - _Initial work_ - [bchrobot](https://github.com/bchrobot)

See also the list of [contributors][contributors] who participated in this project.

## License

This project is licensed under the MIT License - see the [`LICENSE.md`](LICENSE.md) file for details.


[project-tags]: https://github.com/bchrobot/metagenscope-server/tags
[contributors]: https://github.com/bchrobot/metagenscope-server/contributors

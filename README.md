# MetaGenScope Server

[![CircleCI](https://circleci.com/gh/MetaGenScope/metagenscope-server/tree/master.svg?style=svg)](https://circleci.com/gh/MetaGenScope/metagenscope-server/tree/master)

> MetaGenScope server application.

## Getting Started

This readme documents how to run and test the MetaGenScope server as a standalone application. `metagenscope-server` is part of [`metagenscope-main`](https://github.com/metagenscope/metagenscope-main) and should usually be run as part of the complete stack.

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

A startup script is provided to ensure that the application does not attempt to start before all service dependencis are accepting connections. It can be used like so:

```
$ ./startup.sh [host:port[, host:port, ...]] -- [command]
```

An example of waiting for Postgres and Mongo DBs running on localhost before starting the application would look like this:

```
$ ./startup.sh localhost:5435 localhost:27020 -- python manage.py runserver
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

## Development

MetaGenScope uses the GitFlow branching strategy along with Pull Requests for code reviews. Check out [this post](https://devblog.dwarvesf.com/post/git-best-practices/) by the Dwarves Foundation for more information.

### Tool Result Modules

`ToolResult` modules define database storage and API upload for outputs.

To add a new `ToolResult` module write your new module `app/tool_results/my_new_module` following existing conventions. Make sure the main module class inherits from `ToolResultModule` and is named ending in `ResultModule`.

### Display Modules

`DisplayModule`s provide the backing data for each front-end visualization type. They are in charge of:

- Providing the data model for the visualization backing data
- Enumerating the `ToolResult` types that are valid data sources (_WIP_)
- The Middleware task that transforms a set of `Sample`s into the module's data model (_WIP_)

These modules live in `app/display_modules/` and are self-contained: all models, API endpoint definitions, long-running tasks, and tests live within each module.

To add a new `DisplayModule` module:
1. Write your new module `app/display_modules/my_new_module` following existing conventions. Make sure the main module class inherits from `DisplayModule` and is named ending in `Module`.
2. Add your module to `all_display_modules` in `app.display_modules`.

## Continuous Integration

The test suite is run automatically on CircleCI for each push to Github. You can skip this behavior for a commit by appending `[skip ci]` to the commit message.

### Custom Docker Database Images

CircleCI does not allow running commands on secondary containers (eg. the database). To get around this, we use custom images for our database images. Changes to either image need to be built, tagged, and pushed to Docker Hub before CI can succeed.

- **Postgres** - Stock Postgres image with the `uuid-ossp` extension enabled. Located at `./database_docker/postgres_db`.
- **Mongo** - Stock Mongo image with a healthcheck script added. Located at `./database_docker/mongo_db`.

**Steps**

From the appropriate database docker subdirectory, build and tag the image:

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


[project-tags]: https://github.com/metagenscope/metagenscope-server/tags
[contributors]: https://github.com/metagenscope/metagenscope-server/contributors

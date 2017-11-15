# MetaGenScope Server

> MetaGenScope server application.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You will need to have [`pip`](https://pip.pypa.io/en/stable/installing/) and [PostgreSQL](https://wiki.postgresql.org/wiki/Detailed_installation_guides) to run MetaGenScope.

It is also recommended that you use [Virtualenv](https://virtualenv.pypa.io/en/stable/), a tool to create isolated virtual environments, and [Autoenv](https://github.com/kennethreitz/autoenv) to automatically manage environment state.

### Installing

First thing you will need to do is configure your `.env` file.

```bash
cp .env.dist .env # Copy template
vi .env # Make required changes
source .env # Load the environment
```

Then install the Python requirements:

```bash
pip install -r requirements.txt
```

And finally, run the application

```bash
python manage.py runserver
```

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository][project-tags].

## Release History

See `CHANGELOG.md`

## Authors

* **Benjamin Chrobot** - _Initial work_ - [bchrobot](https://github.com/bchrobot)

See also the list of [contributors][contributors] who participated in this project.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.


[project-tags]: https://github.com/bchrobot/metagenscope-server/tags
[contributors]: https://github.com/bchrobot/metagenscope-server/contributors

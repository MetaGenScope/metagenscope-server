# MetaGenScope Server

> MetaGenScope server application.

## Getting Started

`metagenscope-server` is run as part of [`metagenscope-main`](https://github.com/bchrobot/metagenscope-main).

## Testing

The entry point to test suite tools is the `makefile`.

### Linting

Code quality is enforced using pylint, pycodestyle, and pydocstyle. The rules are defined in `.pylintrc`.

These tools may be run together using:

```sh
$ make lint
```

### Running Test Suite

To run the test suite (requires a successful `lint` execution prior to running tests):

```sh
$ make test
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

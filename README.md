<div align="center">
<a href="https://github.com/BDP25/grimoire">
<img src="images/logo.svg" alt="Logo" width="80" height="80">
</a>
<h3 align="center">grimoire</h3>
<p align="center">
Grimoire (gʀiˈmwaːʀ), a book of magical knowledge
<br/>
</p>
</div>

![Contributors](https://img.shields.io/github/contributors/BDP25/grimoire?color=dark-green)
![Issues](https://img.shields.io/github/issues/BDP25/grimoire)
![License](https://img.shields.io/github/license/BDP25/grimoire)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About the Project](#about-the-project)
- [Usage](#usage)
  - [Development](#development)
- [License](#license)
- [Contributors](#contributors)

## About the Project

## Usage

### Development

The project is using [uv](https://docs.astral.sh/uv/) as the python project manager. In addition [Poe the Poet](https://poethepoet.natn.io/index.html) is used to run
tasks.

Some important uv commands:

```shell
# install pyproject dependencies
uv sync

# install a package
uv add <package>
uv add <package> --dev

# run poe tasks
uv run poe all     # run all tasks
uv run poe format  # format code
uv run poe lint    # lint code
uv run poe types   # type check code
uv run poe test    # run tests
```

## License

## Contributors

See the [contributing guidelines](CONTRIBUTING.md) for more information.


**Project Authors:**

- Felix Céline (felixcel)
- Kiritharan Kirishana (kiritkir)
- Truninger John (trunijoh)

</br>
<a href="https://github.com/BDP25/grimoire/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=BDP25/grimoire" />
</a>

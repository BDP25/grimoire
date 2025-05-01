<div align="center">
<a href="https://github.com/BDP25/grimoire">
<img src="images/logo.svg" alt="Logo" width="80" height="80">
</a>
<h3 align="center">grimoire</h3>
<p align="center">
Grimoire (gʀiˈmwaːʀ), a book (tool) of magical knowledge about your code and its dependencies.
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

Ever joined a new software project with an unfamiliar tech stack? You’re faced with internal libraries, legacy code, scattered documentation, and dependency-breaking
changes. Typically, you’d rely on docs, Stack Overflow, code exploration, and now LLMs like ChatGPT. But these tools don’t fully understand your project’s
context—frustrating, right?

That’s why we built Grimoire. It’s a powerful client tool that leverages RAG (Retrieval-Augmented Generation) to deeply understand your code, documentation,
dependencies, and project structure. Grimoire acts as your personal AI assistant, helping you onboard faster, develop smarter, and navigate your project with ease.

- 🔍 Deep Code Understanding – Grimoire analyzes your entire codebase for better insights.
- 📚 Seamless Documentation Access – No more searching; get the right info instantly.
- 🧩 Smart Dependency Mapping – Know how everything connects in your project.

## Usage

First create a new Gemini API key in the [Google AI Studio](https://aistudio.google.com/app/apikey) and save it as `LLM_API_KEY` in your environment.

```shell
export LLM_API_KEY=<your-api-key>
```

Start the local pgvector database:

```shell
docker compose up -d
```

Then you can use the `grim` client to interact with grimoire.

```shell
# with the uv project context
uv run grim --help

# or if you have installed the package
grim --help
```

```text
 Usage: grim [OPTIONS] COMMAND [ARGS]...

 A cli which enables RAG for your project 🔮
 Prequsites:
 - Get an LLM API token (e.g. from https://aistudio.google.com/app/apikey)
 - Set the LLM_API_TOKEN environment variable to the token

╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                 │
╰─────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ──────────────────────────────────────────────────────────────────╮
│ version   Print the version of the grim cli                                 │
│ ask       Ask a question with project context                               │
│ flush     Flush the whole vectorstore                                       │
│ init      Initialize a new grimoire project                                 │
│ sync      Sync the grimoire project with existing configuration             │
│ update    Update the grimoire sources with the latest dependencies          │
│ verify    Verify the configuration of the project                           │
╰─────────────────────────────────────────────────────────────────────────────╯
```

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

# run a script
uv run python sandbox/text_ingestion.py

# run poe tasks
uv run poe all     # run all tasks
uv run poe format  # format code
uv run poe lint    # lint code
uv run poe types   # type check code
uv run poe test    # run tests
```

#### Working with Test Projects

To test a new project, you can simply add the project as submodule to the `test_projects` folder:

```shell
git submodule add <project-url> test_projects/<project-name>
```

Updating the submodule can be done with:

```shell
git submodule update --remote
```

## License

Distributed under the MIT License. See [LICENSE.md](LICENSE.md) for more information.

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

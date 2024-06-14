# My Python Playground: Practice & Experiment

## Create a Virtual Environment (venv)

Python 3.3 and later come with the `venv` module for creating virtual environments. Use the following command to create a virtual environment named `venv` within your project directory:

```bash
python -m venv venv
```

Alternative (Windows): On Windows, you might need to use `py -3 -m venv venv` if you have multiple Python versions installed.

## Install packages with pip and requirements.txt

The following command installs packages in bulk according to the configuration file, `requirements.txt`. In some environments, use `pip3` instead of `pip`.

```bash
pip install -r requirements.txt
```

The configuration file can be named arbitrarily, though `requirements.txt` is commonly used.

Place `requirements.txt` in the directory where you plan to run the command. If the file is in a different directory, specify its path, for example, `path/to/requirements.txt`.

### Installing Packages from URLs

You can also install packages directly from URLs. This is especially useful when you want to install a version of a package that’s not available on PyPI, or if you want to install a package from a private repository. Here’s an example:

```requirements
# requirements.txt

https://github.com/username/repository/archive/branch.zip
```

## How to write requirements.txt

An example of `requirements.txt` is as follows.

```requirements
# requirements.txt

###### Requirements without Version Specifiers ######
nose
nose-cov
beautifulsoup4
#
###### Requirements with Version Specifiers ######
#   See https://www.python.org/dev/peps/pep-0440/#version-specifiers
docopt == 0.6.1             # Version Matching. Must be version 0.6.1
keyring >= 4.1.1            # Minimum version 4.1.1
coverage != 3.5             # Version Exclusion. Anything except version 3.5
Mopidy-Dirble ~= 1.1        # Compatible release. Same as >= 1.1, == 1.*
```

## Create `requirements.txt` with `pip freeze`

`pip freeze` outputs the packages and their versions installed in the current environment in a format that can be used as `requirements.txt`.

```bash
$ pip freeze
agate==1.6.0
agate-dbf==0.2.0
agate-excel==0.2.1
agate-sql==0.5.2
...
```

Using the redirection operator `>`, you can save the output of `pip freeze` to a file. This file can be used to install the same versions of packages in a different environment.

First, redirect the output of `pip freeze` to a file named `requirements.txt`.

```bash
pip freeze > requirements.txt
```

Next, copy or move this `requirements.txt` to a different environment and use it to install the packages.

```bash
pip install -r requirements.txt
```

By following these steps, you can easily replicate the exact package setup from one environment to another.

## Leveraging Docker for Isolated Environments

Docker is another alternative for managing Python packages. It allows you to create isolated environments, called containers, where you can run your Python applications with their dependencies.

```Docker
# Dockerfile
FROM python:3.7
WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
CMD [ "python", "./your_script.py" ]
```

## Troubleshoots

> Could not install packages due to an OSError: [WinError 2] The system cannot find the file specified: 'C:\\Python312\\Scripts\\f2py.exe'

Try running the command as administrator or `pip install 'package name' --user` to install numpy without any special previlages.

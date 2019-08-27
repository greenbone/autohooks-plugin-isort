# Release instructions

Before creating a new release please do a careful consideration about the
version number for the new release. We are following [Semantic Versioning](https://semver.org/)
and [PEP440](https://www.python.org/dev/peps/pep-0440/).

* Install development dependencies

  ```sh
  pipenv install --dev
  ```

* Fetch upstream changes and create release branch

  ```sh
  git fetch upstream
  git checkout -b create-new-release upstream/master
  ```

* Open [setup.py](setup.py) and increment the version number

* Update [CHANGELOG](CHANGELOG.md)

* Create distribution files

  ```sh
  rm -rf dist build autohooks_plugin_isort.egg-info
  python3 setup.py sdist bdist_wheel
  ```

* Create a git commit

  ```sh
  git add .
  git commit -m "Prepare release <version>"
  ```

* Create a `.pypirc` file

  ```sh
  vim ~/.pypirc
  ```

  with the following content (Note: `<username>` must be replaced)

  ```ini
  [distutils]
  index-servers =
      pypi
      testpypi

  [pypi]
  username = <username>

  [testpypi]
  repository = https://test.pypi.org/legacy/
  username = <username>
  ```

* If necessary, create an account at [Test PyPI](https://packaging.python.org/guides/using-testpypi/)

* Upload the archives in dist to [Test PyPI](https://test.pypi.org/)

  ```sh
  twine upload -r testpypi dist/*
  ```

* Check if the package is available at https://test.pypi.org/project/autohooks-plugin-isort

* Create a test directory

  ```sh
  mkdir autohooks-install-test
  cd autohooks-install-test
  pipenv run pip install --pre -I --extra-index-url https://test.pypi.org/simple/ autohooks-plugin-isort
  ```

* Remove test environment

  ```sh
  pipenv --rm
  cd ..
  rm -rf autohooks-install-test
  ```

* Create a release PR

  ```sh
  git push origin
  ```
  Open GitHub and create a PR against https://github.com/greenbone/autohooks-plugin-isort

* Update after PR is merged

  ```sh
  git fetch upstream
  git rebase upstream/master
  ```
* Create a git tag

  ```sh
  git tag v<version>
  ```

  or even signed with your gpg key

  ```sh
  git tag -s v<version>
  ```
* Create final distribution files

  ```sh
  rm -rf dist build autohooks_plugin_isort.egg-info
  python3 setup.py sdist bdist_wheel
  ```

* If necessary, create an account at [PyPI](https://pypi.org/)

* Upload to the real [PyPI](https://pypi.org/)

  ```sh
  twine upload dist/*
  ```

* Check if new version is available at https://pypi.org/project/autohooks-plugin-isort

* Update version in [setup.py](setup.py)

  Use a alpha version like `(1, 1, 1, 'alpha')` or
  `(1, 1, 1, 'alpha', 0)`

* Create a commit

  ```sh
  git add setup.py
  git commit -m "Update version after <version> release"
  ```

* Push changes and tag to GitHub

  ```sh
  git push --tags upstream master
  ```

===================
Anemoi Environments
===================

|Maturity| |CI Test| |CI Publish|

.. |Maturity| image:: https://github.com/ecmwf/codex/raw/refs/heads/main/Project%20Maturity/emerging_badge.svg
   :target: https://github.com/ecmwf/codex/blob/main/Project%20Maturity/readme.md
   :alt: Project Maturity: Emerging

.. |CI Test| image:: https://github.com/MeteoSwiss/anemoi-env/actions/workflows/CI_test.yaml/badge.svg
   :target: https://github.com/MeteoSwiss/anemoi-env/actions/workflows/CI_test.yaml
   :alt: CI Test Status

.. |CI Publish| image:: https://github.com/MeteoSwiss/anemoi-env/actions/workflows/CI_publish.yaml/badge.svg
   :target: https://github.com/MeteoSwiss/anemoi-env/actions/workflows/CI_publish.yaml
   :alt: CI Publish Status

Provides a reproducible, versioned Python environment for Anemoi experiments.

**anemoi-env** is a meta-package that defines a standardized set of dependencies for machine learning and data science workflows. It contains no source code—only dependency declarations that are automatically versioned and published weekly.

Installation
------------

Stable Release (Locked Dependencies)
'''''''''''''''''''''''''''''''''''''

For reproducible environments, install a specific calendar-versioned release from PyPI:

.. code-block:: console

    $ pip install anemoi-env==2025.10.10

Or install the latest locked version from the main branch:

.. code-block:: console

    $ pip install git+https://github.com/MeteoSwiss/anemoi-env.git@main

Development (Flexible Dependencies)
'''''''''''''''''''''''''''''''''''

For development with the **latest Anemoi features from main branches** (no lock file):

.. code-block:: console

    $ pip install git+https://github.com/MeteoSwiss/anemoi-env.git@dev

**Warning**: The dev branch uses bleeding-edge dependencies and may be unstable.

Feature Testing (Fixed Commit SHAs)
'''''''''''''''''''''''''''''''''''

For testing specific features with reproducible Anemoi commits, create a feature branch from **main** (not dev):

.. code-block:: console

    $ git checkout main
    $ git checkout -b feature-test/new-graphs

Then edit ``pyproject.toml`` to pin specific commits:

.. code-block:: toml

    [tool.poetry.dependencies]
    anemoi-datasets = { git = "https://github.com/ecmwf/anemoi-datasets", rev = "abc123def" }
    anemoi-graphs = { git = "https://github.com/ecmwf/anemoi-core.git", subdirectory = "graphs", rev = "def456abc" }
    # ... other packages with fixed revisions

Run ``poetry lock`` to generate a lock file for this specific combination, then install:

.. code-block:: console

    $ poetry lock
    $ poetry install

This approach provides reproducibility while testing bleeding-edge features before they're released to PyPI.

Branching Strategy
------------------

This repository uses a multi-branch strategy with different dependency sources:

* **main**: Contains ``poetry.lock`` and uses **stable PyPI releases** of all dependencies. Updated automatically every Monday via CI. Each update creates a calendar-versioned release (e.g., ``2025.10.10``) and publishes to PyPI. Use this for reproducible, production-ready environments.

* **dev**: Contains ``pyproject.toml`` with **no lock file** and uses **bleeding-edge versions** from Anemoi package main branches (via git dependencies). Used for development against the latest Anemoi features. Not published to PyPI.

* **feature-test/**: Custom feature branches with **fixed commit SHAs** for each Anemoi package. Includes ``poetry.lock`` for reproducible testing of specific feature combinations. Useful for validating new features before they reach PyPI. Not published.

Continuous Integration
----------------------

The repository includes automated CI/CD workflows:

* **CI Test** (``CI_test.yaml``): Runs on every push and pull request. Tests installation and verifies that all Anemoi packages can be imported successfully.

* **CI Publish** (``CI_publish.yaml``): Runs every Monday at 3 AM UTC. Automatically:

  1. Updates ``poetry.lock`` with latest compatible versions
  2. Checks if any dependencies have changed
  3. If changes detected:

     * Updates version to current date (``YYYY.MM.DD``)
     * Runs ``scripts/update_changelog.py`` to document Anemoi package versions
     * Creates a git tag
     * Publishes the new release to PyPI

  4. If no changes, skips publishing

This ensures weekly snapshots of the Anemoi ecosystem are automatically published when updates are available.

Versioning
----------

Uses **Calendar Versioning (CalVer)**: ``YYYY.MM.DD``

Each weekly release represents a snapshot of the dependency tree at that point in time.

What's Included
---------------

* **Anemoi Packages**:

  * ``anemoi-datasets``
  * ``anemoi-graphs``
  * ``anemoi-inference``
  * ``anemoi-models``
  * ``anemoi-registry``
  * ``anemoi-training``
  * ``anemoi-utils``

Development Setup with Poetry
-----------------------------

**Note**: This package is a meta-package with no source code. Development primarily involves updating dependencies in ``pyproject.toml``.

Local Development
'''''''''''''''''

Clone and install in development mode:

.. code-block:: console

    $ git clone https://github.com/MeteoSwiss/anemoi-env.git
    $ cd anemoi-env
    $ git checkout dev
    $ poetry install

Generate Documentation
''''''''''''''''''''''

.. code-block:: console

    $ poetry run sphinx-build doc doc/_build

Then open the index.html file generated in *anemoi-env/doc/_build/*.

Usage For Reproducible Research
'''''''''''''''''''''''''''''''

Always specify the exact version in your project dependencies:

**For stable PyPI releases:**

.. code-block:: toml

    [tool.poetry.dependencies]
    anemoi-env = "2025.10.10"

Or in ``requirements.txt``:

.. code-block:: text

    anemoi-env==2025.10.10

**For testing specific feature combinations:**

.. code-block:: toml

    [tool.poetry.dependencies]
    anemoi-env = { git = "https://github.com/MeteoSwiss/anemoi-env.git", rev = "feature-test/new-graphs" }

This ensures your research uses a specific, reproducible set of dependencies—either from PyPI (stable) or from a pinned feature branch (testing).

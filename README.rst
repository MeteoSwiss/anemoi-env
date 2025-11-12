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

.. |release_version| replace:: 2025.11.1

Provides a reproducible, versioned Python environment for Anemoi experiments.

**anemoi-env** is a meta-package that defines a standardized set of dependencies for machine learning and data science workflows. It contains no source code—only dependency declarations that are automatically versioned and published monthly.

Installation
------------

Stable Release (Locked Dependencies)
'''''''''''''''''''''''''''''''''''''

For reproducible environments, install a specific calendar-versioned release from PyPI:

.. parsed-literal::

    $ pip install anemoi-env==\ |release_version|

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

Advanced Installation
---------------------

CUDA-Specific PyTorch Versions
''''''''''''''''''''''''''''''

By default, ``anemoi-env`` installs PyTorch with CPU support or CUDA support based on what's available in the default PyPI index. To install a **specific CUDA version** (e.g., CUDA 12.1), use PyTorch's extra index URL:

.. parsed-literal::

    $ pip install anemoi-env==\ |release_version| --extra-index-url https://download.pytorch.org/whl/cu121
    $ pip install anemoi-env==\ |release_version| --extra-index-url https://download.pytorch.org/whl/cpu

Installing Anemoi Package Extras
''''''''''''''''''''''''''''''''

Some Anemoi packages provide optional features via extras (e.g., ``anemoi-graphs[tri]`` for trimesh support). To use these extras while respecting the tested dependency versions from ``anemoi-env``:

.. parsed-literal::

    $ pip install anemoi-env==\ |release_version|
    $ pip install "anemoi-graphs[tri]"

**Why install in two steps?**

* Installing ``anemoi-env`` first locks all core Anemoi packages to tested, compatible versions
* Installing the extra second (e.g., ``[tri]``) adds optional dependencies (like ``trimesh``) with version constraints that are compatible with the already-installed ``anemoi-graphs``
* If you directly ``pip install trimesh`` without the extra, you might get an incompatible version that hasn't been tested with Anemoi

Always check each Anemoi package's documentation for available extras.

Branching Strategy
------------------

This repository uses a multi-branch strategy with different dependency sources:

* **main**: Contains ``poetry.lock`` and uses **stable PyPI releases** of all dependencies. Updated automatically on the 1st of every month via CI. Each update creates a calendar-versioned release (e.g., ``2025.10.0``) and publishes to PyPI. Use this for reproducible, production-ready environments.

* **dev**: Contains ``pyproject.toml`` with **no lock file** and uses **bleeding-edge versions** from Anemoi package main branches (via git dependencies). Used for development against the latest Anemoi features. Not published to PyPI.

* **feature-test/**: Custom feature branches with **fixed commit SHAs** for each Anemoi package. Includes ``poetry.lock`` for reproducible testing of specific feature combinations. Useful for validating new features before they reach PyPI. Not published.

Continuous Integration
----------------------

The repository includes automated CI/CD workflows:

* **CI Test** (``CI_test.yaml``): Runs on every push and pull request. Tests installation and verifies that all Anemoi packages can be imported successfully.

* **CI Publish** (``CI_publish.yaml``): Runs on the 1st of every month at 3 AM UTC. Automatically:

  1. Updates ``poetry.lock`` with latest compatible versions
  2. Updates version to current date (``YYYY.MM.patch``)
  3. Updates Changelogs with the new release information
  4. Creates a git tag
  5. Publishes the new release to PyPI

This ensures monthly snapshots of the Anemoi ecosystem are automatically published when updates are available.

Versioning
----------

Uses **Calendar Versioning (CalVer)**: ``YYYY.MM.patch``

Each monthly release represents a snapshot of the dependency tree at that point in time. The patch number increments for additional releases within the same month (e.g., ``2025.10.0``, ``2025.10.1``, ``2025.11.0``).

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

In ``pyproject.toml``:

.. parsed-literal::

    [tool.poetry.dependencies]
    anemoi-env = "|release_version|"

Or in ``requirements.txt``:

.. parsed-literal::

    anemoi-env==\ |release_version|

**For testing specific feature combinations:**

.. code-block:: toml

    [tool.poetry.dependencies]
    anemoi-env = { git = "https://github.com/MeteoSwiss/anemoi-env.git", rev = "feature-test/new-graphs" }

This ensures your research uses a specific, reproducible set of dependencies—either from PyPI (stable) or from a pinned feature branch (testing).

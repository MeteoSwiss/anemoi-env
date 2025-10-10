#!/usr/bin/env python3
"""
Generate changelog from poetry.lock file showing Anemoi package versions.
"""

import re
from datetime import datetime


def parse_poetry_lock(lock_file="poetry.lock"):
    """Parse poetry.lock and extract Anemoi package versions."""
    anemoi_packages = {}
    current_package = None

    with open(lock_file, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('name = '):
                match = re.search(r'name = "([^"]+)"', line)
                if match:
                    current_package = match.group(1)

            elif line.startswith('version = ') and current_package and current_package.startswith('anemoi-'):
                match = re.search(r'version = "([^"]+)"', line)
                if match:
                    anemoi_packages[current_package] = match.group(1)
                    current_package = None

    return anemoi_packages


def read_current_version(pyproject_file="pyproject.toml"):
    """Read current version from pyproject.toml."""
    with open(pyproject_file, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('version = '):
                match = re.search(r'version = "([^"]+)"', line)
                if match:
                    return match.group(1)
    return "unknown"


def generate_changelog_entry(version, anemoi_packages):
    """Generate a changelog entry for the current version."""
    entry = f"\n## Version {version} ({datetime.now().strftime('%Y-%m-%d')})\n\n"
    entry += "### Anemoi Package Versions\n\n"

    for package in sorted(anemoi_packages.keys()):
        entry += f"- **{package}**: `{anemoi_packages[package]}`\n"

    return entry


def update_changelog(changelog_file="CHANGELOG.rst"):
    """Update CHANGELOG.rst with current Anemoi package versions."""
    version = read_current_version()
    anemoi_packages = parse_poetry_lock()

    if not anemoi_packages:
        print("No Anemoi packages found in poetry.lock")
        return

    try:
        with open(changelog_file, 'r', encoding='utf8') as f:
            existing_content = f.read()
    except FileNotFoundError:
        existing_content = "=========\nChangelog\n=========\n\n"

    _entry = generate_changelog_entry(version, anemoi_packages)

    if f"Version {version}" in existing_content:
        print(f"Version {version} already exists in changelog. Updating...")
        lines = existing_content.split('\n')
        new_lines = []
        skip = False
        for i, line in enumerate(lines):
            if f"Version {version}" in line:
                skip = True
            elif skip and (line.startswith("## Version") or line.startswith("Version ")):
                skip = False

            if not skip:
                new_lines.append(line)
        existing_content = '\n'.join(new_lines)

    lines = existing_content.split('\n')
    header_end = 3

    entry_lines = [
        "",
        f"Version {version} ({datetime.now().strftime('%Y-%m-%d')})",
        "=" * len(f"Version {version} ({datetime.now().strftime('%Y-%m-%d')})"),
        "",
        "Anemoi Package Versions",
        "------------------------",
        "",
    ]

    for package in sorted(anemoi_packages.keys()):
        entry_lines.append(f"* **{package}**: ``{anemoi_packages[package]}``")

    new_lines = lines[:header_end] + entry_lines + lines[header_end:]

    with open(changelog_file, 'w', encoding='utf8') as f:
        f.write('\n'.join(new_lines))

    print(f"✅ Updated {changelog_file} with version {version}")
    print(f"   Found {len(anemoi_packages)} Anemoi packages")


if __name__ == "__main__":
    update_changelog()

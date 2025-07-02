# Report

## Introduction
- This document provides a detailed guide on automating the extraction, processing, and mapping of GitHub commits using Python and Nomic Atlas.
- The primary objective is to visualize trends and patterns in commit histories, enabling users to explore metadata such as authors, emails, timestamps, and commit messages.
- Key findings include the ability to process large datasets like the Linux Kernel repository and generate interactive maps for data exploration.

## Section 1: Getting Started
- The guide uses the Linux Kernel repository as an example, showcasing its over one million commits (as of June 2024).
- Users can explore commit history trends, filter by timestamps, and analyze changes in project focus over time (e.g., legal compliance vs. bug fixes).
- The process involves:
  - Cloning a repository.
  - Extracting commit metadata.
  - Creating a data map using Nomic Atlas.

## Section 2: Cloning Repository
- The first step is cloning the GitHub repository locally using the `git` command.
  - Example: `subprocess.run(['git', 'clone', '--mirror', repo_url, repo_path])`.
- If the repository is already cloned, the script fetches updates using `git fetch --all`.

## Section 3: Extracting Commit Metadata
- Metadata such as commit hash, author, email, date, and message is extracted using `git log`.
- The `datetime` library formats timestamps for filtering and visualization.
- Error handling is implemented to skip commits with parsing issues, ensuring data integrity.

## Section 4: Saving Repository as CSV
- Commit data is saved into a CSV file for debugging or offline analysis.
- The CSV includes columns: `id`, `hash`, `author`, `email`, `date`, and `message`.
- Python's `csv.DictWriter` is used for structured data storage.

## Section 5: Creating a Map Using Atlas
- The Nomic Atlas API is used to create interactive maps from the extracted commit data.
- Prerequisites include installing the Nomic library (`pip install --upgrade nomic`) and logging in with an API token.
- Two methods are provided:
  - Creating a map directly from a list of commits.
  - Creating a map from a CSV file for debugging purposes.
- Example: `dataset.create_index(indexed_field='message')` generates a map based on commit messages.

## Section 6: Bringing It All Together
- The driver script integrates all steps:
  - Prompts the user for repository URLs and whether to save commits to a CSV file.
  - Clones repositories, extracts commits, and stores them in a temporary directory.
  - Generates a combined commit map, either from a CSV or directly from the commit data.
- Example output: Maps are created in the Nomic Atlas account, with links provided in the terminal for easy access.

## Section 7: Exploring Your Map
- Generated maps allow users to explore commit histories interactively.
- Larger datasets (e.g., Linux Kernel) may take up to 40 minutes to process, with email notifications sent upon completion.
- Users can filter by timestamps and analyze semantic changes in commit messages over time.

## Conclusion
- The guide demonstrates a robust workflow for visualizing GitHub commit histories using Nomic Atlas.
- Key benefits include the ability to process large repositories, generate interactive maps, and explore trends in commit data.
- This approach is scalable and adaptable for various projects, enabling deeper insights into software development patterns.
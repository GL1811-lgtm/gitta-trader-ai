# How to Upload Code to GitHub

This guide provides the basic steps to upload your code to a GitHub repository.

### Prerequisites

*   You have a GitHub account.
*   You have Git installed on your local machine.
*   You have a GitHub repository created.
*   You have cloned the repository to your local machine or initialized a new git repository.

### Instructions

1.  **Open your terminal or command prompt.**

2.  **Navigate to your project's root directory.**
    ```bash
    cd path/to/your/project
    ```

3.  **Check the status of your repository.** This will show you which files have been modified.
    ```bash
    git status
    ```

4.  **Stage your changes.** This adds your modified files to the commit. To add all files, use:
    ```bash
    git add .
    ```
    To add a specific file, use:
    ```bash
    git add <file-name>
    ```

5.  **Commit your changes.** This saves your staged changes with a descriptive message.
    ```bash
    git commit -m "Your detailed commit message here"
    ```

6.  **Push your changes to GitHub.** This uploads your committed changes to the remote repository. If your main branch is named `main`, use:
    ```bash
    git push origin main
    ```
    If your main branch is named `master`, use:
    ```bash
    git push origin master
    ```

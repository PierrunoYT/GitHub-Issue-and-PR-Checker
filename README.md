# GitHub Issue and PR Checker

A fast, concurrent Python tool to check open issues and pull requests across all your GitHub repositories.

## Features

- 🚀 **High Performance**: Concurrent processing of repositories (5x faster than sequential)
- 📊 **Smart Pagination**: Limits results to prevent excessive API calls
- 🔒 **Secure**: Uses GitHub personal access tokens with environment variable support
- 📈 **Summary Statistics**: Shows total counts and processing time
- ⚡ **Optimized API Usage**: Efficient GitHub API calls with proper pagination
- 🛡️ **Error Handling**: Individual repository errors don't crash the entire process

## Requirements

- Python 3.6+
- PyGithub library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/PierrunoYT/GitHub-Issue-and-PR-Checker.git
   cd "GitHub-Issue-and-PR-Checker"
   ```

2. Install dependencies:
   ```bash
   pip install PyGithub
   ```

3. Create a GitHub Personal Access Token:
   - Go to https://github.com/settings/tokens
   - Click "Generate new token (classic)"
   - Select the `repo` scope
   - Copy the generated token

## Usage

### Option 1: Environment Variable (Recommended)
```bash
# Set your token as an environment variable
export GITHUB_TOKEN=your_personal_access_token_here

# Run the script
python github_checker.py
```

### Option 2: Interactive Input
```bash
# Run the script and enter token when prompted
python github_checker.py
```

## Sample Output

```
--- GitHub Issue and PR Checker ---
This script checks for open issues and pull requests in your repositories.
You will need a GitHub personal access token with 'repo' scope.
You can create one at: https://github.com/settings/tokens
To avoid entering the token every time, you can set it as an environment variable named 'GITHUB_TOKEN'.

Authenticated as: your_username

Fetching your repositories...
Found 15 repositories. Processing...

--- Results (processed in 2.34 seconds) ---

--- Repository: your_username/project1 ---
  [Issue #42] Fix authentication bug
    - Author: collaborator1
    - URL: https://github.com/your_username/project1/issues/42
  [PR #43] Add new feature
    - Author: contributor2
    - URL: https://github.com/your_username/project1/pull/43

--- Repository: your_username/project2 ---
  No open issues.
  No open pull requests.

--- Summary ---
Total repositories: 15
Total open issues: 8
Total open PRs: 12
```

## Performance Optimizations

- **Concurrent Processing**: Uses ThreadPoolExecutor with 5 workers
- **Pagination Limits**: Maximum 50 issues and 50 PRs per repository
- **Efficient API Calls**: Uses `per_page=100` for optimal GitHub API usage
- **Smart Filtering**: Separates issues from pull requests efficiently

## Security

- Tokens are handled securely and never stored in code
- Environment variable support prevents accidental token exposure
- No token is displayed in output or logs

## Troubleshooting

### Rate Limiting
If you hit GitHub's rate limit:
- The script includes built-in error handling
- Wait a few minutes and try again
- Consider reducing the number of concurrent workers in the code

### Authentication Issues
- Ensure your token has `repo` scope
- Check that the token hasn't expired
- Verify the token is correctly set in the environment variable

### No Repositories Found
- Make sure you own repositories (not just collaborating)
- Check that your token has access to the repositories

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

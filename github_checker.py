import os
from github import Github
from getpass import getpass
import concurrent.futures
from threading import Lock
import time

def get_github_token():
    """Gets the GitHub token from an environment variable or prompts the user."""
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GitHub token not found in GITHUB_TOKEN environment variable.")
        token = getpass("Enter your GitHub personal access token: ")
    return token

def process_repository(repo_data, g):
    """Process a single repository to get issues and PRs."""
    repo_name, repo = repo_data
    results = {"repo_name": repo_name, "issues": [], "prs": [], "error": None}
    
    try:
        # Get issues (excluding PRs) with pagination limit
        issues = repo.get_issues(state="open")
        issue_count = 0
        for issue in issues:
            if not issue.pull_request and issue_count < 50:  # Limit to 50 issues per repo
                results["issues"].append({
                    "number": issue.number,
                    "title": issue.title,
                    "author": issue.user.login,
                    "url": issue.html_url
                })
                issue_count += 1
            elif issue_count >= 50:
                break

        # Get PRs with pagination limit
        pulls = repo.get_pulls(state="open")
        pr_count = 0
        for pr in pulls:
            if pr_count < 50:  # Limit to 50 PRs per repo
                results["prs"].append({
                    "number": pr.number,
                    "title": pr.title,
                    "author": pr.user.login,
                    "url": pr.html_url
                })
                pr_count += 1
            else:
                break
                
    except Exception as e:
        results["error"] = str(e)
    
    return results

def main():
    """
    Main function to fetch and display GitHub issues and pull requests.
    """
    token = get_github_token()
    if not token:
        print("No GitHub token provided. Exiting.")
        return

    try:
        g = Github(token, per_page=100)  # Optimize pagination
        user = g.get_user()
        print(f"Authenticated as: {user.login}")

        print("\nFetching your repositories...")
        repos = list(g.get_user().get_repos())
        user_repos = [(repo.full_name, repo) for repo in repos if repo.owner.login == user.login]
        
        print(f"Found {len(user_repos)} repositories. Processing...")
        start_time = time.time()
        
        # Process repositories concurrently
        results = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(process_repository, repo_data, g): repo_data[0] 
                             for repo_data in user_repos}
            
            for future in concurrent.futures.as_completed(future_to_repo):
                repo_name = future_to_repo[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    print(f"Error processing {repo_name}: {e}")

        # Display results
        print(f"\n--- Results (processed in {time.time() - start_time:.2f} seconds) ---")
        
        total_issues = 0
        total_prs = 0
        
        for result in results:
            if result["error"]:
                print(f"\n--- Repository: {result['repo_name']} (Error: {result['error']}) ---")
                continue
                
            print(f"\n--- Repository: {result['repo_name']} ---")
            
            # Display issues
            if result["issues"]:
                for issue in result["issues"]:
                    print(f"  [Issue #{issue['number']}] {issue['title']}")
                    print(f"    - Author: {issue['author']}")
                    print(f"    - URL: {issue['url']}")
                total_issues += len(result["issues"])
            else:
                print("  No open issues.")

            # Display PRs
            if result["prs"]:
                for pr in result["prs"]:
                    print(f"  [PR #{pr['number']}] {pr['title']}")
                    print(f"    - Author: {pr['author']}")
                    print(f"    - URL: {pr['url']}")
                total_prs += len(result["prs"])
            else:
                print("  No open pull requests.")
        
        print(f"\n--- Summary ---")
        print(f"Total repositories: {len(results)}")
        print(f"Total open issues: {total_issues}")
        print(f"Total open PRs: {total_prs}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    print("--- GitHub Issue and PR Checker ---")
    print("This script checks for open issues and pull requests in your repositories.")
    print("You will need a GitHub personal access token with 'repo' scope.")
    print("You can create one at: https://github.com/settings/tokens")
    print("To avoid entering the token every time, you can set it as an environment variable named 'GITHUB_TOKEN'.")
    main()

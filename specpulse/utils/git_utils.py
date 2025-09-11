"""
Git utilities for SpecPulse
"""

import subprocess
from pathlib import Path
from typing import Optional, List, Tuple


class GitUtils:
    """Git operations utility class"""
    
    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()
    
    def _run_git_command(self, *args) -> Tuple[bool, str]:
        """Run a git command and return success status and output"""
        try:
            result = subprocess.run(
                ["git"] + list(args),
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stderr.strip()
        except FileNotFoundError:
            return False, "Git is not installed or not in PATH"
    
    def check_git_installed(self) -> bool:
        """Check if git is installed"""
        success, _ = self._run_git_command("--version")
        return success
    
    def is_git_repo(self, path: Optional[Path] = None) -> bool:
        """Check if directory is a git repository"""
        check_path = path or self.repo_path
        git_dir = check_path / ".git"
        return git_dir.exists() and git_dir.is_dir()
    
    def init_repo(self) -> bool:
        """Initialize a new git repository"""
        success, _ = self._run_git_command("init")
        return success
    
    def get_current_branch(self) -> Optional[str]:
        """Get current branch name"""
        success, output = self._run_git_command("branch", "--show-current")
        return output if success else None
    
    def create_branch(self, branch_name: str) -> bool:
        """Create and checkout a new branch"""
        success, _ = self._run_git_command("checkout", "-b", branch_name)
        return success
    
    def checkout_branch(self, branch_name: str) -> bool:
        """Checkout an existing branch"""
        success, _ = self._run_git_command("checkout", branch_name)
        return success
    
    def get_branches(self) -> List[str]:
        """Get list of all branches"""
        success, output = self._run_git_command("branch", "-a")
        if success:
            branches = []
            for line in output.split('\n'):
                line = line.strip()
                if line:
                    # Remove the * for current branch
                    if line.startswith('*'):
                        line = line[2:]
                    branches.append(line.strip())
            return branches
        return []
    
    def add_files(self, files: Optional[List[str]] = None) -> bool:
        """Add files to staging area"""
        if files:
            success, _ = self._run_git_command("add", *files)
        else:
            success, _ = self._run_git_command("add", ".")
        return success
    
    def commit(self, message: str) -> bool:
        """Create a commit with message"""
        success, _ = self._run_git_command("commit", "-m", message)
        return success
    
    def get_status(self) -> Optional[str]:
        """Get git status"""
        success, output = self._run_git_command("status", "--short")
        return output if success else None
    
    def has_changes(self) -> bool:
        """Check if there are uncommitted changes"""
        status = self.get_status()
        return bool(status) if status is not None else False
    
    def get_log(self, limit: int = 10) -> List[str]:
        """Get recent commit log"""
        success, output = self._run_git_command(
            "log", 
            f"--oneline", 
            f"-{limit}"
        )
        if success:
            return output.split('\n') if output else []
        return []
    
    def stash_changes(self, message: Optional[str] = None) -> bool:
        """Stash current changes"""
        if message:
            success, _ = self._run_git_command("stash", "push", "-m", message)
        else:
            success, _ = self._run_git_command("stash")
        return success
    
    def apply_stash(self, stash_id: Optional[str] = None) -> bool:
        """Apply stashed changes"""
        if stash_id:
            success, _ = self._run_git_command("stash", "apply", stash_id)
        else:
            success, _ = self._run_git_command("stash", "apply")
        return success
    
    def get_remote_url(self, remote: str = "origin") -> Optional[str]:
        """Get remote repository URL"""
        success, output = self._run_git_command("remote", "get-url", remote)
        return output if success else None
    
    def push(self, branch: Optional[str] = None, force: bool = False) -> bool:
        """Push commits to remote"""
        args = ["push"]
        if force:
            args.append("--force")
        if branch:
            args.extend(["origin", branch])
        
        success, _ = self._run_git_command(*args)
        return success
    
    def pull(self, branch: Optional[str] = None) -> bool:
        """Pull changes from remote"""
        args = ["pull"]
        if branch:
            args.extend(["origin", branch])
        
        success, _ = self._run_git_command(*args)
        return success
    
    def get_diff(self, staged: bool = False) -> Optional[str]:
        """Get diff of changes"""
        args = ["diff"]
        if staged:
            args.append("--staged")
        
        success, output = self._run_git_command(*args)
        return output if success else None
    
    def tag(self, tag_name: str, message: Optional[str] = None) -> bool:
        """Create a tag"""
        args = ["tag"]
        if message:
            args.extend(["-a", tag_name, "-m", message])
        else:
            args.append(tag_name)
        
        success, _ = self._run_git_command(*args)
        return success
    
    def get_tags(self) -> List[str]:
        """Get list of tags"""
        success, output = self._run_git_command("tag", "-l")
        if success:
            return output.split('\n') if output else []
        return []
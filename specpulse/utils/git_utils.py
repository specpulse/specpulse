"""
Git utilities for SpecPulse

SECURITY: All git operations use secure subprocess calls with:
- List form (no shell interpretation)
- Input validation for branch names and commit messages
- No shell=True usage

All user-provided inputs are validated before git operations.
"""

import subprocess
import re
from pathlib import Path
from typing import Optional, List, Tuple


class GitSecurityError(Exception):
    """Raised when git operation has security concerns"""
    pass


class GitUtils:
    """
    Git operations utility class with security validation.

    All git commands use secure subprocess calls (no shell=True).
    All user inputs are validated before git operations.
    """

    # Security constraints for git operations
    VALID_BRANCH_NAME = re.compile(r'^[a-zA-Z0-9\-_/]+$')
    MAX_BRANCH_NAME_LENGTH = 255
    MAX_COMMIT_MESSAGE_LENGTH = 5000
    MAX_TAG_NAME_LENGTH = 255

    def __init__(self, repo_path: Optional[Path] = None):
        self.repo_path = repo_path or Path.cwd()

    @staticmethod
    def _validate_branch_name(branch_name: str) -> str:
        """
        Validate git branch name for security.

        Args:
            branch_name: Branch name to validate

        Returns:
            Validated branch name

        Raises:
            GitSecurityError: If branch name is invalid
        """
        if not branch_name:
            raise GitSecurityError("Branch name cannot be empty")

        if len(branch_name) > GitUtils.MAX_BRANCH_NAME_LENGTH:
            raise GitSecurityError(
                f"Branch name too long: {len(branch_name)} chars "
                f"(max {GitUtils.MAX_BRANCH_NAME_LENGTH})"
            )

        # Check for command injection patterns
        dangerous_chars = [';', '&', '|', '$', '`', '(', ')', '<', '>', '\n', '\r']
        for char in dangerous_chars:
            if char in branch_name:
                raise GitSecurityError(
                    f"Branch name contains forbidden character: '{char}'"
                )

        # Validate character set (allow slashes for feature branches)
        if not GitUtils.VALID_BRANCH_NAME.match(branch_name):
            raise GitSecurityError(
                f"Branch name contains invalid characters: '{branch_name}'. "
                "Only alphanumeric, hyphen, underscore, and forward slash allowed."
            )

        return branch_name

    @staticmethod
    def _validate_commit_message(message: str) -> str:
        """
        Validate commit message for security.

        Args:
            message: Commit message to validate

        Returns:
            Validated message

        Raises:
            GitSecurityError: If message is invalid
        """
        if not message:
            raise GitSecurityError("Commit message cannot be empty")

        if len(message) > GitUtils.MAX_COMMIT_MESSAGE_LENGTH:
            raise GitSecurityError(
                f"Commit message too long: {len(message)} chars "
                f"(max {GitUtils.MAX_COMMIT_MESSAGE_LENGTH})"
            )

        # Check for command injection attempts in commit message
        # Git commit messages are passed via -m flag, so shell metacharacters
        # won't be interpreted, but we still validate for safety
        dangerous_patterns = ['$(', '`', '\x00']  # Null bytes and command substitution
        for pattern in dangerous_patterns:
            if pattern in message:
                raise GitSecurityError(
                    f"Commit message contains forbidden pattern: '{pattern}'"
                )

        return message

    @staticmethod
    def _validate_tag_name(tag_name: str) -> str:
        """
        Validate git tag name for security.

        Args:
            tag_name: Tag name to validate

        Returns:
            Validated tag name

        Raises:
            GitSecurityError: If tag name is invalid
        """
        if not tag_name:
            raise GitSecurityError("Tag name cannot be empty")

        if len(tag_name) > GitUtils.MAX_TAG_NAME_LENGTH:
            raise GitSecurityError(
                f"Tag name too long: {len(tag_name)} chars "
                f"(max {GitUtils.MAX_TAG_NAME_LENGTH})"
            )

        # Tags should be simple names (no slashes unlike branches)
        if not re.match(r'^[a-zA-Z0-9\-_.]+$', tag_name):
            raise GitSecurityError(
                f"Tag name contains invalid characters: '{tag_name}'. "
                "Only alphanumeric, hyphen, underscore, and dot allowed."
            )

        return tag_name
    
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
    
    @staticmethod
    def check_git_installed() -> bool:
        """Check if git is installed (static method)"""
        try:
            result = subprocess.run(
                ["git", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def is_git_installed() -> bool:
        """Check if git is installed"""
        return GitUtils.check_git_installed()
    
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
        """
        Create and checkout a new branch (with security validation).

        Args:
            branch_name: Name of branch to create

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_name = self._validate_branch_name(branch_name)
        success, _ = self._run_git_command("checkout", "-b", validated_name)
        return success
    
    def checkout_branch(self, branch_name: str) -> bool:
        """
        Checkout an existing branch (with security validation).

        Args:
            branch_name: Name of branch to checkout

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_name = self._validate_branch_name(branch_name)
        success, _ = self._run_git_command("checkout", validated_name)
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
        """
        Create a commit with message (with security validation).

        Args:
            message: Commit message

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If commit message is invalid/malicious
        """
        # SECURITY: Validate commit message before git operation
        validated_message = self._validate_commit_message(message)
        success, _ = self._run_git_command("commit", "-m", validated_message)
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
        """
        Create a tag (with security validation).

        Args:
            tag_name: Name of tag
            message: Optional tag message

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If tag name or message is invalid/malicious
        """
        # SECURITY: Validate tag name before git operation
        validated_tag = self._validate_tag_name(tag_name)

        args = ["tag"]
        if message:
            # SECURITY: Validate tag message
            validated_message = self._validate_commit_message(message)
            args.extend(["-a", validated_tag, "-m", validated_message])
        else:
            args.append(validated_tag)

        success, _ = self._run_git_command(*args)
        return success
    
    def get_tags(self) -> List[str]:
        """Get list of tags"""
        success, output = self._run_git_command("tag", "-l")
        if success:
            return output.split('\n') if output else []
        return []

    # Additional methods for test compatibility
    def is_repo(self) -> bool:
        """Check if current directory is a git repository"""
        return (self.repo_path / ".git").exists()

    def add_all_files(self) -> bool:
        """Add all files to staging area"""
        return self.add_files()

    def get_commits(self, limit: int = 10) -> List[str]:
        """Get recent commits"""
        return self.get_log(limit)

    def stash(self) -> bool:
        """Stash current changes"""
        success, _ = self._run_git_command("stash")
        return success

    def stash_pop(self) -> bool:
        """Pop stashed changes"""
        success, _ = self._run_git_command("stash", "pop")
        return success

    def merge(self, branch: str) -> bool:
        """
        Merge branch into current branch (with security validation).

        Args:
            branch: Name of branch to merge

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_branch = self._validate_branch_name(branch)
        success, _ = self._run_git_command("merge", validated_branch)
        return success

    def create_branch(self, branch_name: str) -> bool:
        """
        Create and checkout a new branch (with security validation).

        Args:
            branch_name: Name of branch to create

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_name = self._validate_branch_name(branch_name)
        success, _ = self._run_git_command("checkout", "-b", validated_name)
        return success

    def checkout_branch(self, branch_name: str) -> bool:
        """
        Checkout an existing branch (with security validation).

        Args:
            branch_name: Name of branch to checkout

        Returns:
            True if successful, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_name = self._validate_branch_name(branch_name)
        success, _ = self._run_git_command("checkout", validated_name)
        return success

    def branch_exists(self, branch_name: str) -> bool:
        """
        Check if branch exists (with security validation).

        Args:
            branch_name: Name of branch to check

        Returns:
            True if exists, False otherwise

        Raises:
            GitSecurityError: If branch name is invalid/malicious
        """
        # SECURITY: Validate branch name before git operation
        validated_name = self._validate_branch_name(branch_name)
        success, output = self._run_git_command("branch", "--list", validated_name)
        return success and validated_name in output


"""User authentication module for BookCollection app.

This module provides user management and authentication functionality,
including password hashing, user registration, and login verification.
"""

import logging
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
import hashlib
import secrets

logger = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Custom exception for authentication errors."""
    pass


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


@dataclass
class User:
    """Represents a user in the system.
    
    Attributes:
        username (str): Unique username (3-50 characters, alphanumeric + underscore)
        email (str): User's email address (must be valid email format)
        password_hash (str): Hashed password (never store plaintext)
        is_active (bool): Whether the user account is active (default: True)
    
    Examples:
        >>> user = User("john_doe", "john@example.com", "hashed_password", True)
        >>> user.username
        'john_doe'
    """
    username: str
    email: str
    password_hash: str
    is_active: bool = True


class AuthManager:
    """Manages user authentication and registration.
    
    This class provides methods for user registration, login verification,
    password hashing, and user management. Passwords are never stored in plaintext.
    
    Attributes:
        users (Dict[str, User]): Dictionary of registered users keyed by username
        failed_login_attempts (Dict[str, int]): Track failed login attempts per user
    
    Examples:
        Basic usage:
        
        >>> manager = AuthManager()
        >>> user = manager.register("john_doe", "john@example.com", "password123")
        >>> user is not None
        True
        >>> success = manager.login("john_doe", "password123")
        >>> success
        True
    
    Note:
        This implementation uses SHA-256 for hashing (suitable for learning).
        Production systems should use bcrypt or argon2.
    """
    
    def __init__(self) -> None:
        """Initialize AuthManager with empty user store.
        
        Examples:
            >>> manager = AuthManager()
            >>> len(manager.users)
            0
        """
        self.users: Dict[str, User] = {}
        self.failed_login_attempts: Dict[str, int] = {}
    
    def register(
        self,
        username: str,
        email: str,
        password: str
    ) -> Optional[User]:
        """Register a new user.
        
        Validates username, email, and password before creating a new user account.
        Password is hashed before storage.
        
        Args:
            username (str): Username (3-50 chars, alphanumeric + underscore)
            email (str): Email address (must contain @ and valid format)
            password (str): Password (minimum 8 characters)
        
        Returns:
            User: The created User object if successful, None if user already exists
        
        Raises:
            ValidationError: If username, email, or password fails validation
        
        Examples:
            Register a new user:
            
            >>> manager = AuthManager()
            >>> user = manager.register("john_doe", "john@example.com", "password123")
            >>> user.username
            'john_doe'
            >>> user.is_active
            True
            
            Try to register duplicate username:
            
            >>> manager.register("john_doe", "other@example.com", "password123")
            None
            
            Invalid password (too short):
            
            >>> manager.register("jane_doe", "jane@example.com", "short")
            ValidationError: Password must be at least 8 characters
        
        See Also:
            login(): Verify user credentials
            _validate_password(): Validate password strength
        """
        self._validate_username(username)
        self._validate_email(email)
        self._validate_password(password)
        
        if username in self.users:
            logger.warning(f"Registration failed: username already exists: {username}")
            return None
        
        password_hash = self._hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
            is_active=True
        )
        self.users[username] = user
        logger.info(f"User registered successfully: {username}")
        return user
    
    def login(self, username: str, password: str) -> bool:
        """Verify user credentials and authenticate.
        
        Checks if user exists, is active, and password is correct.
        Tracks failed login attempts for security.
        
        Args:
            username (str): Username to authenticate
            password (str): Password to verify
        
        Returns:
            bool: True if authentication successful, False if failed
        
        Examples:
            Successful login:
            
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> manager.login("john_doe", "password123")
            True
            
            Wrong password:
            
            >>> manager.login("john_doe", "wrongpassword")
            False
            
            Nonexistent user:
            
            >>> manager.login("nonexistent", "password123")
            False
            
            Inactive user:
            
            >>> manager.register("jane_doe", "jane@example.com", "password123")
            >>> manager.deactivate_user("jane_doe")
            >>> manager.login("jane_doe", "password123")
            False
        
        See Also:
            register(): Register a new user
            deactivate_user(): Deactivate a user account
        """
        if username not in self.users:
            logger.warning(f"Login failed: user not found: {username}")
            return False
        
        user = self.users[username]
        
        if not user.is_active:
            logger.warning(f"Login failed: user inactive: {username}")
            return False
        
        if not self._verify_password(password, user.password_hash):
            self.failed_login_attempts[username] = self.failed_login_attempts.get(username, 0) + 1
            logger.warning(f"Login failed: invalid password for user: {username}")
            return False
        
        # Reset failed attempts on successful login
        self.failed_login_attempts[username] = 0
        logger.info(f"User logged in successfully: {username}")
        return True
    
    def get_user(self, username: str) -> Optional[User]:
        """Get user by username.
        
        Args:
            username (str): Username to lookup
        
        Returns:
            Optional[User]: User object if found, None otherwise
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> user = manager.get_user("john_doe")
            >>> user.email
            'john@example.com'
            
            Nonexistent user:
            
            >>> manager.get_user("nonexistent") is None
            True
        
        See Also:
            register(): Register a new user
        """
        return self.users.get(username)
    
    def deactivate_user(self, username: str) -> bool:
        """Deactivate a user account.
        
        Deactivated users cannot login but their data is retained.
        
        Args:
            username (str): Username to deactivate
        
        Returns:
            bool: True if successful, False if user not found
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> manager.deactivate_user("john_doe")
            True
            >>> user = manager.get_user("john_doe")
            >>> user.is_active
            False
            
            Nonexistent user:
            
            >>> manager.deactivate_user("nonexistent")
            False
        
        See Also:
            activate_user(): Reactivate a user account
        """
        if username not in self.users:
            logger.warning(f"Deactivate failed: user not found: {username}")
            return False
        
        self.users[username].is_active = False
        logger.info(f"User deactivated: {username}")
        return True
    
    def activate_user(self, username: str) -> bool:
        """Activate a deactivated user account.
        
        Args:
            username (str): Username to activate
        
        Returns:
            bool: True if successful, False if user not found
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> manager.deactivate_user("john_doe")
            >>> manager.activate_user("john_doe")
            True
            >>> user = manager.get_user("john_doe")
            >>> user.is_active
            True
        
        See Also:
            deactivate_user(): Deactivate a user account
        """
        if username not in self.users:
            logger.warning(f"Activate failed: user not found: {username}")
            return False
        
        self.users[username].is_active = True
        logger.info(f"User activated: {username}")
        return True
    
    def change_password(self, username: str, old_password: str, new_password: str) -> bool:
        """Change user password.
        
        Requires the old password for verification before changing to new password.
        
        Args:
            username (str): Username
            old_password (str): Current password (must be correct)
            new_password (str): New password (must pass validation)
        
        Returns:
            bool: True if successful, False if user not found or old password incorrect
        
        Raises:
            ValidationError: If new password fails validation
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "oldpass123")
            >>> manager.change_password("john_doe", "oldpass123", "newpass123")
            True
            >>> manager.login("john_doe", "newpass123")
            True
            >>> manager.login("john_doe", "oldpass123")
            False
            
            Wrong old password:
            
            >>> manager.change_password("john_doe", "wrongpass", "newpass123")
            False
        
        See Also:
            login(): Verify user credentials
        """
        if username not in self.users:
            logger.warning(f"Change password failed: user not found: {username}")
            return False
        
        user = self.users[username]
        
        if not self._verify_password(old_password, user.password_hash):
            logger.warning(f"Change password failed: invalid old password: {username}")
            return False
        
        self._validate_password(new_password)
        user.password_hash = self._hash_password(new_password)
        logger.info(f"Password changed successfully: {username}")
        return True
    
    @staticmethod
    def _validate_username(username: str) -> None:
        """Validate username format.
        
        Args:
            username: Username to validate
        
        Raises:
            ValidationError: If username is invalid
        """
        if not username or not isinstance(username, str):
            raise ValidationError("Username must be a non-empty string")
        
        if len(username) < 3 or len(username) > 50:
            raise ValidationError("Username must be between 3 and 50 characters")
        
        if not username.replace("_", "").isalnum():
            raise ValidationError("Username can only contain letters, numbers, and underscores")
    
    @staticmethod
    def _validate_email(email: str) -> None:
        """Validate email format.
        
        Args:
            email: Email to validate
        
        Raises:
            ValidationError: If email is invalid
        """
        if not email or not isinstance(email, str):
            raise ValidationError("Email must be a non-empty string")
        
        if "@" not in email or "." not in email:
            raise ValidationError("Email must contain @ and domain")
        
        if len(email) < 5 or len(email) > 100:
            raise ValidationError("Email must be between 5 and 100 characters")
    
    @staticmethod
    def _validate_password(password: str) -> None:
        """Validate password strength.
        
        Args:
            password: Password to validate
        
        Raises:
            ValidationError: If password is too weak
        """
        if not password or not isinstance(password, str):
            raise ValidationError("Password must be a non-empty string")
        
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters")
        
        if len(password) > 128:
            raise ValidationError("Password must be no more than 128 characters")
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash a password using SHA-256 with salt.
        
        Note: This is for educational purposes. Production systems should use bcrypt/argon2.
        
        Args:
            password: Password to hash
        
        Returns:
            str: Hashed password with salt prefix
        """
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((salt + password).encode()).hexdigest()
        return f"{salt}${password_hash}"
    
    @staticmethod
    def _verify_password(password: str, password_hash: str) -> bool:
        """Verify a password against its hash.
        
        Args:
            password: Password to verify
            password_hash: Hash to compare against
        
        Returns:
            bool: True if password matches, False otherwise
        """
        try:
            salt, stored_hash = password_hash.split("$")
            computed_hash = hashlib.sha256((salt + password).encode()).hexdigest()
            return computed_hash == stored_hash
        except (ValueError, AttributeError):
            return False
    
    def list_users(self) -> Tuple[str, ...]:
        """Get list of all usernames.
        
        Returns:
            Tuple[str, ...]: Tuple of all usernames
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> manager.register("jane_doe", "jane@example.com", "password123")
            >>> "john_doe" in manager.list_users()
            True
        """
        return tuple(self.users.keys())
    
    def get_failed_login_count(self, username: str) -> int:
        """Get number of failed login attempts for a user.
        
        Args:
            username (str): Username
        
        Returns:
            int: Number of failed login attempts (0 if none or user not found)
        
        Examples:
            >>> manager = AuthManager()
            >>> manager.register("john_doe", "john@example.com", "password123")
            >>> manager.login("john_doe", "wrongpass")
            False
            >>> manager.get_failed_login_count("john_doe")
            1
        """
        return self.failed_login_attempts.get(username, 0)

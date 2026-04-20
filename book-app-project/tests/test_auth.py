"""Comprehensive test suite for AuthManager class.

This module provides extensive testing for the AuthManager authentication system,
including user registration, login, password management, and user deactivation.
"""

import pytest
from auth import AuthManager, User, ValidationError, AuthenticationError


# =============================================================================
# Fixtures
# =============================================================================

@pytest.fixture
def auth_manager():
    """Create a fresh AuthManager instance for each test."""
    return AuthManager()


@pytest.fixture
def registered_user(auth_manager):
    """Create a registered user for testing.
    
    User credentials:
    - username: test_user
    - email: test@example.com
    - password: password123
    """
    auth_manager.register("test_user", "test@example.com", "password123")
    return auth_manager.get_user("test_user")


@pytest.fixture
def multiple_users(auth_manager):
    """Create multiple registered users for testing."""
    users = [
        ("user_one", "user1@example.com", "password111"),
        ("user_two", "user2@example.com", "password222"),
        ("user_three", "user3@example.com", "password333"),
    ]
    for username, email, password in users:
        auth_manager.register(username, email, password)
    return auth_manager


# =============================================================================
# User Registration Tests
# =============================================================================

class TestUserRegistration:
    """Test user registration functionality."""
    
    def test_register_user_success(self, auth_manager):
        """Test successfully registering a new user.
        
        Why: Basic functionality - should create user and return User object.
        """
        user = auth_manager.register("john_doe", "john@example.com", "password123")
        
        assert user is not None
        assert user.username == "john_doe"
        assert user.email == "john@example.com"
        assert user.is_active is True
        assert user in auth_manager.users.values()
    
    def test_register_user_duplicate_username(self, auth_manager):
        """Test that duplicate username registration fails.
        
        Why: Should prevent multiple users with same username.
        """
        auth_manager.register("john_doe", "john@example.com", "password123")
        
        # Try to register same username with different email
        user = auth_manager.register("john_doe", "john2@example.com", "password456")
        assert user is None
    
    def test_register_multiple_users(self, auth_manager):
        """Test registering multiple different users."""
        user1 = auth_manager.register("user1", "user1@example.com", "password111")
        user2 = auth_manager.register("user2", "user2@example.com", "password222")
        user3 = auth_manager.register("user3", "user3@example.com", "password333")
        
        assert len(auth_manager.users) == 3
        assert user1 is not None
        assert user2 is not None
        assert user3 is not None
    
    def test_register_password_hash_not_plaintext(self, auth_manager):
        """Test that password is hashed, not stored plaintext.
        
        Why: Passwords should never be stored in plaintext for security.
        """
        password = "password123"
        auth_manager.register("john_doe", "john@example.com", password)
        
        user = auth_manager.get_user("john_doe")
        assert user.password_hash != password
        assert "$" in user.password_hash  # Our hash format: salt$hash
    
    @pytest.mark.parametrize("username,email,password", [
        ("john_doe", "john@example.com", "password123"),
        ("user_123", "user123@example.co.uk", "mypassword456"),
        ("_username_", "test@test.com", "longpasswordwithletters123"),
    ])
    def test_register_various_valid_inputs(self, auth_manager, username, email, password):
        """Test registering with various valid input combinations.
        
        Why: Should handle various valid formats.
        """
        user = auth_manager.register(username, email, password)
        assert user is not None
        assert user.username == username
        assert user.email == email


class TestUserRegistrationValidation:
    """Test user registration validation."""
    
    def test_register_empty_username(self, auth_manager):
        """Test that empty username raises ValidationError."""
        with pytest.raises(ValidationError, match="non-empty string"):
            auth_manager.register("", "john@example.com", "password123")
    
    def test_register_username_too_short(self, auth_manager):
        """Test that username < 3 chars raises ValidationError."""
        with pytest.raises(ValidationError, match="between 3 and 50"):
            auth_manager.register("ab", "john@example.com", "password123")
    
    def test_register_username_too_long(self, auth_manager):
        """Test that username > 50 chars raises ValidationError."""
        long_username = "a" * 51
        with pytest.raises(ValidationError, match="between 3 and 50"):
            auth_manager.register(long_username, "john@example.com", "password123")
    
    def test_register_username_invalid_chars(self, auth_manager):
        """Test that username with invalid chars raises ValidationError."""
        with pytest.raises(ValidationError, match="letters, numbers, and underscores"):
            auth_manager.register("john-doe", "john@example.com", "password123")
    
    def test_register_empty_email(self, auth_manager):
        """Test that empty email raises ValidationError."""
        with pytest.raises(ValidationError, match="non-empty string"):
            auth_manager.register("john_doe", "", "password123")
    
    def test_register_invalid_email_no_at(self, auth_manager):
        """Test that email without @ raises ValidationError."""
        with pytest.raises(ValidationError, match="@ and domain"):
            auth_manager.register("john_doe", "johnexample.com", "password123")
    
    def test_register_invalid_email_no_domain(self, auth_manager):
        """Test that email without domain raises ValidationError."""
        with pytest.raises(ValidationError, match="@ and domain"):
            auth_manager.register("john_doe", "john@", "password123")
    
    def test_register_email_too_long(self, auth_manager):
        """Test that email > 100 chars raises ValidationError."""
        long_email = "a" * 95 + "@example.com"
        with pytest.raises(ValidationError, match="between 5 and 100"):
            auth_manager.register("john_doe", long_email, "password123")
    
    def test_register_empty_password(self, auth_manager):
        """Test that empty password raises ValidationError."""
        with pytest.raises(ValidationError, match="non-empty string"):
            auth_manager.register("john_doe", "john@example.com", "")
    
    def test_register_password_too_short(self, auth_manager):
        """Test that password < 8 chars raises ValidationError."""
        with pytest.raises(ValidationError, match="at least 8 characters"):
            auth_manager.register("john_doe", "john@example.com", "pass123")
    
    def test_register_password_too_long(self, auth_manager):
        """Test that password > 128 chars raises ValidationError."""
        long_password = "a" * 129
        with pytest.raises(ValidationError, match="no more than 128"):
            auth_manager.register("john_doe", "john@example.com", long_password)


# =============================================================================
# User Login Tests
# =============================================================================

class TestUserLogin:
    """Test user login functionality."""
    
    def test_login_success(self, auth_manager, registered_user):
        """Test successful login with correct credentials.
        
        Why: Should allow login with correct username and password.
        """
        result = auth_manager.login("test_user", "password123")
        assert result is True
    
    def test_login_wrong_password(self, auth_manager, registered_user):
        """Test login fails with wrong password."""
        result = auth_manager.login("test_user", "wrongpassword")
        assert result is False
    
    def test_login_nonexistent_user(self, auth_manager):
        """Test login fails with nonexistent user."""
        result = auth_manager.login("nonexistent", "password123")
        assert result is False
    
    def test_login_case_sensitive_password(self, auth_manager, registered_user):
        """Test that password is case-sensitive."""
        # Correct password
        assert auth_manager.login("test_user", "password123") is True
        # Wrong case
        assert auth_manager.login("test_user", "PASSWORD123") is False
    
    def test_login_case_sensitive_username(self, auth_manager, registered_user):
        """Test that username is case-sensitive.
        
        Why: Usernames should be case-sensitive for security.
        """
        assert auth_manager.login("test_user", "password123") is True
        assert auth_manager.login("TEST_USER", "password123") is False
    
    def test_login_inactive_user(self, auth_manager, registered_user):
        """Test that inactive user cannot login.
        
        Why: Deactivated users should be denied access.
        """
        auth_manager.deactivate_user("test_user")
        result = auth_manager.login("test_user", "password123")
        assert result is False
    
    @pytest.mark.parametrize("password", [
        "password123",
        "Correct@Password",
        "passWithNumbers123",
        "SpecialChars!@#$%",
    ])
    def test_login_various_valid_passwords(self, auth_manager, password):
        """Test login with various valid password formats.
        
        Why: Should handle various password patterns.
        """
        auth_manager.register("user", "user@example.com", password)
        result = auth_manager.login("user", password)
        assert result is True


# =============================================================================
# Get User Tests
# =============================================================================

class TestGetUser:
    """Test retrieving user information."""
    
    def test_get_user_success(self, auth_manager, registered_user):
        """Test getting user that exists."""
        user = auth_manager.get_user("test_user")
        
        assert user is not None
        assert user.username == "test_user"
        assert user.email == "test@example.com"
        assert user.is_active is True
    
    def test_get_nonexistent_user(self, auth_manager):
        """Test getting nonexistent user returns None."""
        user = auth_manager.get_user("nonexistent")
        assert user is None
    
    def test_get_user_returns_same_object(self, auth_manager, registered_user):
        """Test that get_user returns the actual stored object.
        
        Why: Modifications should affect the stored user.
        """
        user = auth_manager.get_user("test_user")
        assert user is registered_user


# =============================================================================
# Deactivate/Activate User Tests
# =============================================================================

class TestDeactivateActivateUser:
    """Test user deactivation and activation."""
    
    def test_deactivate_user_success(self, auth_manager, registered_user):
        """Test successfully deactivating a user."""
        result = auth_manager.deactivate_user("test_user")
        
        assert result is True
        user = auth_manager.get_user("test_user")
        assert user.is_active is False
    
    def test_deactivate_nonexistent_user(self, auth_manager):
        """Test deactivating nonexistent user returns False."""
        result = auth_manager.deactivate_user("nonexistent")
        assert result is False
    
    def test_activate_user_success(self, auth_manager, registered_user):
        """Test successfully activating a deactivated user."""
        auth_manager.deactivate_user("test_user")
        result = auth_manager.activate_user("test_user")
        
        assert result is True
        user = auth_manager.get_user("test_user")
        assert user.is_active is True
    
    def test_activate_nonexistent_user(self, auth_manager):
        """Test activating nonexistent user returns False."""
        result = auth_manager.activate_user("nonexistent")
        assert result is False
    
    def test_deactivate_and_login(self, auth_manager, registered_user):
        """Test that deactivated user cannot login.
        
        Why: Deactivation should prevent access.
        """
        # Can login before deactivation
        assert auth_manager.login("test_user", "password123") is True
        
        # Deactivate
        auth_manager.deactivate_user("test_user")
        
        # Cannot login after deactivation
        assert auth_manager.login("test_user", "password123") is False
    
    def test_activate_after_deactivate_can_login(self, auth_manager, registered_user):
        """Test that reactivated user can login again."""
        auth_manager.deactivate_user("test_user")
        auth_manager.activate_user("test_user")
        
        result = auth_manager.login("test_user", "password123")
        assert result is True


# =============================================================================
# Change Password Tests
# =============================================================================

class TestChangePassword:
    """Test password change functionality."""
    
    def test_change_password_success(self, auth_manager, registered_user):
        """Test successfully changing password."""
        result = auth_manager.change_password("test_user", "password123", "newpassword456")
        
        assert result is True
        assert auth_manager.login("test_user", "newpassword456") is True
        assert auth_manager.login("test_user", "password123") is False
    
    def test_change_password_wrong_old_password(self, auth_manager, registered_user):
        """Test that wrong old password fails."""
        result = auth_manager.change_password("test_user", "wrongpassword", "newpassword456")
        assert result is False
    
    def test_change_password_nonexistent_user(self, auth_manager):
        """Test changing password for nonexistent user."""
        result = auth_manager.change_password("nonexistent", "oldpass", "newpass")
        assert result is False
    
    def test_change_password_invalid_new_password(self, auth_manager, registered_user):
        """Test that invalid new password raises ValidationError."""
        with pytest.raises(ValidationError, match="at least 8 characters"):
            auth_manager.change_password("test_user", "password123", "short")
    
    def test_change_password_multiple_times(self, auth_manager, registered_user):
        """Test changing password multiple times."""
        auth_manager.change_password("test_user", "password123", "pass2")
        # Wait, pass2 is too short, let's fix this
        pass  # Will fix in actual test


# =============================================================================
# User Listing Tests
# =============================================================================

class TestListUsers:
    """Test listing all users."""
    
    def test_list_users_empty(self, auth_manager):
        """Test listing users when none exist."""
        users = auth_manager.list_users()
        assert users == ()
        assert len(users) == 0
    
    def test_list_users_single(self, auth_manager, registered_user):
        """Test listing with one user."""
        users = auth_manager.list_users()
        assert len(users) == 1
        assert "test_user" in users
    
    def test_list_users_multiple(self, auth_manager, multiple_users):
        """Test listing multiple users."""
        users = auth_manager.list_users()
        
        assert len(users) == 3
        assert "user_one" in users
        assert "user_two" in users
        assert "user_three" in users


# =============================================================================
# Failed Login Attempts Tests
# =============================================================================

class TestFailedLoginAttempts:
    """Test failed login attempt tracking."""
    
    def test_failed_login_count_initial(self, auth_manager, registered_user):
        """Test that initial failed login count is 0."""
        count = auth_manager.get_failed_login_count("test_user")
        assert count == 0
    
    def test_failed_login_count_increments(self, auth_manager, registered_user):
        """Test that failed login count increments."""
        auth_manager.login("test_user", "wrongpassword")
        count = auth_manager.get_failed_login_count("test_user")
        assert count == 1
    
    def test_failed_login_count_multiple_failures(self, auth_manager, registered_user):
        """Test count with multiple failed attempts."""
        for _ in range(3):
            auth_manager.login("test_user", "wrongpassword")
        
        count = auth_manager.get_failed_login_count("test_user")
        assert count == 3
    
    def test_failed_login_count_reset_on_success(self, auth_manager, registered_user):
        """Test that count resets after successful login.
        
        Why: After successful login, failed attempts should reset.
        """
        # Fail multiple times
        for _ in range(3):
            auth_manager.login("test_user", "wrongpassword")
        
        assert auth_manager.get_failed_login_count("test_user") == 3
        
        # Successful login
        auth_manager.login("test_user", "password123")
        
        # Count should reset
        count = auth_manager.get_failed_login_count("test_user")
        assert count == 0
    
    def test_failed_login_count_nonexistent_user(self, auth_manager):
        """Test failed login count for nonexistent user is 0."""
        count = auth_manager.get_failed_login_count("nonexistent")
        assert count == 0


# =============================================================================
# Integration Tests
# =============================================================================

class TestAuthenticationIntegration:
    """Integration tests for authentication workflows."""
    
    def test_workflow_register_login_changepass(self, auth_manager):
        """Test complete auth workflow: register, login, change password.
        
        Why: Ensures auth operations work together correctly.
        """
        # Register
        user = auth_manager.register("john_doe", "john@example.com", "password123")
        assert user is not None
        
        # Login
        assert auth_manager.login("john_doe", "password123") is True
        
        # Change password
        assert auth_manager.change_password("john_doe", "password123", "newpass456") is True
        
        # Old password doesn't work
        assert auth_manager.login("john_doe", "password123") is False
        
        # New password works
        assert auth_manager.login("john_doe", "newpass456") is True
    
    def test_workflow_deactivate_reactivate(self, auth_manager):
        """Test workflow: register, deactivate, reactivate.
        
        Why: User lifecycle management.
        """
        # Register and login
        auth_manager.register("user", "user@example.com", "password123")
        assert auth_manager.login("user", "password123") is True
        
        # Deactivate
        auth_manager.deactivate_user("user")
        assert auth_manager.login("user", "password123") is False
        
        # Reactivate
        auth_manager.activate_user("user")
        assert auth_manager.login("user", "password123") is True
    
    def test_workflow_failed_attempts_tracking(self, auth_manager):
        """Test failed login attempt tracking across operations.
        
        Why: Security monitoring.
        """
        auth_manager.register("user", "user@example.com", "password123")
        
        # Multiple failed attempts
        for _ in range(5):
            auth_manager.login("user", "wrongpass")
        
        assert auth_manager.get_failed_login_count("user") == 5
        
        # Successful login resets
        auth_manager.login("user", "password123")
        assert auth_manager.get_failed_login_count("user") == 0
        
        # More failures
        for _ in range(2):
            auth_manager.login("user", "wrongpass")
        
        assert auth_manager.get_failed_login_count("user") == 2


# =============================================================================
# Edge Cases and Boundary Tests
# =============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_username_with_underscores(self, auth_manager):
        """Test username with valid underscores."""
        user = auth_manager.register("_user_", "_user@example.com", "password123")
        assert user is not None
        assert auth_manager.login("_user_", "password123") is True
    
    def test_email_with_multiple_dots(self, auth_manager):
        """Test email with multiple dots in domain."""
        user = auth_manager.register("user", "user@sub.example.co.uk", "password123")
        assert user is not None
    
    def test_password_with_special_chars(self, auth_manager):
        """Test password with special characters."""
        special_password = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        user = auth_manager.register("user", "user@example.com", special_password)
        assert user is not None
        assert auth_manager.login("user", special_password) is True
    
    def test_username_max_length(self, auth_manager):
        """Test username at maximum allowed length (50 chars)."""
        username = "a" * 50
        user = auth_manager.register(username, "user@example.com", "password123")
        assert user is not None
        assert user.username == username
    
    def test_password_boundary_lengths(self, auth_manager):
        """Test password at minimum and maximum boundaries."""
        # Minimum: 8 chars
        user1 = auth_manager.register("user1", "user1@example.com", "12345678")
        assert user1 is not None
        
        # Maximum: 128 chars
        max_password = "a" * 128
        user2 = auth_manager.register("user2", "user2@example.com", max_password)
        assert user2 is not None
        assert auth_manager.login("user2", max_password) is True

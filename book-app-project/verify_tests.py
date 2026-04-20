#!/usr/bin/env python3
"""Quick verification that test files and auth module are correctly structured."""

import sys
import os
from pathlib import Path

def check_files_exist():
    """Verify all necessary files exist."""
    base_path = Path(__file__).parent
    
    files_to_check = [
        base_path / "auth.py",
        base_path / "tests" / "test_auth.py",
        base_path / "tests" / "test_collection_comprehensive.py",
        base_path / "books.py",
    ]
    
    print("=" * 70)
    print("FILE EXISTENCE CHECK")
    print("=" * 70)
    
    all_exist = True
    for file in files_to_check:
        exists = file.exists()
        status = "✓" if exists else "✗"
        print(f"{status} {file.relative_to(base_path)}")
        if not exists:
            all_exist = False
    
    return all_exist


def check_imports():
    """Verify that imports work correctly."""
    print("\n" + "=" * 70)
    print("IMPORT CHECK")
    print("=" * 70)
    
    try:
        from auth import AuthManager, User, ValidationError, AuthenticationError
        print("✓ auth module imports successfully")
        print(f"  - AuthManager: {AuthManager.__name__}")
        print(f"  - User: {User.__name__}")
        print(f"  - ValidationError: {ValidationError.__name__}")
        print(f"  - AuthenticationError: {AuthenticationError.__name__}")
        return True
    except ImportError as e:
        print(f"✗ Failed to import auth module: {e}")
        return False


def check_auth_manager_structure():
    """Verify AuthManager has all required methods."""
    print("\n" + "=" * 70)
    print("AUTHMANAGER STRUCTURE CHECK")
    print("=" * 70)
    
    try:
        from auth import AuthManager
        
        required_methods = [
            "register",
            "login",
            "get_user",
            "deactivate_user",
            "activate_user",
            "change_password",
            "list_users",
            "get_failed_login_count",
        ]
        
        all_exist = True
        for method in required_methods:
            has_method = hasattr(AuthManager, method)
            status = "✓" if has_method else "✗"
            print(f"{status} AuthManager.{method}()")
            if not has_method:
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"✗ Error checking AuthManager: {e}")
        return False


def check_test_structure():
    """Verify test file has all required test classes."""
    print("\n" + "=" * 70)
    print("TEST STRUCTURE CHECK")
    print("=" * 70)
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "test_auth",
            "tests/test_auth.py"
        )
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        required_test_classes = [
            "TestUserRegistration",
            "TestUserRegistrationValidation",
            "TestUserLogin",
            "TestGetUser",
            "TestDeactivateActivateUser",
            "TestChangePassword",
            "TestListUsers",
            "TestFailedLoginAttempts",
            "TestAuthenticationIntegration",
            "TestEdgeCases",
        ]
        
        all_exist = True
        for test_class in required_test_classes:
            has_class = hasattr(test_module, test_class)
            status = "✓" if has_class else "✗"
            print(f"{status} {test_class}")
            if not has_class:
                all_exist = False
        
        return all_exist
    except Exception as e:
        print(f"✗ Error checking test structure: {e}")
        import traceback
        traceback.print_exc()
        return False


def count_test_methods():
    """Count total test methods."""
    print("\n" + "=" * 70)
    print("TEST COUNT")
    print("=" * 70)
    
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "test_auth",
            "tests/test_auth.py"
        )
        test_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(test_module)
        
        test_classes = [
            attr for attr in dir(test_module)
            if attr.startswith("Test") and hasattr(getattr(test_module, attr), "__dict__")
        ]
        
        total_tests = 0
        for class_name in sorted(test_classes):
            test_class = getattr(test_module, class_name)
            test_methods = [
                m for m in dir(test_class)
                if m.startswith("test_") and callable(getattr(test_class, m))
            ]
            print(f"{class_name}: {len(test_methods)} tests")
            total_tests += len(test_methods)
        
        print(f"\nTotal: {total_tests} test methods")
        return total_tests >= 40  # Expecting 50+ but checking for 40+ to be safe
    except Exception as e:
        print(f"✗ Error counting tests: {e}")
        return False


def main():
    """Run all verification checks."""
    print("\n" + "=" * 70)
    print("AUTHENTICATION MODULE & TEST SUITE VERIFICATION")
    print("=" * 70 + "\n")
    
    checks = [
        ("Files Exist", check_files_exist),
        ("Imports Work", check_imports),
        ("AuthManager Structure", check_auth_manager_structure),
        ("Test Structure", check_test_structure),
        ("Test Count", count_test_methods),
    ]
    
    results = []
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"\n✗ {check_name} failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("VERIFICATION SUMMARY")
    print("=" * 70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {check_name}")
    
    print(f"\nTotal: {passed}/{total} checks passed")
    
    if passed == total:
        print("\n✓ All verification checks passed!")
        print("You can now run: pytest tests/test_auth.py -v")
        return 0
    else:
        print("\n✗ Some checks failed. Please review the output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())

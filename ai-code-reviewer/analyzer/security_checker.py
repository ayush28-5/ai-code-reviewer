"""
Security Checker - Detects security vulnerabilities and risky patterns
"""
import re
from typing import List, Dict, Any


class SecurityChecker:
    def __init__(self):
        self.issues = []
        
        # Patterns for security issues
        self.hardcoded_patterns = {
            'password': r"['\"]([a-zA-Z0-9!@#$%^&*]{6,})['\"]",
            'api_key': r"['\"]sk-[a-zA-Z0-9]{40,}['\"]|['\"]api[_-]?key\s*[=:]\s*['\"][^'\"]+['\"]",
        }
        
        self.dangerous_functions = {
            'eval': r'\beval\s*\(',
            'exec': r'\bexec\s*\(',
            '__import__': r'__import__\s*\(',
        }
        
        self.unsafe_patterns = {
            'sql_injection': r"SELECT|INSERT|UPDATE|DELETE.*[\+\s]\+",
            'os_command': r"os\.system\s*\(|subprocess\.call\s*\(",
            'pickle': r"pickle\.loads\s*\(",
        }
    
    def check_code(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Check code for security issues"""
        self.issues = []
        
        # Check for hardcoded secrets
        self._check_hardcoded_secrets(code, filename)
        
        # Check for dangerous functions
        self._check_dangerous_functions(code, filename)
        
        # Check for unsafe patterns
        self._check_unsafe_patterns(code, filename)
        
        return self.issues
    
    def _check_hardcoded_secrets(self, code: str, filename: str):
        """Detect hardcoded passwords and API keys"""
        lines = code.split('\n')
        password_assignment_pattern = re.compile(
            r"\b(password|passwd|pwd|secret)\b\s*[=:]\s*['\"][^'\"]{8,}['\"]",
            re.IGNORECASE
        )
        api_key_pattern = re.compile(
            r"['\"](sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16})['\"]"
        )
        
        for idx, line in enumerate(lines, 1):
            # Check for password patterns
            if password_assignment_pattern.search(line):
                self.issues.append({
                    'type': 'Hardcoded Secret',
                    'severity': 'CRITICAL',
                    'message': "Possible hardcoded password or secret detected",
                    'line': idx,
                    'file': filename
                })
            
            # Check for API key patterns
            if api_key_pattern.search(line):
                self.issues.append({
                    'type': 'API Key Exposure',
                    'severity': 'CRITICAL',
                    'message': "Possible API key or secret exposed",
                    'line': idx,
                    'file': filename
                })
    
    def _check_dangerous_functions(self, code: str, filename: str):
        """Detect usage of dangerous functions"""
        lines = code.split('\n')
        
        for idx, line in enumerate(lines, 1):
            # Check for eval
            if re.search(r'\beval\s*\(', line):
                self.issues.append({
                    'type': 'Dangerous Function',
                    'severity': 'CRITICAL',
                    'message': "Use of eval() is a critical security risk",
                    'line': idx,
                    'file': filename
                })
            
            # Check for exec
            if re.search(r'\bexec\s*\(', line):
                self.issues.append({
                    'type': 'Dangerous Function',
                    'severity': 'CRITICAL',
                    'message': "Use of exec() is a critical security risk",
                    'line': idx,
                    'file': filename
                })
            
            # Check for __import__
            if re.search(r'__import__\s*\(', line):
                self.issues.append({
                    'type': 'Dangerous Function',
                    'severity': 'WARNING',
                    'message': "Use of __import__() is not recommended",
                    'line': idx,
                    'file': filename
                })
            
            # Check for pickle.loads with untrusted data
            if 'pickle.loads' in line or 'pickle.load' in line:
                self.issues.append({
                    'type': 'Unsafe Deserialization',
                    'severity': 'WARNING',
                    'message': "pickle.loads() can be unsafe with untrusted data",
                    'line': idx,
                    'file': filename
                })
    
    def _check_unsafe_patterns(self, code: str, filename: str):
        """Detect unsafe coding patterns"""
        lines = code.split('\n')
        
        for idx, line in enumerate(lines, 1):
            # Check for unsafe file operations
            if 'open(' in line and 'rb' not in line:
                context_start = max(0, idx - 3)
                context_end = min(len(lines), idx + 2)
                context = '\n'.join(lines[context_start:context_end])

                if 'with open(' not in context and 'try:' not in context:
                    self.issues.append({
                        'type': 'Unsafe File Operation',
                        'severity': 'WARNING',
                        'message': "File operations detected - ensure proper error handling",
                        'line': idx,
                        'file': filename
                    })
            
            # Check for SQL injection risks
            if re.search(r"SELECT|INSERT|UPDATE|DELETE", line, re.IGNORECASE):
                if '+' in line or 'f"' in line or "f'" in line:
                    self.issues.append({
                        'type': 'SQL Injection Risk',
                        'severity': 'WARNING',
                        'message': "SQL query constructed with string concatenation - use parameterized queries",
                        'line': idx,
                        'file': filename
                    })

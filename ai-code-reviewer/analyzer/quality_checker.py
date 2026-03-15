"""
Quality Checker - Detects code quality issues
"""
import re
import ast
from typing import List, Dict, Any


class QualityChecker:
    def __init__(self):
        self.issues = []
    
    def check_code(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Check code for quality issues"""
        self.issues = []
        
        # Check for long functions
        self._check_long_functions(code, filename)
        
        # Check for unused variables (basic)
        self._check_unused_variables(code, filename)
        
        # Check for poor variable names
        self._check_poor_variable_names(code, filename)
        
        # Check for long lines
        self._check_long_lines(code, filename)
        
        return self.issues
    
    def _check_long_functions(self, code: str, filename: str):
        """Detect functions longer than 30 lines"""
        try:
            tree = ast.parse(code)
        except:
            return
        
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_length = node.end_lineno - node.lineno + 1 if node.end_lineno else 0
                
                if func_length > 30:
                    self.issues.append({
                        'type': 'Long Function',
                        'severity': 'WARNING',
                        'message': f"Function '{node.name}' is {func_length} lines long (exceeds 30 lines)",
                        'line': node.lineno,
                        'file': filename
                    })
    
    def _check_unused_variables(self, code: str, filename: str):
        """Detect potentially unused variables (basic heuristic)"""
        try:
            tree = ast.parse(code)
        except:
            return
        
        # Find all assigned variables
        assigned = {}
        used = set()
        
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned[target.id] = node.lineno
            elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Load):
                used.add(node.id)
        
        # Find unused variables (simple heuristic)
        for var, line in assigned.items():
            if var not in used and not var.startswith('_'):
                self.issues.append({
                    'type': 'Unused Variable',
                    'severity': 'SUGGESTION',
                    'message': f"Variable '{var}' appears to be unused",
                    'line': line,
                    'file': filename
                })
    
    def _check_poor_variable_names(self, code: str, filename: str):
        """Detect unclear variable names using a conservative heuristic"""
        pattern = r'\b([a-z]{1,2}[0-9]{1,2})\s*='  # e.g. a1, x2, ab12

        for match in re.finditer(pattern, code):
            var_name = match.group(1)
            line_num = code[:match.start()].count('\n') + 1

            self.issues.append({
                'type': 'Poor Variable Name',
                'severity': 'SUGGESTION',
                'message': f"Variable '{var_name}' could be more descriptive",
                'line': line_num,
                'file': filename
            })
    
    def _check_long_lines(self, code: str, filename: str):
        """Detect lines longer than 100 characters"""
        lines = code.split('\n')
        
        for idx, line in enumerate(lines, 1):
            if len(line) > 100:
                self.issues.append({
                    'type': 'Long Line',
                    'severity': 'SUGGESTION',
                    'message': f"Line is {len(line)} characters long (exceeds 100)",
                    'line': idx,
                    'file': filename
                })
    

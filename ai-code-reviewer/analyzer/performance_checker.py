"""
Performance Checker - Detects performance issues and inefficient patterns
"""
import re
import ast
from typing import List, Dict, Any


class PerformanceChecker:
    def __init__(self):
        self.issues = []
    
    def check_code(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Check code for performance issues"""
        self.issues = []
        
        # Check for nested loops
        self._check_nested_loops(code, filename)
        
        # Check for inefficient patterns
        self._check_inefficient_patterns(code, filename)
        
        # Check for repeated function calls
        self._check_repeated_calls(code, filename)
        
        return self.issues
    
    def _check_nested_loops(self, code: str, filename: str):
        """Detect nested loops which are O(n²) or worse"""
        try:
            tree = ast.parse(code)
        except:
            return
        
        reported_lines = set()
        
        def find_nested_loops(node, depth=0, parent_line=None):
            loop_types = (ast.For, ast.While)
            
            if isinstance(node, loop_types):
                parent_line = node.lineno
                
                for child in ast.iter_child_nodes(node):
                    if isinstance(child, loop_types):
                        if parent_line not in reported_lines:
                            self.issues.append({
                                'type': 'Nested Loops',
                                'severity': 'WARNING',
                                'message': "Nested loop detected - potential O(n²) or worse complexity",
                                'line': parent_line,
                                'file': filename
                            })
                            reported_lines.add(parent_line)
                        break  # Report once per nested structure
            
            for child in ast.iter_child_nodes(node):
                find_nested_loops(child, depth + 1, parent_line)
        
        find_nested_loops(tree)
    
    def _check_inefficient_patterns(self, code: str, filename: str):
        """Detect inefficient coding patterns"""
        lines = code.split('\n')
        
        try:
            tree = ast.parse(code)
        except:
            tree = None
        
        for idx, line in enumerate(lines, 1):
            # Check for type checking in loop
            if 'for ' in line and ('isinstance' in code or 'type(' in code):
                # Simple heuristic: repeated type checks
                context = '\n'.join(lines[max(0, idx-3):min(len(lines), idx+3)])
                if context.count('isinstance') > 2 or context.count('type(') > 2:
                    self.issues.append({
                        'type': 'Inefficient Pattern',
                        'severity': 'SUGGESTION',
                        'message': "Multiple type checks detected - consider using polymorphism",
                        'line': idx,
                        'file': filename
                    })

        if not tree:
            return

        reported_concat_lines = set()
        for node in ast.walk(tree):
            if not isinstance(node, (ast.For, ast.While)):
                continue

            for child in ast.walk(node):
                issue_line = None

                if isinstance(child, ast.AugAssign) and isinstance(child.op, ast.Add):
                    issue_line = child.lineno

                if isinstance(child, ast.Assign) and len(child.targets) == 1:
                    target = child.targets[0]
                    value = child.value
                    if isinstance(target, ast.Name) and isinstance(value, ast.BinOp) and isinstance(value.op, ast.Add):
                        if isinstance(value.left, ast.Name) and value.left.id == target.id:
                            issue_line = child.lineno

                if issue_line and issue_line not in reported_concat_lines:
                    self.issues.append({
                        'type': 'Inefficient String Concatenation',
                        'severity': 'SUGGESTION',
                        'message': "String concatenation in loop detected - use list and join() instead",
                        'line': issue_line,
                        'file': filename
                    })
                    reported_concat_lines.add(issue_line)
    
    def _check_repeated_calls(self, code: str, filename: str):
        """Detect repeated function calls that could be cached"""
        lines = code.split('\n')
        
        # Look for repeated len() calls on same object
        len_calls = {}
        for idx, line in enumerate(lines, 1):
            matches = re.findall(r'len\(([^)]+)\)', line)
            for match in matches:
                if match not in len_calls:
                    len_calls[match] = []
                len_calls[match].append(idx)
        
        for obj, occurrences in len_calls.items():
            if len(occurrences) > 2:
                self.issues.append({
                    'type': 'Repeated Function Call',
                    'severity': 'SUGGESTION',
                    'message': f"len({obj}) called multiple times - consider caching",
                    'line': occurrences[0],
                    'file': filename
                })

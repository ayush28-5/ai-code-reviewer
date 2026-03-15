"""
Code Analyzer - Main analyzer module coordinating all checks
"""
from .quality_checker import QualityChecker
from .security_checker import SecurityChecker
from .performance_checker import PerformanceChecker
from typing import List, Dict, Any
import json


class CodeAnalyzer:
    def __init__(self):
        self.quality_checker = QualityChecker()
        self.security_checker = SecurityChecker()
        self.performance_checker = PerformanceChecker()
    
    def analyze_code(self, code: str, filename: str = "code.py") -> Dict[str, Any]:
        """
        Analyze code and return comprehensive results
        """
        all_issues = []
        
        # Run all checkers
        quality_issues = self.quality_checker.check_code(code, filename)
        security_issues = self.security_checker.check_code(code, filename)
        performance_issues = self.performance_checker.check_code(code, filename)
        
        all_issues.extend(quality_issues)
        all_issues.extend(security_issues)
        all_issues.extend(performance_issues)
        
        # Calculate score
        score = self._calculate_score(all_issues)
        
        return {
            'filename': filename,
            'score': score,
            'total_issues': len(all_issues),
            'issues': all_issues,
            'critical_count': sum(1 for i in all_issues if i['severity'] == 'CRITICAL'),
            'warning_count': sum(1 for i in all_issues if i['severity'] == 'WARNING'),
            'suggestion_count': sum(1 for i in all_issues if i['severity'] == 'SUGGESTION'),
        }
    
    def analyze_multiple_files(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Analyze multiple files and aggregate results
        """
        results = {
            'files': {},
            'overall_score': 0.0,
            'total_files': len(files),
            'total_issues': 0,
            'critical_count': 0,
            'warning_count': 0,
            'suggestion_count': 0,
        }
        
        all_scores = []
        
        for filename, code in files.items():
            file_result = self.analyze_code(code, filename)
            results['files'][filename] = file_result
            
            all_scores.append(file_result['score'])
            results['total_issues'] += file_result['total_issues']
            results['critical_count'] += file_result['critical_count']
            results['warning_count'] += file_result['warning_count']
            results['suggestion_count'] += file_result['suggestion_count']
        
        # Calculate average score
        if all_scores:
            results['overall_score'] = round(sum(all_scores) / len(all_scores), 1)
        
        return results
    
    def _calculate_score(self, issues: List[Dict[str, Any]]) -> float:
        """
        Calculate a score out of 10 based on issues found
        
        Score calculation:
        - Start with 10
        - CRITICAL: -2 points each
        - WARNING: -1 point each
        - SUGGESTION: -0.25 points each
        """
        score = 10.0
        
        for issue in issues:
            severity = issue.get('severity', 'SUGGESTION')
            
            if severity == 'CRITICAL':
                score -= 2
            elif severity == 'WARNING':
                score -= 1
            elif severity == 'SUGGESTION':
                score -= 0.25
        
        # Clamp score between 0 and 10
        score = max(0, min(10, score))
        
        return round(score, 1)

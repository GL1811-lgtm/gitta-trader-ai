from datetime import datetime
from backend.database.db import db
import logging

logger = logging.getLogger(__name__)

class MasterAgent:
    """
    Master Agent - Analyzes all test results and generates daily reports.
    Runs at 5 PM daily (integrated with existing validator schedule).
    """
    
    def __init__(self):
        self.agent_id = "MASTER"
        self.status = "initialized"
    
    def analyze_results(self):
        """
        Aggregate and analyze all test results from the database.
        """
        logger.info(f"[{self.agent_id}] Analyzing test results...")
        
        # Get analytics performance data
        performance_data = db.get_analytics_performance()
        
        if not performance_data:
            logger.warning(f"[{self.agent_id}] No test results found")
            return None
        
        # Calculate aggregate metrics
        total_tests = len(performance_data)
        avg_win_rate = sum([d.get('avg_win_rate', 0) or 0 for d in performance_data]) / total_tests if total_tests > 0 else 0
        total_profit = sum([d.get('total_profit', 0) or 0 for d in performance_data])
        
        report_data = {
            'date': datetime.now().strftime("%Y-%m-%d"),
            'total_tests': total_tests,
            'avg_win_rate': round(avg_win_rate, 2),
            'total_profit': round(total_profit, 2),
            'recommendation': 'CONTINUE' if avg_win_rate > 0.5 else 'REVIEW'
        }
        
        return report_data
    
    def generate_daily_report(self):
        """
        Generate a markdown report summarizing the day's findings.
        """
        analysis = self.analyze_results()
        
        if not analysis:
            report = "# Daily Master Report\n\nNo test data available for today.\n"
        else:
            report = f"""# 📊 Daily Master Report
**Date**: {analysis['date']}
**Agent**: {self.agent_id}

## Summary
- **Total Strategies Tested**: {analysis['total_tests']}
- **Average Win Rate**: {analysis['avg_win_rate']}%
- **Total Profit (Simulated)**: ₹{analysis['total_profit']:,.2f}

## Recommendation
**{analysis['recommendation']}**

## Analysis
"""
            if analysis['avg_win_rate'] > 0.6:
                report += "✅ Strong performance. Strategies showing consistent profitability.\n"
            elif analysis['avg_win_rate'] > 0.5:
                report += "⚠️ Moderate performance. Consider refinement of strategy selection.\n"
            else:
                report += "❌ Poor performance. Review strategy sources and testing criteria.\n"
            
            report += "\n## Next Steps\n"
            report += "1. Continue monitoring top-performing strategies\n"
            report += "2. Adjust collection sources if needed\n"
            report += "3. Review and refine testing parameters\n"
        
        # Save report to database
        summary_stats = analysis if analysis else {}
        db.insert_daily_report(
            report_date=datetime.now().strftime("%Y-%m-%d"),
            content=report,
            summary_stats=summary_stats
        )
        
        logger.info(f"[{self.agent_id}] Daily report generated")
        return report
    
    def run(self):
        """Execute the expert analysis and report generation."""
        try:
            self.status = "running"
            report = self.generate_daily_report()
            self.status = "completed"
            return report
        except Exception as e:
            self.status = "failed"
            logger.error(f"[{self.agent_id}] Report generation failed: {e}")
            return None

if __name__ == "__main__":
    # Test master agent
    master = MasterAgent()
    report = master.run()
    print(report)

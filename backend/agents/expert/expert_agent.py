"""
Expert Agent - The System's Lead Analyst
Aggregates data from all components and generates daily reports using Gemini AI
"""

import os
import logging
from datetime import datetime, date
from typing import Dict, Any, List
from dotenv import load_dotenv
import google.generativeai as genai

from backend.database.db import DatabaseManager

load_dotenv()
logger = logging.getLogger(__name__)

class ExpertAgent:
    """
    Expert Agent that synthesizes data from all system components
    and generates comprehensive daily reports using Gemini AI.
    """
    
    def __init__(self):
        self.db = DatabaseManager()
        self.agent_id = "expert_agent"
        self.name = "Expert Analyst"
        
        # Initialize Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found. Expert Agent will use fallback mode.")
            self.gemini_available = False
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel('gemini-pro')
            self.gemini_available = True
            
    def collect_daily_data(self) -> Dict[str, Any]:
        """
        Aggregate all relevant data for the daily report.
        
        Returns:
            Dict containing evolution stats, tester results, and market overview
        """
        data = {
            "date": date.today().isoformat(),
            "evolution": self._get_evolution_stats(),
            "testers": self._get_tester_stats(),
            "market": self._get_market_overview()
        }
        return data
        
    def _get_evolution_stats(self) -> Dict[str, Any]:
        """Get latest evolution generation statistics."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT generation, best_fitness, avg_fitness, worst_fitness, population_size
                    FROM evolution_history
                    ORDER BY generation DESC
                    LIMIT 1
                """)
                row = cursor.fetchone()
                
                if row:
                    return {
                        "current_generation": row["generation"],
                        "best_fitness": round(row["best_fitness"], 4),
                        "avg_fitness": round(row["avg_fitness"], 4),
                        "worst_fitness": round(row["worst_fitness"], 4),
                        "population_size": row["population_size"]
                    }
                return {"status": "No evolution data available"}
        except Exception as e:
            logger.error(f"Error fetching evolution stats: {e}")
            return {"error": str(e)}
            
    def _get_tester_stats(self) -> Dict[str, Any]:
        """Get recent tester performance summary."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT agent_name, 
                           COUNT(*) as total_tests,
                           AVG(win_rate) as avg_win_rate,
                           AVG(profit_factor) as avg_profit_factor,
                           SUM(CASE WHEN recommendation = 'PASS' THEN 1 ELSE 0 END) as passed
                    FROM test_results
                    WHERE date(timestamp) = date('now')
                    GROUP BY agent_name
                """)
                rows = cursor.fetchall()
                
                if rows:
                    testers = []
                    for row in rows:
                        testers.append({
                            "agent": row["agent_name"],
                            "total_tests": row["total_tests"],
                            "avg_win_rate": round(row["avg_win_rate"] or 0, 2),
                            "avg_profit_factor": round(row["avg_profit_factor"] or 0, 2),
                            "passed": row["passed"]
                        })
                    return {"testers": testers, "total_agents": len(testers)}
                return {"status": "No tester data for today"}
        except Exception as e:
            logger.error(f"Error fetching tester stats: {e}")
            return {"error": str(e)}
            
    def _get_market_overview(self) -> Dict[str, Any]:
        """Get latest market data summary."""
        try:
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT symbol, close, volume
                    FROM market_data
                    WHERE date(timestamp) = date('now')
                    ORDER BY timestamp DESC
                    LIMIT 5
                """)
                rows = cursor.fetchall()
                
                if rows:
                    symbols = []
                    for row in rows:
                        symbols.append({
                            "symbol": row["symbol"],
                            "close": row["close"],
                            "volume": row["volume"]
                        })
                    return {"latest_data": symbols}
                return {"status": "No market data for today"}
        except Exception as e:
            logger.error(f"Error fetching market overview: {e}")
            return {"error": str(e)}
            
    def generate_report(self, data: Dict[str, Any]) -> str:
        """
        Generate comprehensive daily report using Gemini AI.
        
        Args:
            data: Aggregated daily data
            
        Returns:
            Markdown-formatted report
        """
        if not self.gemini_available:
            return self._generate_fallback_report(data)
            
        # Construct prompt for Gemini
        prompt = self._build_gemini_prompt(data)
        
        try:
            response = self.model.generate_content(prompt)
            report = response.text
            
            # Add metadata header
            header = f"""# Daily Trading System Report
**Date**: {data['date']}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent**: {self.name}

---

"""
            return header + report
            
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            return self._generate_fallback_report(data)
            
    def _build_gemini_prompt(self, data: Dict[str, Any]) -> str:
        """Build the prompt for Gemini to generate the report."""
        prompt = f"""You are an expert trading system analyst. Generate a comprehensive daily report based on the following data:

**Evolution System:**
{data['evolution']}

**Tester Performance:**
{data['testers']}

**Market Overview:**
{data['market']}

Please provide:
1. **Executive Summary**: Brief overview of the day's performance
2. **Evolution Progress**: Analysis of the evolution system's current generation
3. **Best Strategies**: Highlight top-performing organisms/strategies
4. **Testing Results**: Summary of tester agent performance
5. **Market Context**: Key market movements and their impact
6. **Recommendations**: Action items for tomorrow
7. **Risk Assessment**: Current system health and risk levels

Format the report in clear, professional markdown. Be concise but insightful. Focus on actionable insights.
"""
        return prompt
        
    def _generate_fallback_report(self, data: Dict[str, Any]) -> str:
        """Generate a basic report without AI if Gemini is unavailable."""
        report = f"""# Daily Trading System Report
**Date**: {data['date']}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Agent**: {self.name} (Fallback Mode)

---

## Evolution System

"""
        # Evolution stats
        evo = data.get('evolution', {})
        if 'current_generation' in evo:
            report += f"""- **Generation**: {evo['current_generation']}
- **Best Fitness**: {evo['best_fitness']}
- **Average Fitness**: {evo['avg_fitness']}
- **Population Size**: {evo['population_size']}

"""
        else:
            report += f"_{evo.get('status', 'No data')}_\n\n"
            
        # Tester stats
        report += "## Tester Performance\n\n"
        testers = data.get('testers', {})
        if 'testers' in testers:
            for t in testers['testers']:
                report += f"- **{t['agent']}**: {t['total_tests']} tests, {t['avg_win_rate']}% win rate, {t['passed']} passed\n"
            report += "\n"
        else:
            report += f"_{testers.get('status', 'No data')}_\n\n"
            
        # Market overview
        report += "## Market Overview\n\n"
        market = data.get('market', {})
        if 'latest_data' in market:
            for m in market['latest_data']:
                report += f"- **{m['symbol']}**: ₹{m['close']:,.2f} (Volume: {m['volume']:,})\n"
            report += "\n"
        else:
            report += f"_{market.get('status', 'No data')}_\n\n"
            
        report += "---\n\n*Note: AI-powered insights unavailable. Using basic template.*\n"
        return report
        
    def save_report(self, report: str, report_type: str = "EVENING") -> bool:
        """
        Save the generated report to database and file.
        
        Args:
            report: Markdown report content
            report_type: 'MORNING' or 'EVENING'
            
        Returns:
            True if successful
        """
        try:
            # Save to database
            report_date = date.today()
            with self.db._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO daily_reports (report_date, type, content, timestamp)
                    VALUES (?, ?, ?, ?)
                """, (report_date, report_type, report, datetime.now()))
                conn.commit()
                
            # Save to file
            reports_dir = os.path.join(os.path.dirname(__file__), '../../data/reports')
            os.makedirs(reports_dir, exist_ok=True)
            
            filename = f"{report_type.lower()}_{report_date}.md"
            filepath = os.path.join(reports_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
                
            logger.info(f"Report saved: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving report: {e}")
            return False
            
    def run(self) -> Dict[str, Any]:
        """
        Execute the full Expert Agent workflow:
        1. Collect data
        2. Generate report
        3. Save report
        
        Returns:
            Status dict
        """
        logger.info(f"[{self.agent_id}] Starting daily report generation...")
        
        try:
            # Step 1: Collect data
            data = self.collect_daily_data()
            
            # Step 2: Generate report
            report = self.generate_report(data)
            
            # Step 3: Save report
            success = self.save_report(report, "EVENING")
            
            if success:
                logger.info(f"[{self.agent_id}] Daily report generated successfully.")
                return {
                    "status": "success",
                    "report_length": len(report),
                    "date": data['date']
                }
            else:
                return {
                    "status": "error",
                    "message": "Failed to save report"
                }
                
        except Exception as e:
            logger.error(f"[{self.agent_id}] Error generating report: {e}")
            return {
                "status": "error",
                "message": str(e)
            }


if __name__ == "__main__":
    # Test the Expert Agent
    logging.basicConfig(level=logging.INFO)
    agent = ExpertAgent()
    result = agent.run()
    print(f"\nResult: {result}")

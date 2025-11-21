from backend.evolution.code_generator import CodeGenerator
from backend.evolution.weakness_analyzer import WeaknessAnalyzer
from backend.database.db import db

class ImprovementLoop:
    """
    Orchestrates the self-improvement cycle:
    Analyze -> Generate -> Verify -> Store
    """
    
    def __init__(self):
        self.generator = CodeGenerator()
        self.analyzer = WeaknessAnalyzer()

    def improve_strategy(self, strategy_id: str, current_code: str, metrics: dict):
        """
        Runs one improvement cycle for a strategy.
        """
        print(f"Starting improvement loop for {strategy_id}...")
        
        # 1. Analyze Weakness
        weakness_report = self.analyzer.analyze(metrics)
        print(f"Analysis: {weakness_report}")
        
        if "No major weaknesses" in weakness_report:
            print("Strategy is good enough. Skipping improvement.")
            return
            
        # 2. Generate Improved Code
        prompt = f"Improve this trading strategy to fix the following weaknesses:\n{weakness_report}\n\nCurrent Code:\n{current_code}"
        try:
            new_code = self.generator.generate_strategy_code(prompt)
            
            # 3. Log Modification
            db.log_code_modification(
                file_path=f"strategy_{strategy_id}.py",
                modification_type="OPTIMIZATION",
                description=f"Fixed weaknesses: {weakness_report}",
                previous_code_hash=str(hash(current_code)),
                new_code_hash=str(hash(new_code)),
                status="PENDING"
            )
            print("Improvement generated and logged.")
            return new_code
            
        except Exception as e:
            print(f"Error generating improvement: {e}")

if __name__ == "__main__":
    loop = ImprovementLoop()
    loop.improve_strategy(
        "test_strat", 
        "def strategy(): pass", 
        {"sharpe_ratio": 0.5, "max_drawdown": -0.3}
    )

class WeaknessAnalyzer:
    """
    Analyzes performance metrics to identify specific weaknesses in a strategy.
    """
    
    @staticmethod
    def analyze(metrics: dict) -> str:
        """
        Returns a textual report of weaknesses.
        """
        weaknesses = []
        
        if metrics.get('sharpe_ratio', 0) < 1.0:
            weaknesses.append("Low risk-adjusted return (Sharpe < 1.0). Strategy takes too much risk for the return.")
            
        if metrics.get('max_drawdown', 0) < -0.20:
            weaknesses.append("High drawdown (> 20%). Strategy needs better stop-loss or position sizing.")
            
        if metrics.get('win_rate', 0) < 0.40:
            weaknesses.append("Low win rate (< 40%). Entry signals might be false positives.")
            
        if not weaknesses:
            return "No major weaknesses detected."
            
        return "Weaknesses Detected:\n- " + "\n- ".join(weaknesses)

if __name__ == "__main__":
    metrics = {"sharpe_ratio": 0.8, "max_drawdown": -0.25, "win_rate": 0.35}
    print(WeaknessAnalyzer.analyze(metrics))

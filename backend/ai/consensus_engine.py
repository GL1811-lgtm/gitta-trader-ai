"""
Consensus Engine
Analyzes responses from multiple AI models and creates consensus
"""

from typing import List, Dict
import re
from collections import Counter

class ConsensusEngine:
    """Creates consensus from multiple AI model responses"""
    
    def __init__(self):
        pass
    
    def extract_score(self, text: str) -> float:
        """
        Extract viability score from AI response
        
        Args:
            text: AI response text
            
        Returns:
            Score (1-10), or 0 if not found
        """
        if not text:
            return 0.0
        
        # Look for patterns like "8/10", "score: 7", "viability: 6"
        patterns = [
            r'(\d+)/10',
            r'score[:\s]+(\d+)',
            r'viability[:\s]+(\d+)',
            r'rating[:\s]+(\d+)',
            r'(\d+)\s*out\s*of\s*10'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                score = float(match.group(1))
                return min(10.0, max(1.0, score))
        
        return 0.0
    
    def extract_recommendation(self, text: str) -> str:
        """
        Extract recommendation from AI response
        
        Args:
            text: AI response text
            
        Returns:
            'VIABLE', 'MODERATE', or 'RISKY'
        """
        if not text:
            return "UNKNOWN"
        
        text_lower = text.lower()
        
        # Check for explicit recommendations
        if "viable" in text_lower and "not viable" not in text_lower:
            return "VIABLE"
        elif "risky" in text_lower or "high risk" in text_lower:
            return "RISKY"
        elif "moderate" in text_lower or "caution" in text_lower:
            return "MODERATE"
        
        return "UNKNOWN"
    
    def calculate_consensus(self, responses: List[Dict]) -> Dict:
        """
        Calculate consensus from multiple AI responses
        
        Args:
            responses: List of AI response dicts
            
        Returns:
            Consensus analysis
        """
        successful = [r for r in responses if r.get("success", False)]
        
        if not successful:
            return {
                "status": "failed",
                "reason": "No successful responses",
                "confidence": 0.0
            }
        
        # Extract scores and recommendations
        scores = []
        recommendations = []
        weighted_scores = []
        
        for response in successful:
            score = self.extract_score(response.get("content", ""))
            recommendation = self.extract_recommendation(response.get("content", ""))
            weight = response.get("weight", 1.0)
            
            if score > 0:
                scores.append(score)
                weighted_scores.append(score * weight)
            
            if recommendation != "UNKNOWN":
                recommendations.append(recommendation)
        
        # Calculate metrics
        total_responses = len(successful)
        avg_score = sum(scores) / len(scores) if scores else 0.0
        weighted_avg = sum(weighted_scores) / sum([r.get("weight", 1.0) for r in successful]) if weighted_scores else 0.0
        
        # Determine consensus recommendation
        if recommendations:
            rec_counts = Counter(recommendations)
            consensus_rec = rec_counts.most_common(1)[0][0]
            consensus_count = rec_counts[consensus_rec]
            agreement_rate = consensus_count / len(recommendations)
        else:
            consensus_rec = "UNKNOWN"
            agreement_rate = 0.0
        
        # Calculate confidence
        confidence = self._calculate_confidence(
            scores,
            recommendations,
            total_responses,
            agreement_rate
        )
        
        # Identify agreements and disagreements
        agreements = []
        disagreements = []
        
        for rec, count in Counter(recommendations).items():
            if rec == consensus_rec:
                agreements.append({
                    "recommendation": rec,
                    "count": count,
                    "percentage": (count / len(recommendations) * 100) if recommendations else 0
                })
            else:
                disagreements.append({
                    "recommendation": rec,
                    "count": count,
                    "percentage": (count / len(recommendations) * 100) if recommendations else 0
                })
        
        return {
            "status": "success",
            "total_responses": total_responses,
            "scores_found": len(scores),
            "average_score": round(avg_score, 2),
            "weighted_average_score": round(weighted_avg, 2),
            "consensus_recommendation": consensus_rec,
            "agreement_rate": round(agreement_rate * 100, 1),
            "confidence": round(confidence * 100, 1),
            "agreements": agreements,
            "disagreements": disagreements,
            "all_scores": scores,
            "all_recommendations": recommendations,
            "interpretation": self._interpret_results(avg_score, consensus_rec, confidence)
        }
    
    def _calculate_confidence(
        self,
        scores: List[float],
        recommendations: List[str],
        total_responses: int,
        agreement_rate: float
    ) -> float:
        """
        Calculate confidence score based on multiple factors
        
        Returns:
            Confidence score (0.0-1.0)
        """
        factors = []
        
        # Factor 1: Agreement rate (40% weight)
        factors.append(agreement_rate * 0.4)
        
        # Factor 2: Number of responses (20% weight)
        response_factor = min(total_responses / 8.0, 1.0)  # 8 is target
        factors.append(response_factor * 0.2)
        
        # Factor 3: Score consistency (20% weight)
        if len(scores) >= 2:
            score_std = (max(scores) - min(scores)) / 10.0  # Normalize to 0-1
            consistency = 1.0 - min(score_std, 1.0)
            factors.append(consistency * 0.2)
        
        # Factor 4: Number of scores found (20% weight)
        score_factor = len(scores) / total_responses if total_responses > 0 else 0
        factors.append(score_factor * 0.2)
        
        return sum(factors)
    
    def _interpret_results(
        self,
        avg_score: float,
        recommendation: str,
        confidence: float
    ) -> str:
        """Generate human-readable interpretation"""
        
        if avg_score >= 7.5:
            score_text = "strong"
        elif avg_score >= 5.5:
            score_text = "moderate"
        else:
            score_text = "weak"
        
        if confidence >= 0.75:
            conf_text = "high confidence"
        elif confidence >= 0.5:
            conf_text = "moderate confidence"
        else:
            conf_text = "low confidence"
        
        return f"This is a {score_text} strategy ({recommendation.lower()}) with {conf_text}."


def create_consensus(responses: List[Dict]) -> Dict:
    """Convenience function to create consensus"""
    engine = ConsensusEngine()
    return engine.calculate_consensus(responses)


if __name__ == "__main__":
    # Test consensus engine
    print("=" * 60)
    print("Consensus Engine Test")
    print("=" * 60)
    
    # Sample responses
    sample_responses = [
        {
            "model_name": "Model 1",
            "content": "Viability score: 8/10. This is a VIABLE strategy with good risk management.",
            "weight": 1.2,
            "success": True
        },
        {
            "model_name": "Model 2",
            "content": "I rate this 7 out of 10. VIABLE for experienced traders.",
            "weight": 1.0,
            "success": True
        },
        {
            "model_name": "Model 3",
            "content": "Score: 6/10. MODERATE risk, needs improvements.",
            "weight": 1.0,
            "success": True
        },
        {
            "model_name": "Model 4",
            "content": "This is RISKY. Score: 4/10. Not recommended.",
            "weight": 0.9,
            "success": True
        }
    ]
    
    engine = ConsensusEngine()
    consensus = engine.calculate_consensus(sample_responses)
    
    print(f"\nConsensus Results:")
    print(f"  Average Score: {consensus['average_score']}/10")
    print(f"  Weighted Average: {consensus['weighted_average_score']}/10")
    print(f"  Recommendation: {consensus['consensus_recommendation']}")
    print(f"  Agreement Rate: {consensus['agreement_rate']}%")
    print(f"  Confidence: {consensus['confidence']}%")
    print(f"\nInterpretation: {consensus['interpretation']}")

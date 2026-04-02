from BusinessLogic.SoccerScorer import SoccerScorer
from BusinessLogic.SoftballScorer import SoftballScorer
from BusinessLogic.TennisScorer import TennisScorer
from BusinessLogic.VolleyballScorer import VolleyballScorer


class ScoreFactory:
    # field types: tennis, volleyball, softball, soccer

    @staticmethod
    def create_scorer(sport_name):
        if sport_name == "tennis":
            return TennisScorer()
        elif sport_name == "volleyball":
            return VolleyballScorer()
        elif sport_name == "softball":
            return SoftballScorer()
        elif sport_name == "soccer":
            return SoccerScorer()
        else:
            raise ValueError(f"Unsupported sport: {sport_name}")
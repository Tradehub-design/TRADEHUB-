class GradeEngine:

    @staticmethod
    def grade(edge_score):

        if edge_score >= 95:
            return "S"

        if edge_score >= 90:
            return "A+"

        if edge_score >= 80:
            return "A"

        if edge_score >= 70:
            return "B"

        if edge_score >= 60:
            return "C"

        return "F"

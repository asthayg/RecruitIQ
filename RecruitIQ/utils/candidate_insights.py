def generate_candidate_insights(score, matched, missing):

    # -------------------------
    # Resume Grade
    # -------------------------

    if score >= 90:
        grade = "A+"

    elif score >= 80:
        grade = "A"

    elif score >= 70:
        grade = "B+"

    elif score >= 60:
        grade = "B"

    else:
        grade = "C"

    # -------------------------
    # Hiring Decision
    # -------------------------

    if score >= 85:

        decision = "Proceed to Technical Interview"

        confidence = 95

    elif score >= 70:

        decision = "Recommended for Interview"

        confidence = 82

    elif score >= 60:

        decision = "Needs Skill Improvement"

        confidence = 65

    else:

        decision = "Not Ready Yet"

        confidence = 35

    # -------------------------
    # Salary Prediction
    # -------------------------

    if score >= 90:

        internship = "₹30K – ₹50K / month"

        fulltime = "₹12 – ₹18 LPA"

    elif score >= 80:

        internship = "₹20K – ₹35K / month"

        fulltime = "₹8 – ₹12 LPA"

    elif score >= 70:

        internship = "₹15K – ₹25K / month"

        fulltime = "₹6 – ₹8 LPA"

    else:

        internship = "₹5K – ₹12K / month"

        fulltime = "₹3 – ₹5 LPA"

    return {

        "grade": grade,

        "decision": decision,

        "confidence": confidence,

        "internship": internship,

        "fulltime": fulltime

    }
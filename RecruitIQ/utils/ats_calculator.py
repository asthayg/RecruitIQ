def calculate_ats(matched,total):

    score = (
        len(matched)/total
    ) * 100

    return round(score,2)
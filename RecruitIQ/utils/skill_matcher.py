def match_skills(resume, skills):

    matched = []

    for skill in skills:

        if skill.lower() in resume.lower():

            matched.append(skill)

    return matched
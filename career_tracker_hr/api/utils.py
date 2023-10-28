def percentage_of_similarity(vacancy_skills, candidate_skills):
    vacancy_skills = [skill.name for skill in vacancy_skills]
    candidate_skills = [skill.name for skill in candidate_skills]

    similarity_skills = set(candidate_skills).intersection(vacancy_skills)

    if len(vacancy_skills) == 0:
        similarity = 100
    else:
        similarity = len(similarity_skills) / len(vacancy_skills) * 100
    
    return similarity

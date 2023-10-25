def percentage_of_similarity(
        vacancy_skills: list[dict], candidate_skills: list[dict]
):
    vacancy_skills = [skill['name'] for skill in vacancy_skills]
    candidate_skills = [skill['name'] for skill in candidate_skills]

    similarity_skills = set(candidate_skills).intersection(vacancy_skills)
    similarity = len(similarity_skills) / len(vacancy_skills) * 100
    
    return similarity
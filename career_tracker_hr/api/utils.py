from django.http import HttpResponse

from api.constants import WEIGHT

def percentage_of_similarity(vacancy_skills, candidate_skills):
    """Рассчет процента совпадения"""
    vacancy_skills = [(skill[0].name, skill[1]) for skill in vacancy_skills]
    candidate_skills = [skill.name for skill in candidate_skills]

    sum_weight = sum(WEIGHT[skill[1]] for skill in vacancy_skills)

    sum_candidate_skills = 0
    for vacancy_skill in vacancy_skills:
        if vacancy_skill[0] in candidate_skills:
            sum_candidate_skills += WEIGHT[vacancy_skill[1]]

    if len(vacancy_skills) == 0:
        similarity = 100
    else:
        similarity = sum_candidate_skills / sum_weight * 100
    return round(similarity)


def download_file(content):
    """Загрузка файла"""
    with open(content.path, 'rb') as file:
        file_extension = content.name.split('.')[-1]
        content_type = f'application/{file_extension}'
        response = HttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{content.name}"'
        return response

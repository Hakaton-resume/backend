from django.http import HttpResponse

from api.constants import WEIGHT, EXPERIENCE


def skills_compаration(vacancy_skills, candidate_skills):
    """Рассчет процента совпадения"""
    vacancy_skills = [(skill[0].name, skill[1]) for skill in vacancy_skills]
    candidate_skills = [skill.name for skill in candidate_skills]

    sum_weight = sum(WEIGHT[skill[1]] for skill in vacancy_skills)

    sum_candidate_skills = 0
    for vacancy_skill in vacancy_skills:
        if vacancy_skill[0] in candidate_skills:
            sum_candidate_skills += WEIGHT[vacancy_skill[1]]

    if len(vacancy_skills) == 0:
        similarity = 1
    else:
        similarity = sum_candidate_skills / sum_weight
    return similarity


def experience_compаration(vacancy_experience, student_experience):
    """Сравнение требуемого в вакансии опыта и опыта соискателя"""
    try:
        required_experience = EXPERIENCE[vacancy_experience]
        if required_experience[0] <= int(student_experience) <= required_experience[1]:
            return 1
        elif required_experience[0] > int(student_experience):
            return 0
        return 0.9
    except KeyError:
        try:
            if vacancy_experience == student_experience:
                return 1
            elif vacancy_experience < student_experience:
                return 0.9
            return 0
        except Exception:
            return None


def percentage_of_similarity(*args):
    """Рассчет процента совпадений"""
    count = 0
    sum_args = 0
    for arg in args:
        if arg is not None:
            count += 1
            sum_args += arg
    return round(sum_args / count * 100)


def download_file(content):
    """Загрузка файла"""
    with open(content.path, 'rb') as file:
        file_extension = content.name.split('.')[-1]
        content_type = f'application/{file_extension}'
        response = HttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{content.name}"'
        return response

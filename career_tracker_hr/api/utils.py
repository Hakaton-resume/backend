from django.http import HttpResponse

def percentage_of_similarity(vacancy_skills, candidate_skills):
    vacancy_skills = [skill.name for skill in vacancy_skills]
    candidate_skills = [skill.name for skill in candidate_skills]

    similarity_skills = set(candidate_skills).intersection(vacancy_skills)

    if len(vacancy_skills) == 0:
        similarity = 100
    else:
        similarity = len(similarity_skills) / len(vacancy_skills) * 100
    
    return similarity

def download_file(content):
    with open(content.path, 'rb') as file:
        file_extension = content.name.split('.')[-1]
        content_type = f'application/{file_extension}'
        response = HttpResponse(file, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{content.name}"'
        return response


        
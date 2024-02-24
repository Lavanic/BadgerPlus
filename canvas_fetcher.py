import requests
from datetime import datetime, timedelta

def fetch_canvas_assignments_and_exams(access_token):
    canvas_domain = 'canvas.wisc.edu'
    courses_url = f'https://{canvas_domain}/api/v1/courses'
    headers = {'Authorization': f'Bearer {access_token}'}

    structured_assignments_exams = []
    now = datetime.utcnow()
    one_week_later = now + timedelta(days=7)

    response = requests.get(courses_url, headers=headers)
    if response.status_code == 200:
        courses = response.json()
        for course in courses:
            course_name = course.get('name', 'Unnamed Course')
            assignments_url = f'{courses_url}/{course["id"]}/assignments'
            assignments_response = requests.get(assignments_url, headers=headers)
            if assignments_response.status_code == 200:
                assignments = assignments_response.json()
                for assignment in assignments:
                    due_at = assignment.get('due_at')
                    if due_at:
                        due_date = datetime.strptime(due_at, '%Y-%m-%dT%H:%M:%SZ')
                        if now <= due_date <= one_week_later:
                            structured_assignments_exams.append({
                                'course_name': course_name,
                                'name': assignment.get('name'),
                                'due_at': due_at,
                                'type': 'Exam' if "exam" in assignment.get("name", "").lower() else 'Assignment'
                            })
    return structured_assignments_exams

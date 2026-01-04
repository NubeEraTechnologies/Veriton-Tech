# path('upload/', views.upload_html_file, name='upload_html'),
# path('view/', views.view_html_file, name='view_html'),  # File list view

import uuid
from urllib.parse import urljoin
import requests
from django.http import JsonResponse
import base64  # Import the base64 module
# Load the Git access token from environment variables

GIT_REPO_URL = "https://oauth:NubeEra-ImranAli@github.com/NubeEra-ImranAli/study_kit.git"
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/NubeEra-ImranAli/study_kit/main/"
GIT_API_URL = "https://api.github.com/repos/NubeEra-ImranAli/study_kit/contents/"

def load_file_mapping():
    headers = {
        "Authorization": f"Bearer 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"  # Use your GitHub personal access token
    }
    response = requests.get(GIT_API_URL, headers=headers)

    if response.status_code == 200:
        return {file['name']: str(uuid.uuid4()) for file in response.json()}
            
    else:
        return {}
def upload_html_file(request):
    if request.method == "POST":
        # Get the uploaded file
        uploaded_file = request.FILES['file']
        file_name = uploaded_file.name

        # Prepare the API URL and headers
        api_url = f"{GIT_API_URL}{file_name}"
        headers = {
            "Authorization": f"Bearer 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",  # Use your GitHub personal access token
            "Content-Type": "application/json"
        }

        # Read the content of the uploaded file
        content = uploaded_file.read().decode('utf-8')
        # Prepare data to send to GitHub
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
        data = {
            "message": f"Add {file_name}",
            "content": encoded_content,
            "branch": "main"
        }

        # Send the PUT request to GitHub
        response = requests.put(api_url, headers=headers, json=data)

        if response.status_code == 201:
            return redirect('view_html')  # Redirect to the file list view
        else:
            return JsonResponse({"error": "Failed to upload file"}, status=response.status_code)

    return render(request, 'bootcampapp/upload.html')

def view_html_file(request):
    file_mapping = load_file_mapping()  # Load file mapping each time
    return render(request, 'bootcampapp/file_list.html', {
        'file_mapping': file_mapping
    })
import os
import base64
from dotenv import load_dotenv
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
from azure.devops.v6_0.git.models import GitPush, GitCommitRef, GitCommitChanges, GitChange, ItemContent


# Azure DevOps organization URL and personal access token
organization_url = os.getenv("AZURE_DEVOPS_URL")
personal_access_token = os.getenv("AZURE_DEVOPS_PAT")

# Project and repository information
project_name = os.getenv("AZURE_DEVOPS_PROJECT")
repository_id =  os.getenv("AZURE_DEVOPS_REPOSITORY") # Replace with your repository ID

# File content and path
file_content = "This is the content of the file."
file_path = "path/to/your/file.txt"

# Create a connection to Azure DevOps
credentials = BasicAuthentication("", personal_access_token)
connection = Connection(base_url=organization_url, creds=credentials)

# Get the Git client
git_client = connection.clients.get_git_client()

# Encode the file content
file_content_bytes = file_content.encode("utf-8")
file_content_base64 = base64.b64encode(file_content_bytes).decode("utf-8")

# Create a change for the new file
change = GitChange(change_type="add", item={"path": file_path})
change.new_content = ItemContent(content_type="rawtext", content=file_content_base64)

# Create a commit for the change
commit = GitCommitRef(comment="Add new file", changes=[change])

# Push the commit to the branch
push = GitPush(commits=[commit], ref_updates=None)
git_client.create_push(push, project=project_name, repository_id=repository_id, ref_name=f"refs/heads/{branch_name}")

print("File uploaded to the repository.")
import requests
from typing import Dict, List, Optional, Any, Union
from requests.auth import HTTPBasicAuth

from .config import jenkins_settings


class JenkinsClient:
    """Client for interacting with Jenkins API."""
    
    def __init__(self):
        """Initialize the Jenkins client using configuration settings."""
        try:
            # Disable SSL verification warnings
            import urllib3
            urllib3.disable_warnings()
            
            if jenkins_settings.username and jenkins_settings.token:
                print(f"Using API token authentication for user {jenkins_settings.username}")
                self.auth = HTTPBasicAuth(jenkins_settings.username, jenkins_settings.token)
                self.base_url = jenkins_settings.jenkins_url.rstrip('/')
                
                # Test connection
                print("\nTesting connection with direct request...")
                response = requests.get(f"{self.base_url}/api/json", 
                                     auth=self.auth, 
                                     verify=False)
                print(f"Direct request status: {response.status_code}")
                
                if response.ok:
                    print("Direct API call successful!")
                    data = response.json()
                    print(f"Server version: {data.get('_class', 'unknown')}")
                    
                    # Store the initial jobs data
                    self._jobs = data.get('jobs', [])
                    print(f"Found {len(self._jobs)} jobs:")
                    for job in self._jobs:
                        print(f"- {job['name']} ({job.get('color', 'unknown')})")
                else:
                    print(f"Direct API call failed: {response.text}")
                    raise Exception("Failed to connect to Jenkins")
            else:
                raise ValueError("Username and token are required")
            
        except Exception as e:
            print(f"\nError connecting to Jenkins: {str(e)}")
            print("\nPlease check:")
            print(f"1. Jenkins server is running at {jenkins_settings.jenkins_url}")
            print("2. Your credentials in .env file are correct")
            print("3. You have proper permissions in Jenkins")
            import traceback
            traceback.print_exc()
            raise
    
    def get_jobs(self) -> List[Dict[str, Any]]:
        """Get a list of all Jenkins jobs."""
        try:
            response = requests.get(f"{self.base_url}/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json().get('jobs', [])
        except Exception as e:
            print(f"Error getting Jenkins jobs: {str(e)}")
            return []
    
    def get_job_info(self, job_name: str) -> Dict[str, Any]:
        """Get detailed information about a specific job."""
        try:
            response = requests.get(f"{self.base_url}/job/{job_name}/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting job info for {job_name}: {str(e)}")
            raise
    
    def get_build_info(self, job_name: str, build_number: int) -> Dict[str, Any]:
        """Get information about a specific build."""
        try:
            response = requests.get(f"{self.base_url}/job/{job_name}/{build_number}/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting build info for {job_name} #{build_number}: {str(e)}")
            raise
    
    def get_build_console_output(self, job_name: str, build_number: int) -> str:
        """Get console output from a build."""
        try:
            response = requests.get(f"{self.base_url}/job/{job_name}/{build_number}/consoleText",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"Error getting build console for {job_name} #{build_number}: {str(e)}")
            raise
    
    def build_job(self, job_name: str, parameters: Optional[Dict[str, Any]] = None) -> int:
        """Trigger a build for a job."""
        try:
            url = f"{self.base_url}/job/{job_name}/build"
            if parameters:
                url = f"{self.base_url}/job/{job_name}/buildWithParameters"
            response = requests.post(url,
                                  auth=self.auth,
                                  params=parameters,
                                  verify=False)
            response.raise_for_status()
            # Get queue item number from Location header
            location = response.headers.get('Location', '')
            queue_id = location.split('/')[-2] if location else None
            return int(queue_id) if queue_id and queue_id.isdigit() else -1
        except Exception as e:
            print(f"Error triggering build for {job_name}: {str(e)}")
            raise
    
    def stop_build(self, job_name: str, build_number: int) -> None:
        """Stop a running build."""
        try:
            response = requests.post(f"{self.base_url}/job/{job_name}/{build_number}/stop",
                                  auth=self.auth,
                                  verify=False)
            response.raise_for_status()
        except Exception as e:
            print(f"Error stopping build {job_name} #{build_number}: {str(e)}")
            raise
    
    def get_queue_info(self) -> List[Dict[str, Any]]:
        """Get information about the queue."""
        try:
            response = requests.get(f"{self.base_url}/queue/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json().get('items', [])
        except Exception as e:
            print(f"Error getting queue info: {str(e)}")
            return []
    
    def get_node_info(self, node_name: str) -> Dict[str, Any]:
        """Get information about a specific node."""
        try:
            response = requests.get(f"{self.base_url}/computer/{node_name}/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error getting node info for {node_name}: {str(e)}")
            raise
    
    def get_nodes(self) -> List[Dict[str, str]]:
        """Get a list of all nodes."""
        try:
            response = requests.get(f"{self.base_url}/computer/api/json",
                                 auth=self.auth,
                                 verify=False)
            response.raise_for_status()
            return response.json().get('computer', [])
        except Exception as e:
            print(f"Error getting nodes: {str(e)}")
            return []


# Create a singleton instance
jenkins_client = JenkinsClient()

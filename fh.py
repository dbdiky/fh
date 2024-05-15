import subprocess
import os
import re
from datetime import datetime  # Import the datetime module

def filter_pods_by_status(context, statuses_to_filter):
    try:
        print("Context:", context)
        subprocess.run(["kubectl", "config", "use-context", context], check=True)
        result = subprocess.run(["kubectl", "get", "pods", "-A", "-o", "wide"], check=True, capture_output=True, text=True)
        lines = result.stdout.split("\n")
        for line in lines:
            if any(status in line for status in statuses_to_filter):
                print(line)
        print("------------------------")
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr.strip())
    except Exception as e:
        print("Error:", e)

def get_all_contexts():
    try:
        result = subprocess.run(["kubectl", "config", "get-contexts", "-o", "name"], check=True, capture_output=True, text=True)
        contexts = result.stdout.strip().split("\n")
        return contexts
    except subprocess.CalledProcessError as e:
        print("Error:", e.stderr.strip())
        return []
    except Exception as e:
        print("Error:", e)
        return []        

def execute_aws_command(command):
    if command is None:
        print("Error: No command provided.")
        return
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        print("Command executed successfully:")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print(e.stderr.strip())
    except Exception as e:
        print("Error:", e)

def execute_terraform_command(command):
    try:
        result = subprocess.run(command, shell=True, check=True, text=True)
        print("Command executed successfully:")
        print(result.stdout.strip())
    except subprocess.CalledProcessError as e:
        print("Error executing command:")
        print(e.stderr.strip())
    except Exception as e:
        print("Error:", e)

def execute_kubectl_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            print("Error executing command:")
            print(result.stderr.strip())  # Print error output
            return None
    except Exception as e:
        print("Error:", e)
        return None
        
#import subprocess

def get_current_kubectl_context():
    try:
        result = subprocess.run(['kubectl', 'config', 'current-context'], capture_output=True, text=True)
        current_context = result.stdout.strip()
        return current_context
    except Exception as e:
        print("Error:", e)
        return None

def choose_kubectl_context():
    print("\nKubernetes Contexts:")
    try:
        current_context = get_current_kubectl_context()
        result = subprocess.run(['kubectl', 'config', 'get-contexts', '-o=name'], capture_output=True, text=True)
        contexts = result.stdout.strip().split('\n')
        if not contexts:
            print("No contexts found.")
            return None
        for i, context in enumerate(contexts):
            if context == current_context:
                print(f"{i+1}. * {context}")
            else:
                print(f"{i+1}. {context}")
        print(f"{len(contexts) + 1}. ** Add new context **")
        print(f"{len(contexts) + 2}. ** Remove context **")
        choice = input("Context: ")
        if choice.lower() == 'exit':
            return None
        elif choice == '':
            return current_context
        choice = int(choice)
        if choice == len(contexts) + 1:
            add_new_context()
            return choose_kubectl_context()
        elif choice == len(contexts) + 2:
            remove_context(contexts)
            return choose_kubectl_context()
        if choice < 1 or choice > len(contexts):
            print("Invalid choice.")
            return None
        return contexts[choice - 1]
    except Exception as e:
        print("Error:", e)
        return None
    
def add_new_context():
    try:
        region = input("Enter the region: ")
        cluster_name = input("Enter the cluster name: ")
        #context_name = input("Enter the context name: ")
        command = f"AWS_PROFILE=fh aws eks --region {region} update-kubeconfig --name {cluster_name}"
        subprocess.run(command, shell=True, check=True)
        print(f"Context '{cluster_name}' added successfully.")
    except Exception as e:
        print("Error:", e)

def remove_context(contexts):
    try:
        print("\nRemove Context:")
        choice = int(input("Enter the number of the context to remove: "))
        if choice < 1 or choice > len(contexts):
            print("Invalid choice.")
            return
        context_to_remove = contexts[choice - 1]
        subprocess.run(['kubectl', 'config', 'delete-context', context_to_remove])
        print(f"Context '{context_to_remove}' removed successfully.")
    except ValueError:
        print("Invalid input. Please enter a valid number.")
    except Exception as e:
        print("Error:", e)

def determine_namespace(context):
    if "test" in context.lower():
        return "test"
    else:
        return "main"

def main_menu(namespace, current_context):
    while True:
        print("\n\033[1;31mCurrent Context:\033[0m", current_context)
        print("\nMain Menu")
        print("1. Switch Kubernetes Context")
        print("2. SSC")
        print("3. SAST")
        print("4. DAST")
        print("5. LIM")
        print("6. Cluster")
        print("7. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context
        elif choice == '2':
            ssc_menu(namespace, current_context)
        elif choice == '3':
            sast_menu(namespace, current_context)
        elif choice == '4':
            dast_menu(namespace, current_context)
        elif choice == '5':
            lim_menu(namespace, current_context)
        elif choice == '6':
            cluster_menu(namespace, current_context)                
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def ssc_menu(namespace, current_context):
    while True:
        print("\n\033[1;31mCurrent Context:\033[0m", current_context)
        print("\nSSC Options")
        print("1. Switch Kubernetes Context")
        print("2. View SSC Log")
        print("3. Watch SSC Log")
        print("4. Download SSC Log")
        print("5. View SSC Audit Log")
        print("6. Watch SSC Audit Log")
        print("7. Download SSC Audit Log")
        print("8. Reboot SSC")
        print("9. SSC Drive Usage")
        print("10. Clear Tomcat Temp Folder")
        print("11. Clear Tomcat Logs")
        print("12. Exit")
        print("13. Go back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context
        elif choice == '2':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- cat /fortify/ssc/logs/ssc.log"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")

        elif choice == '3':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- tail /fortify/ssc/logs/ssc.log -f"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '4':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"ssc-log-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- cat /fortify/ssc/logs/ssc.log"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")
                
        elif choice == '5':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- cat /fortify/ssc/logs/ssc_audit.log"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")

        elif choice == '6':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- tail /fortify/ssc/logs/ssc_audit.log -f"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)
              
        elif choice == '7':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"ssc-audit-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- cat /fortify/ssc/logs/ssc_audit.log"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")
                
        elif choice == '8':
            command = f"kubectl delete po -n {namespace} ssc-webapp-0"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '9':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- df -ah"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '10':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- bash -c 'rm -rf /fortify/tomcat/temp/*'"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '11':
            command = f"kubectl exec -it -n {namespace} ssc-webapp-0 -- bash -c 'rm -rf /fortify/tomcat/logs/*'"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '12':
            print("Exiting...")
            break

        elif choice == '13':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def sast_menu(namespace, current_context):
    while True:
        print("\n\033[1;31mCurrent Context:\033[0m", current_context)
        print("\nSAST Options")
        print("1. Switch Kubernetes Context")
        print("2. View Controller Log")
        print("3. Watch Controller")
        print("4. Download Controller Log")
        print("5. Controller Disk Usage")
        print("6. List Job Directory")
        print("7. Scan Job Log")
        print("8. Scan Job Package")
        print("9. Job FH Support Log")
        print("10. Job Directory")
        print("11. Exit")
        print("12. Go back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context

        elif choice == '2':
            command = f"kubectl exec -it -n {namespace} scancentral-sast-controller-0 -- cat /fortify/logs/scancentralCtrl.log"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")

        elif choice == '3':
            command = f"kubectl exec -it -n {namespace} scancentral-sast-controller-0 -- tail /fortify/logs/scancentralCtrl.log -f"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '4':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"sast-ctrl-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl exec -it -n {namespace} scancentral-sast-controller-0 -- cat /fortify/logs/scancentralCtrl.log"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")
                
        elif choice == '5':
            command = f"kubectl exec -it -n {namespace} scancentral-sast-controller-0 -- df -ah"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")

        elif choice == '6':
            os_choice = input("OS: ")
            sensor = input("Enter the Sensor No.: ")
            job_id = input("Job ID or Enter to see all jobs: ")
            command = f"kubectl exec -it -n {namespace} scancentral-sast-worker-{os_choice}-{sensor} -- powershell -C ls jobs/{job_id}"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")

        elif choice == '7':
            os_choice = input("OS: ")
            sensor = input("Enter the Sensor No.: ")
            job_id = input("Job ID: ")
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"sast-scan-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl exec -it -n {namespace} scancentral-sast-worker-{os_choice}-{sensor} -- powershell -C cat jobs/{job_id}/scan.log"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")

        elif choice == '8':
            os_choice = input("OS: ")
            sensor = input("Enter the Sensor No.: ")
            job_id = input("Job ID: ")
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            # Define four commands and corresponding filenames
            commands_files = [
                (f"kubectl exec -it -n {namespace} scancentral-sast-controller-0 -- cat /fortify/logs/scancentralCtrl.log", f"sast-ctrl-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl exec -it -n {namespace} scancentral-sast-worker-{os_choice}-{sensor} -- powershell -C cat jobs/{job_id}/scan.log", f"sast-scan-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl exec -it -n {namespace} scancentral-sast-worker-{os_choice}-{sensor} -- powershell -C cat jobs/{job_id}/scan_FortifySupport.log", f"sast-FortifySupport-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log")
            ]
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            for command, filename in commands_files:
                file_path = os.path.join(directory, filename)
                result = execute_kubectl_command(command)
                if result:
                    result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                    try:
                        with open(file_path, 'w') as f:
                            f.write(result)
                        print(f"File '{filename}' created successfully at {file_path}")
                    except Exception as e:
                        print("Error:", e)
                else:
                    print(f"Failed to capture output from the command: {command}")
            
        elif choice == '9':
                os_choice = input("OS: ")
                sensor = input("Enter the Sensor No.: ")
                job_id = input("Job ID: ")
                cluster_name_match = re.search(r'/([^/]+)$', current_context)
                if cluster_name_match:
                    cluster_name = cluster_name_match.group(1).replace("fh-", "")
                else:
                    print("Error: Could not extract cluster name from context.")
                    continue
                filename = f"sast-FortifySupport-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
                context_name = current_context.split('/')[-1]
                directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
                os.makedirs(directory, exist_ok=True)
                file_path = os.path.join(directory, filename)
                command = f"kubectl exec -it -n {namespace} scancentral-sast-worker-{os_choice}-{sensor} -- powershell -C cat jobs/{job_id}/scan_FortifySupport.log"
                result = execute_kubectl_command(command)
                if result:
                    result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                    try:
                        with open(file_path, 'w') as f:
                            f.write(result)
                        print(f"File '{filename}' created successfully at {file_path}")
                    except Exception as e:
                        print("Error:", e)
                else:
                    print("Failed to capture output from the command.")

        elif choice == '10':
            os_choice = input("OS: ")
            sensor = input("Enter the Sensor No.: ")
            job_id = input("Paste the Job ID: ")
            # Extract context name from current_context
            context_name = current_context.split('/')[-1]  # Assuming context is in the format "namespace/context"
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name, job_id))
            os.makedirs(directory, exist_ok=True)
            # Construct the directory path inside the container
            container_dir = f"/fortify/jobs/{job_id}"  # Update DIR if necessary
            # Construct the command to execute
            command = f"kubectl cp -n {namespace} scancentral-sast-worker-{os_choice}-{sensor}:/{container_dir}/ {directory}"
            # Execute the command and capture the output
            result = execute_kubectl_command(command)
            # Check if the command executed successfully
            if result is not None:
                print("Directory copied successfully.")
            else:
                print("Failed to copy directory.")

        elif choice == '11':
            print("Exiting...")
            break
        elif choice == '12':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def dast_menu(namespace, current_context):
    while True:
        print("\n\033[1;31mCurrent Context:\033[0m", current_context)
        print("\nDAST Options")
        print("1. Switch Kubernetes Context")
        print("2. DAST Scanner Log")
        print("3. DAST API Log")
        print("4. DAST Global Services Log")
        print("5. DAST Utility Services")
        print("6. All DAST Logs")
        print("7. Exit")
        print("8. Go back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context
                
        elif choice == '2':
            sensor = input("Enter the Sensor No.: ")
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"dast-scanner-{sensor}-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl logs -n {namespace} scanner-{sensor}"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")

        elif choice == '3':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"dast-api-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl logs -n {namespace} scancentral-dast-api-0 -c api"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")

        elif choice == '4':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"dast-global-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl logs -n {namespace} scancentral-dast-globalservice-0 -c globalservice"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")

        elif choice == '5':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"dast-util-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl logs -n {namespace} scancentral-dast-utilityservice-0 -c utilityservice"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")

        elif choice == '6':
            sensor = input("Enter the Sensor No.: ")
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            # Define four commands and corresponding filenames
            commands_files = [
                (f"kubectl logs -n {namespace} scanner-{sensor}", f"dast-scanner-{sensor}-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-scanner-std-{sensor}", f"dast-scanner-std-{sensor}-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-api-0 -c api", f"dast-api-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-globalservice-0 -c globalservice", f"dast-global-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-utilityservice-0 -c utilityservice", f"dast-util-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-core-fc-server-0", f"dast-fc-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-core-api-0 -c api", f"dast-api-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-core-globalservice-0 -c globalservice", f"dast-global-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
                (f"kubectl logs -n {namespace} scancentral-dast-core-utilityservice-0 -c utilityservice", f"dast-util-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"),
            ]
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            
            for command, filename in commands_files:
                file_path = os.path.join(directory, filename)
                result = execute_kubectl_command(command)
                if result:
                    result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                    try:
                        with open(file_path, 'w') as f:
                            f.write(result)
                        print(f"File '{filename}' created successfully at {file_path}")
                    except Exception as e:
                        print("Error:", e)
                else:
                    print(f"Failed to capture output from the command: {command}") 

        elif choice == '7':
            print("Exiting...")
            break
        elif choice == '8':
            break
        else:
            print("Invalid choice. Please enter a valid option.")
        
def lim_menu(namespace, current_context):
    while True:
        print("\nLIM Options")
        print("1. Switch Kubernetes Context")
        print("2. View LIM Log")
        print("3. Watch LIM Log")
        print("4. Download LIM Log")
        print("5. Exit")
        print("6. Go back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context

        elif choice == '2':
            command = f"kubectl exec -it -n {namespace} lim-0 -- powershell -C 'Get-Content -Path log.txt'"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)

        elif choice == '3':
            command = f"kubectl exec -it -n {namespace} lim-0 -- powershell -C 'Get-Content -Path log.txt -Wait'"
            print("Executing command:", command)
            try:
                # Start tailing the log file
                subprocess.run(command, shell=True)
            except Exception as e:
                print("Failed to execute command:", e)        
        
        elif choice == '4':
            cluster_name_match = re.search(r'/([^/]+)$', current_context)
            if cluster_name_match:
                cluster_name = cluster_name_match.group(1).replace("fh-", "")
            else:
                print("Error: Could not extract cluster name from context.")
                continue
            filename = f"LIM-Log-{cluster_name}_{datetime.now().strftime('%m-%d_%H-%M')}.log"
            context_name = current_context.split('/')[-1]
            directory = os.path.expanduser(os.path.join("~", "Downloads", "Logs", context_name))
            os.makedirs(directory, exist_ok=True)
            file_path = os.path.join(directory, filename)
            command = f"kubectl exec -it -n main lim-0 -- powershell -C 'cat log.txt'"
            result = execute_kubectl_command(command)
            if result:
                result = re.sub(r'arn:aws:eks:[^:]+:\d+:cluster/[^ ]+', '', result)
                try:
                    with open(file_path, 'w') as f:
                        f.write(result)
                    print(f"File '{filename}' created successfully at {file_path}")
                except Exception as e:
                    print("Error:", e)
            else:
                print("Failed to capture output from the command.")
        elif choice == '5':
            print("Exiting...")
            break
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

def cluster_menu(namespace, current_context):
    while True:
        print("\nCluster Options")
        print("1. Switch Kubernetes Context")
        print("2. View All Clusters")
        print("3. Add EKS Cluster")
        print("4. Exit")
        print("5. Go back to Main Menu")
        choice = input("Enter your choice: ")

        if choice == '1':
            new_context = choose_kubectl_context()
            if new_context:
                if new_context != current_context:
                    print(f"Switching to context: {new_context}")
                    subprocess.run(['kubectl', 'config', 'use-context', new_context])
                    namespace = determine_namespace(new_context)
                    print(f"Determined namespace: {namespace}")
                    current_context = new_context

        elif choice == '2':
            contexts = get_all_contexts()
            statuses_to_filter = ["Pending", "Terminating", "CrashLoopBackOff"]
            for context in contexts:
                filter_pods_by_status(context, statuses_to_filter)

        elif choice == '3':
            command = f"kubectl logs -n {namespace} ssc-webapp-0"
            print("Executing command:", command)
            result = execute_kubectl_command(command)
            if result:
                print("Output:", result)
            else:
                print("Failed to execute command.")
        elif choice == '4':
            print("Exiting...")
            break
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    context = choose_kubectl_context()
    if context:
        print(f"Switching to context: {context}")
        subprocess.run(['kubectl', 'config', 'use-context', context])
        namespace = determine_namespace(context)
        print(f"Determined namespace: {namespace}")
        main_menu(namespace, context)
    else:
        print("No context chosen. Exiting...")

# Determine namespace based on context
def determine_namespace(context):
    if "test" in context.lower():
        return "test"
    else:
        return "main"

# Get the current date and time
current_date_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Get the current context
current_context = get_current_kubectl_context()

# Construct the filename
filename = f"{current_context}_{current_date_time}.log"

# Start with default context and namespace
context = None
namespace = None

# Call the main menu
main_menu(context, namespace)
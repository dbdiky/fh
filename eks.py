import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_eks_clusters(profile_name):
    try:
        # Create a session using the specified profile
        session = boto3.Session(profile_name=profile_name)
        
        # Initialize the EC2 client for the session to get the list of regions
        ec2_client = session.client('ec2')
        regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

        eks_clusters = {}

        # Loop through each region to list EKS clusters
        for region in regions:
            eks_client = session.client('eks', region_name=region)
            clusters = eks_client.list_clusters()['clusters']
            eks_clusters[region] = clusters

        return eks_clusters

    except NoCredentialsError:
        print("Credentials not available.")
        return None
    except PartialCredentialsError:
        print("Incomplete credentials provided.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == "__main__":
    profile_name = input("Enter the AWS profile name: ")
    eks_clusters = list_eks_clusters(profile_name)
    if eks_clusters is not None:
        for region, clusters in eks_clusters.items():
            if clusters:
                print(f"Region: {region}")
                for cluster in clusters:
                    print(f"  - Cluster Name: {cluster}")
            else:
                print(f"Region: {region} has no EKS clusters.")


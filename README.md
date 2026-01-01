# Automating AWS Services with Scripting and the AWS CLI

## Task 1: Connect to your Linux EC2 instance

In this task you will connect to your EC2 instance using AWS Systems Manager - Session manager.

- Copy the `Ec2InstanceSessionUrl` value from the list to the left of these instructions and paste it into a new web browser tab.
- A new web browser tab opens with a AWS Systems Manager - Session Manager console connecting to your EC2 instance.
- A set of commands are run automatically when you connect to the instance that change to the user's home directory and display the path of the working directory, similar to this:

![Topology](./pictures/Topology.png)

home/ec2-user
```

---

## Task 2: Three Ways to Access AWS

### Create a Key Pair using the CLI

You will now create a Key Pair with the AWS Command Line Interface (CLI).

**Note:** The Linux EC2 Instance provisioned for this lab is intended to simulate actions taken on your own machine. It goes against best practice to ever download and store a private key on an EC2 Instance.

1. Return to AWS Systems Manager - Session manager tab.
2. Paste this command in your Terminal:

```bash
aws ec2 create-key-pair --key-name CLI
```

**Example Output:**

```json
[ec2-user@ip-10-1-11-8 ~]$ aws ec2 create-key-pair --key-name CLI
{
    "KeyPairId": "key-00b36ec27ba38b980",
    "KeyName": "CLI",
    "KeyFingerprint": "d0:f4:f7:df:ca:7a:d8:9e:45:55:8e:73:7d:ef:58:2d:af:d2:e0:24",
    "KeyMaterial": "-----BEGIN RSA PRIVATE KEY-----\nREDACTED\n-----END RSA PRIVATE KEY-----"
}
```

A large block of text will appear with your RSA Private Key. You would normally store this key for future use, but it is not required for this lab. This command created a Key Pair just like the console. However, the AWS CLI gives the ability to interface with AWS without having to browse through a web page.

### Create a Key Pair Programmatically

It is also possible to interact with AWS services from a programming language or scripting language. This adds the ability to perform logic around AWS, such as obtaining a list of Amazon EC2 instances, then performing an action against each instance.

A small program has been provided that will create a Key Pair using the Python scripting language.

3. Paste this command to view the script:

```bash
cat create-keypair.py
```

**Script: create-keypair.py**

```python
#!/usr/bin/env python3
import boto3

# Connect to the Amazon EC2 service
ec2_client = boto3.client('ec2')

# Create a Key Pair
key = ec2_client.create_key_pair(KeyName = 'SDK')

# Print the private Fingerprint of the private key
print(key.get('KeyFingerprint'))
```

**The script does the following:**
- Loads the AWS SDK for Python, called boto3
- Connects to the Amazon EC2 service
- Creates a Key Pair called SDK
- Displays the Key Pair on-screen (this normally would be saved to a file)

4. Paste this command to run the script:

```bash
./create-keypair.py
```

**Example Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ ./create-keypair.py
/usr/local/lib/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
3e:57:b5:c0:a6:86:91:d9:17:ee:32:32:04:41:14:b6:b9:e5:8f:4d
```

### Cleanup Script

**Script: cleanup-keypairs.py**

```python
#!/usr/bin/env python3
import boto3

# Connect to the Amazon EC2 service
ec2_client = boto3.client('ec2')

keypairs = ec2_client.describe_key_pairs()

for key in keypairs['KeyPairs']:
    if 'lab' not in key['KeyName'].lower():
        print ("Deleting key pair", key['KeyName'])
        ec2_client.delete_key_pair(KeyName=key['KeyName'])
```

---

## Task 3: Access Amazon S3 with the AWS CLI

The AWS CLI provides convenient commands for accessing Amazon S3. Here are some of the available commands:

| Command | Purpose |
|---------|---------|
| `aws s3 mb s3://my-bucket` | Make a bucket |
| `aws s3 ls` | List all buckets |
| `aws s3 ls s3://my-bucket` | List the contents of a specific bucket |
| `aws s3 cp file s3://my-bucket/file` | Upload a file to a bucket |
| `aws s3 cp s3://my-bucket/file file` | Download a file from a bucket |
| `aws s3 cp s3://bucket1/file s3://bucket2/file` | Copy a file between buckets |
| `aws s3 sync . s3://my-bucket` | Synchronize a directory with an S3 bucket |

### Create a Bucket

Create a bucket with this command:

```bash
aws s3 mb s3://data-232435
```

**Example Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ aws s3 mb s3://data-232435
make_bucket: data-232435
```

### Upload a File

```bash
aws s3 cp create-keypair.py s3://data-232435
```

**Example Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ aws s3 cp create-keypair.py s3://data-232435
upload: ./create-keypair.py to s3://data-232435/create-keypair.py
```

### Sync Directory

View the contents of your bucket with this command:

```bash
aws s3 sync . s3://data-232435
```

**Example Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ aws s3 sync . s3://data-232435
upload: .aws/config to s3://data-232435/.aws/config
upload: .ssh/authorized_keys to s3://data-232435/.ssh/authorized_keys
upload: ./.bash_profile to s3://data-232435/.bash_profile
upload: ./.bash_logout to s3://data-232435/.bash_logout
upload: ./.bashrc to s3://data-232435/.bashrc
upload: ./.lesshst to s3://data-232435/.lesshst
upload: ./stopinator.py to s3://data-232435/stopinator.py
upload: ./highlow.py to s3://data-232435/highlow.py
upload: ./cleanup-keypairs.py to s3://data-232435/cleanup-keypairs.py
upload: ./show-credentials to s3://data-232435/show-credentials
upload: ./snapshotter.py to s3://data-232435/snapshotter.py
```

You can view the list of files in the Amazon S3 Management Console. In the Management Console, select **Refresh**.

Many synchronized files should now appear. The sync command only copies files that are not in the destination, or any files that have changed since the last time sync was run. This makes it easy to perform an incremental backup to Amazon S3.

![S3 List](pictures/s3list.png)

---

## Task 4: Automate EBS Snapshots

### Create an EBS Snapshot in the Management Console


![EBS Volume](pictures/ebs-volume.png)
![Snapshot](pictures/snapshoot.png)

### Create an EBS Snapshot with the AWS CLI

Type the following command in your Session manager terminal, replacing `YOUR-VOLUME-ID` with the Volume ID you just copied:

```bash
aws ec2 create-snapshot --description CLI --volume-id YOUR-VOLUME-ID
```

**Example Output:**

```json
[ec2-user@ip-10-1-11-8 ~]$ aws ec2 create-snapshot --description CLI --volume-id vol-057b7afc598750219
{
    "Tags": [],
    "SnapshotId": "snap-0f91051992066f8f2",
    "VolumeId": "vol-057b7afc598750219",
    "State": "pending",
    "StartTime": "2026-01-01T17:37:33.426000+00:00",
    "Progress": "",
    "OwnerId": "675866705092",
    "Description": "CLI",
    "VolumeSize": 20,
    "Encrypted": false
}
```

### Create an EBS Snapshot Programmatically

**Script: snapshotter.py**

```python
#!/usr/bin/env python3
import boto3
import datetime

MAX_SNAPSHOTS = 2   # Number of snapshots to keep

# Connect to the Amazon EC2 service
ec2 = boto3.resource('ec2')

# Loop through each volume
for volume in ec2.volumes.all():
    # Create a snapshot of the volume with the current time as a Description
    new_snapshot = volume.create_snapshot(Description = str(datetime.datetime.now()))
    print ("Created snapshot " + new_snapshot.id)
    
    # Too many snapshots?
    snapshots = list(volume.snapshots.all())
    if len(snapshots) > MAX_SNAPSHOTS:
        # Delete oldest snapshots, but keep MAX_SNAPSHOTS available
        snapshots_sorted = sorted([(s, s.start_time) for s in snapshots], key=lambda k: k[1])
        for snapshot in snapshots_sorted[:-MAX_SNAPSHOTS]:
            print ("Deleted snapshot " + snapshot[0].id)
            snapshot[0].delete()
```

**The script does the following:**
- Connects to the Amazon EC2 service
- Goes through list of all EBS volumes and for each volume:
  - Creates a new snapshot
  - Obtains a list of snapshots for that volume
  - Deletes the oldest snapshots, leaving the two most recent snapshots

Run the script by typing the following command:

```bash
./snapshotter.py
```

**First Execution Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ ./snapshotter.py
/usr/local/lib/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
Created snapshot snap-07acc0710d98d583a
Deleted snapshot snap-08b3dcf733e625e76
Created snapshot snap-0bc5e47d47581fd5a
```

You will see two 20 GiB snapshots of the Test Instance and one 8 GiB snapshot of the CLI instance.

### Check Snapshot Rotation

Check that it is rotating correctly:
- Make a mental note of the snapshots displayed
- Run the snapshotter.py command again

 ![Snapshot 2](pictures/snapshoo2.png)


Once executed `./snapshotter.py` command again you will see the new snapshot will be created.

**Second Execution Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ ./snapshotter.py
/usr/local/lib/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
Created snapshot snap-0f1543f2a98b0a7e9
Deleted snapshot snap-0f91051992066f8f2
Created snapshot snap-0dfc7bc4d16de5327
```

### Question & Answer

**Question:** Why were the 20 GiB and 8 GiB snapshots started at the same time?

**Answer:** Because the automation script iterates over all EBS volumes attached to the EC2 instance and calls the CreateSnapshot API for each volume in the same execution flow. AWS processes these snapshot requests independently and asynchronously, so when the script is triggered, snapshot creation for both the 20 GiB and 8 GiB volumes is initiated almost simultaneously, even though they may complete at different times.

![Volume 2](pictures/volume2.png)


---

## Task 5: Control Amazon EC2 Instances with The Stopinator!

**Script: stopinator.py**

```python
#!/usr/bin/env python3

import boto3

# Connect to the Amazon EC2 service
ec2 = boto3.resource('ec2')

# Loop through each instance
for instance in ec2.instances.all():
    state = instance.state['Name']
    for tag in instance.tags:
        # Check for the 'stopinator' tag
        if tag['Key'] == 'stopinator':
            action = tag['Value'].lower()
            
            # Stop?
            if action == 'stop' and state == 'running':
                print ("Stopping instance", instance.id)
                instance.stop()
            
            # Terminate?
            elif action == 'terminate' and state != 'terminated':
                print ("Terminating instance", instance.id)
                instance.terminate()
```

**The script does the following:**
- Connects to the Amazon EC2 service
- Obtains a list of all EC2 instances
- Loops through each instance
- If an instance is in the running state and has a tag named `stopinator`, it reads the value of the tag and then either stops or terminates the instance

### First Execution

```bash
./stopinator.py
```

**Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ ./stopinator.py
/usr/local/lib/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
```

Stopinator didn't stop the instance because it only targets running EC2 instances with the `stopinator` tag; once you add `stopinator=stop` (or if the tag already exists), the script will stop the instance.

### Second Execution (After Adding Tag)

Run the `./stopinator.py` script again then you will see that instance will be stopped.

**Output:**

```
[ec2-user@ip-10-1-11-8 ~]$ ./stopinator.py
/usr/local/lib/python3.9/site-packages/boto3/compat.py:89: PythonDeprecationWarning: Boto3 will no longer support Python 3.9 starting April 29, 2026. To continue receiving service updates, bug fixes, and security updates please upgrade to Python 3.10 or later. More information can be found here: https://aws.amazon.com/blogs/developer/python-support-policy-updates-for-aws-sdks-and-tools/
  warnings.warn(warning, PythonDeprecationWarning)
Stopping instance i-0997c32df2b9f109e
```
![Stopinator Tag](pictures/stopinator-tag.png)



### Important Note

**Stopinator is just an idea for automating EC2 cost control.** You can schedule it to run every evening to stop instances and save money, and optionally run another script in the morning to start them again. 

To avoid stopping the wrong machines, use tags to control behavior:
- Stop only instances that are explicitly tagged
- Keep tagged "important" instances running and stop the rest
- Add a tag like "max-hours" and run Stopinator hourly to terminate instances that have been running longer than the allowed time (useful for labs and experiments)

---

## Task 6: Custom CloudWatch Metrics

### Sending Metrics via the AWS CLI

**Script: highlow.py**

```python
#!/usr/bin/env python3
import boto3
import datetime

# Connect to CloudWatch
cloudwatch = boto3.client('cloudwatch')

# Generate random number
import random
value = random.randint(1, 100)

# Send the metric
cloudwatch.put_metric_data(
    Namespace='Custom',
    MetricData=[
        {
            'MetricName': 'HighLow',
            'Value': value,
            'Timestamp': datetime.datetime.utcnow()
        }
    ]
)

print(f"Sent metric value: {value}")
```

---

## Task 7: Security Credentials for your Scripts

When you run scripts that interact with AWS services, they need credentials to authenticate. EC2 instances can use IAM roles to automatically provide temporary credentials.

### View Security Credentials

```bash
./show-credentials
```

**Example Output:**

```
[ec2-user@ip-10-1-11-167 ~]$ ./show-credentials
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    56  100    56    0     0  39270      0 --:--:-- --:--:-- --:--:-- 56000
*   Trying 169.254.169.254:80...
* Connected to 169.254.169.254 (169.254.169.254) port 80...
> GET /latest/meta-data/iam/security-credentials/<REDACTED_ROLE_NAME> HTTP/1.1
> Host: 169.254.169.254

{
  "Code": "Success",
  "Type": "AWS-HMAC",
  "AccessKeyId": "ASIA****************",
  "SecretAccessKey": "******************************",
  "Token": "******************************",
  "Expiration": "REDACTED"
}
```

The instance metadata service (169.254.169.254) provides temporary security credentials that are automatically rotated by AWS. This is the secure way to provide credentials to applications running on EC2 instances.

---

## Summary

In this lab, you learned how to:

1. **Connect to EC2 instances** using AWS Systems Manager Session Manager
2. **Use AWS CLI** to create key pairs, manage S3 buckets, and create EBS snapshots
3. **Write Python scripts** using boto3 to automate AWS tasks
4. **Create automated backup scripts** for EBS volumes with snapshot rotation
5. **Control EC2 instances** programmatically using tags
6. **Send custom CloudWatch metrics** from your applications
7. **Understand IAM roles** and how EC2 instances receive temporary credentials

These automation techniques can save time, reduce errors, and enable sophisticated cost control and operational workflows in your AWS environment.

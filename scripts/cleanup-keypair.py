#!/usr/bin/env python3
import boto3
import datetime

MAX_SNAPSHOTS = 2  # Number of snapshots to keep

# Connect to the Amazon EC2 service
ec2 = boto3.resource('ec2')

# Loop through each volume
for volume in ec2.volumes.all():
    # Create a snapshot of the volume with the current time as a Description
    new_snapshot = volume.create_snapshot(Description=str(datetime.datetime.now()))
    print("Created snapshot " + new_snapshot.id)

    # Too many snapshots?
    snapshots = list(volume.snapshots.all())
    if len(snapshots) > MAX_SNAPSHOTS:
        # Delete oldest snapshots, but keep MAX_SNAPSHOTS available
        snapshots_sorted = sorted([(s, s.start_time) for s in snapshots], key=lambda k: k[1])
        for snapshot in snapshots_sorted[:-MAX_SNAPSHOTS]:
            print("Deleted snapshot " + snapshot[0].id)
            snapshot[0].delete()
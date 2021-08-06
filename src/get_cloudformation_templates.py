import collections
import json
import os
import time
import types

import boto3


def get_cloudformation_templates():
    cloudformation_client = boto3.client('cloudformation', region_name='us-east-1')

    
    deleted_stacks = cloudformation_client.list_stacks(StackStatusFilter=['DELETE_COMPLETE']).get('StackSummaries')
    for stack in deleted_stacks:
        stack_info = cloudformation_client.describe_stacks(StackName=stack['StackId']).get('Stacks')
        for info in stack_info:
                template = cloudformation_client.get_template(StackName=stack['StackId'],TemplateStage='Original').get('TemplateBody')
                if isinstance(template, collections.OrderedDict):
                    os.makedirs(os.path.dirname('templates/'+time.strftime('%Y%m%d')+'/'+stack['StackName']+'.json'), exist_ok=True)
                    with open('templates/'+time.strftime('%Y%m%d')+'/'+stack['StackName']+'.json', 'w') as file:
                        file.write(json.dumps(template, indent=4))
                elif isinstance(template, str):
                    os.makedirs(os.path.dirname('templates/'+time.strftime('%Y%m%d')+'/'+stack['StackName']+'.yaml'), exist_ok=True)
                    with open('templates/'+time.strftime('%Y%m%d')+'/'+stack['StackName']+'.yaml', 'w') as file:
                        file.write(template)

if __name__ == "__main__":
    get_cloudformation_templates()

import json

def lambda_handler(event, context):
    # TODO implement
        print("Lambda Test")
        if event['number'] == 'One':
            return 'it is number'   
        elif event['number'] == 'word':
            return 'not number'
        elif event['code'] == 'code':
            return 'code'
        else:
            return 'special character'
        
        
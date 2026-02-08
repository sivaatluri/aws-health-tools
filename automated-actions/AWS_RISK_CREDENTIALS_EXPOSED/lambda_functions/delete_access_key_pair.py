import boto3

iam = boto3.client('iam')


def lambda_handler(event, context):
    account_id = event['account']
    time_discovered = event['time']
    details = event['detail']
    access_key_id = details['affectedEntities'][0]['entityValue']
    print('Looking up username for access key pair...')
    username = get_username_from_key(access_key_id)
    print('Deactivating exposed access key pair...')
    deactivate_exposed_key_pair(username, access_key_id)
    return {
        "account_id": account_id,
        "time_discovered": time_discovered,
        "username": username,
        "deactivated_key": access_key_id
    }


def get_username_from_key(access_key_id):
    """ Retrieves username last associated with specified IAM access key ID.

    Args:
        access_key_id (string): IAM access key ID to lookup user with.

    Returns:
        (string)
        Username last associated with specified IAM access key ID.

    """
    try:
        response = iam.get_access_key_last_used(
            AccessKeyId=access_key_id
        )
    except Exception as e:
        print(e)
        print('Unable to retrieve username for access key "{}".'.format(access_key_id))
        raise(e)
    return response['UserName']


def deactivate_exposed_key_pair(username, access_key_id):
    """ Deactivates IAM access key pair identified by access key ID for specified user.

    Args:
        username (string): Username of IAM user to deactivate key pair for.
        access_key_id (string): IAM access key ID to identify key pair to deactivate.

    Returns:
        (None)

    """
    try:
        iam.update_access_key(
            UserName=username,
            AccessKeyId=access_key_id,
            Status='Inactive'
        )
    except Exception as e:
        print(e)
        print('Unable to deactivate access key "{}" for user "{}".'.format(access_key_id, username))
        raise(e)

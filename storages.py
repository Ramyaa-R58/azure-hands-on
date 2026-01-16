from azure.core.exceptions import ResourceNotFoundError
from azure.identity import ClientSecretCredential, DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from settings import *
from azure.mgmt.storage import StorageManagementClient
from azure.storage.blob import BlobClient
from azure.storage.fileshare import ShareServiceClient
from azure.storage.queue import QueueClient
from azure.data.tables import TableServiceClient

credential = DefaultAzureCredential()
def resource_groups():

    resource_client = ResourceManagementClient(credential,AZURE_SUBSCRIPTION_ID)

    #to create / update RG
    resource_client.resource_groups.create_or_update('new_resource_grp',{
        'location':'eastus'
    })
    # to list all RG
    resource_list = resource_client.resource_groups.list()
    for resource in resource_list:
        print("resource-group-name:",resource.name)

    # to get particular resource group
    resource_result = resource_client.resource_groups.get('new_resource_grp')
    print("resource name",resource_result.name)

    # to delete a RG
    # delete_result = resource_client.resource_groups.begin_delete('new_resource_grp')
    # # to create / update RG
    # resource_client.resource_groups.create_or_update('new_resource_grp', {
    #     'location': 'eastus'
    # })
def storage_account():
    storage_client = StorageManagementClient(credential,AZURE_SUBSCRIPTION_ID)
    # to check available name for storage accounts
    # check = storage_client.storage_accounts.check_name_availability({'name':'new_storage_account'})
    # if not check.name_available:
    storage_client.storage_accounts.begin_create('new_resource_grp',STORAGE_ACCOUNT,{
                                                 'location':'eastus',
        'sku':{'name':'Standard_LRS'},
        'kind':'StorageV2'
    })
def blob_storage(file_name:str,dest_file_name:str,file_obj):
    storage_client = StorageManagementClient(credential,AZURE_SUBSCRIPTION_ID)

    account_url = f"https://{STORAGE_ACCOUNT}.blob.core.windows.net/"
    storage_client.blob_containers.create('new_resource_grp',STORAGE_ACCOUNT,'newcontainer',{})
    # to create a blob file
    blob_client = BlobClient(account_url,'newcontainer',file_name,credential=credential)


    blob_client.upload_blob(file_obj,overwrite=True)
    with open(dest_file_name,'wb') as data:
        stream = blob_client.download_blob()
        for data_chunk in stream.chunks():
            data.write(data_chunk)


def share_storage(file_name:str,destination_file_name:str,file_obj):
    storage_client = StorageManagementClient(credential,AZURE_SUBSCRIPTION_ID)

    account_endpoint = f"https://{STORAGE_ACCOUNT}.file.core.windows.net/"


    share_client = ShareServiceClient(account_endpoint,credential=STORAGE_ACCESS_KEY)
    share_name = 'newshare'
    share = share_client.get_share_client('newshare')
    shares = share_client.list_shares()

    if not any(s.name == share_name for s in shares):
        share_client.create_share('newshare')


    # to create a directory
    #
    dir_client = share.get_directory_client('newdir')
    if not dir_client.exists():
        share.create_directory('newdir')

    # file_client = share.get_file_client('new_file_share.txt')
    file_client = dir_client.get_file_client(file_name)



    file_client.upload_file(file_obj)
    with open(destination_file_name,'wb') as data:
        stream = file_client.download_file()
        for chunk in stream.chunks():
            data.write(chunk)
    #file_client.delete_file()
    #share.delete_share()

def queue_storage(messages:list=None):
    queue_client = QueueClient(account_url=f'https://{STORAGE_ACCOUNT}.queue.core.windows.net',queue_name='newqueue',credential=credential)
    try:
        # Try to get properties — fails if queue doesn't exist
        queue_client.get_queue_properties()
        print("Queue exists.")
    except ResourceNotFoundError:
        queue_client.create_queue()
        print("Queue created.")
    for message in messages:
        queue_client.send_message(message)
    # queue_client.peek_messages()
    msg = queue_client.receive_messages()

    # for message in msg:
    #     queue_client.update_message(message.id,message.pop_receipt,'new content updated')
    #     print("message id:",message.id)
    #     print("message content:",message.content)
        # queue_client.delete_message(message)

def table_storage(entity_messages:list=None):
    table_service_client = TableServiceClient.from_connection_string(CONN_STRING)
    table_name = 'newtable'
    table_client = table_service_client.get_table_client('newtable')
    tables = table_service_client.list_tables()
    if not any(t.name == table_name for t in tables):
        table_service_client.create_table('newtable')
    for entity in entity_messages:
        entity = {
            "PartitionKey": entity.partition_key,
            "RowKey": entity.row_key,
            "Name": entity.name,
            "Age": entity.age
        }

        table_client.create_entity(entity)

    result = table_client.list_entities()
    print(result)
    query_params = {
        'name':'Ramyaa'
    }
    query_filter = 'Name eq @name'
    result = table_client.query_entities(query_filter=query_filter, parameters=query_params)
    print(result)
    tables = table_service_client.list_tables()

    # to delete entity
    # table_client.delete_entity('001','001')



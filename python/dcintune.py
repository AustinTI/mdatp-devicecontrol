import asyncio
import configparser
import os
import base64
from msgraph_beta.generated.models.o_data_errors.o_data_error import ODataError
from dcgraph import Graph
import plistlib

async def main():
    
    # Load settings
    config = configparser.ConfigParser()

    config_file_path = os.path.join(os.path.dirname(__file__), "config.cfg")  
    config.read(config_file_path)
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    await greet_user(graph)

    choice = -1

    while choice != 0:
        print('Please choose one of the following options:')
        print('0. Exit')
        print('1. Display access token')
        print('2. List my inbox')
        print('3. Send mail')
        print('4. Make a Graph call')

        try:
            choice = int(input())
        except ValueError:
            choice = -1

        try:
            if choice == 0:
                print('Goodbye...')
            elif choice == 1:
                await display_access_token(graph)
            elif choice == 2:
                await list_inbox(graph)
            elif choice == 3:
                await send_mail(graph)
            elif choice == 4:
                await make_graph_call(graph)
            else:
                print('Invalid choice!\n')
        except ODataError as odata_error:
            print('Error:')
            if odata_error.error:
                print(odata_error.error.code, odata_error.error.message)



async def greet_user(graph: Graph):
    user = await graph.get_user()
    if user:
        print('Hello,', user.display_name)
        # For Work/school accounts, email is in mail property
        # Personal accounts, email is in userPrincipalName
        print('Email:', user.mail or user.user_principal_name, '\n')

async def display_access_token(graph: Graph):
    token = await graph.get_user_token()
    print('User token:', token, '\n')

async def list_inbox(graph: Graph):
    # TODO
    return

async def send_mail(graph: Graph):
    # TODO
    return

async def make_graph_call(graph: Graph):
    configs = await graph.make_graph_call()
    for device_config in configs.value:
        if device_config.odata_type == "#microsoft.graph.macOSCustomConfiguration":
            payload_bytes = device_config.payload
            payload = base64.b64decode(payload_bytes)
            plist = plistlib.loads(payload,fmt=plistlib.FMT_XML)
            if 'deviceControl' in plist['PayloadContent'][0]:
                deviceControl = plist['PayloadContent'][0]['deviceControl']
                print(deviceControl)

                id = device_config.id

                assignments = await graph.get_assignments(id)



# Run main
asyncio.run(main())
import os
from datetime import datetime
from pprint import pprint
from dotenv import load_dotenv
from royal_mail_address import AddressFindRequestDef, ApiClient, ApiException, Configuration, DefaultApi


def main() -> None:
    load_dotenv(r"C:\prdev\envs\amdev\rm_play.env")
    configuration = Configuration(
        # host = "https://api.royalmail.net/addressfind/v1"
    )
    client_id = os.environ["ROYAL_MAIL_CLIENT_ID"].strip()
    client_secret = os.environ["ROYAL_MAIL_CLIENT_SECRET"].strip()
    configuration.api_key["Client-Id"] = client_id
    configuration.api_key["Client-Secret"] = client_secret
    x_rmg_date_time = datetime.now().astimezone().isoformat(timespec="seconds")
    print(f"Using x_rmg_date_time: {x_rmg_date_time}")

    with ApiClient(configuration) as api_client:
        api_instance = DefaultApi(api_client)
        # x_rmg_date_time = date.today()
        address_text = 'Sycamore Grove, Bracebridge Heath, Lincoln'
        address_find_request = AddressFindRequestDef(
            address_text=address_text,
        )

        try:
            api_response = api_instance.address_find(x_rmg_date_time, address_find_request)
            print("The response of DefaultApi->address_find:\n")
            for address in api_response.addresses:
                pprint(address.model_dump())
                print(f'WE FOUND AN {address.type}')
        except ApiException as e:
            print("Exception when calling DefaultApi->address_find: %s\n" % e)


if __name__ == '__main__':
    main()

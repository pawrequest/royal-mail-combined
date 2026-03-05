from royal_mail_combined.apis.parcels_apis.client import ParcelAPIClient
from royal_mail_combined.apis.click_and_drop.client import ClickAndDropClient
from royal_mail_combined.config import RoyalMailSettingsGlobal
from royal_mail_combined.apis.returns.models import ReturnsRequest, ReturnsResponse, AvailableServicesResponse
from royal_mail_combined.core.endpoints import RETURNS_ENDPOINT, RETURNS_SERVICES_ENDPOINT
from royal_mail_combined.core.http_client import RMBaseClient


class RoyalMailClient:
    def __init__(self, settings: RoyalMailSettingsGlobal):
        self.settings = settings
        self.http_client = RMBaseClient(settings=settings)
        self.click_and_drop = ClickAndDropClient(settings=settings)
        self.parcel_api = ParcelAPIClient(settings=settings)

    # ORDERS
    def create_return_shipment_order(self, return_request: ReturnsRequest) -> ReturnsResponse:
        res = self.http_client.do_post(
            url=RETURNS_ENDPOINT, data=return_request, headers=self.settings.headers_bearer()
        )
        res_model = ReturnsResponse.model_validate(res.json())
        return res_model

    # ORDERS
    def check_return_services(self) -> AvailableServicesResponse:
        res = self.http_client.do_get(url=RETURNS_SERVICES_ENDPOINT, headers=self.settings.headers_bearer())
        res_model = AvailableServicesResponse.model_validate(res.json())
        return res_model

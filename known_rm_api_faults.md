| name                     | endpoint | expected                                                                                | actual       | fix                                     | 
|--------------------------|----------|-----------------------------------------------------------------------------------------|--------------|-----------------------------------------|
| Collection Create Status |          | status = 201                                                                            | status = 200 | manually edit response_type_map         |
| Return Service Name      |          | service.name from returns/Available services should match CollectionCreate requirements |              | use hardcoded values from email support |

# Collection Create Status

docs say success status code is 201, but in reality it is 200
manually edited response map

# Return Service Name

service.name from returns/Available services should match CollectionCreate requirements, but it does not.

# labels

no number of parcels
no date

# no rate-limit info in headers from AddressSearch endpoint

# AddressRecordDef returned from retrieve address with > 30 chars in company name

# package formats other than 'parcel' do not work
API says i sent SmallParcel PascalCase but i sent 'smallParcel' camelcase

(Order reference "ISP School" failed, errors=[
Error in ['Field=PostageDetails.ServiceCode: Value=TPN24', 'Field=Packages.PackageFormatIdentifier: Value=SmallParcel']: 33 -
Package size 'SmallParcel' is not valid for the service 'TPN24'.])) Reason: None


``` json
'failed_orders': [   {   'errors': [   {   'error_code': 33,
                                              'error_message': "Package size 'SmallParcel' is not valid for the "
                                                               "service 'TPN24'.",
                                              'fields': [   {   'field_name': 'PostageDetails.ServiceCode',
                                                                'value': 'TPN24'},
                                                            {   'field_name': 'Packages.PackageFormatIdentifier',
                                                                'value': 'SmallParcel'}]}],
                            'order': {   'billing': {   'address': {   'address_line1': '70 Kingsgate Road',
                                                                       'address_line2': 'Kilburn',
                                                                       'address_line3': '',
                                                                       'city': 'London',
                                                                       'company_name': 'Amherst Radio Centre',
                                                                       'country_code': 'GB',
                                                                       'county': None,
                                                                       'full_name': 'Giles Toman',
                                                                       'postcode': 'NW6 4TE'},
                                                        'email_address': 'radios@amherst.co.uk',
                                                        'phone_number': '07973147257'},
                                         'contains_dangerous_goods': False,
                                         'currency_code': None,
                                         'customs_duty_costs': None,
                                         'dangerous_goods_description': None,
                                         'dangerous_goods_quantity': None,
                                         'dangerous_goods_un_code': None,
                                         'importer': None,
                                         'is_recipient_a_business': None,
                                         'label': None,
                                         'order_date': datetime.datetime(2026, 3, 31, 0, 0),
                                         'order_reference': 'ISP School',
                                         'order_tax': None,
                                         'other_costs': 0.0,
                                         'packages': [   {   'contents': [],
                                                             'custom_package_format_identifier': None,
                                                             'dimensions': None,
                                                             'package_format_identifier': 'smallParcel',
                                                             'weight_in_grams': 2000}],
                                         'planned_despatch_date': datetime.datetime(2026, 3, 31, 0, 0),
                                         'postage_details': {   'air_number': None,
                                                                'carrier_name': None,
                                                                'commercial_invoice_date': None,
                                                                'commercial_invoice_number': None,
                                                                'consequential_loss': None,
                                                                'department': None,
                                                                'guaranteed_saturday_delivery': None,
                                                                'ioss_number': None,
                                                                'is_local_collect': None,
                                                                'receive_email_notification': True,
                                                                'receive_sms_notification': True,
                                                                'recipient_eori_number': None,
                                                                'request_signature_upon_delivery': None,
                                                                'requires_export_license': None,
                                                                'safe_place': None,
                                                                'send_notifications_to': 'recipient',
                                                                'service_code': 'TPN24',
                                                                'service_register_code': None},
                                         'recipient': {   'address': {   'address_line1': 'Castlewood Farm',
                                                                         'address_line2': '3 Conyer Road',
                                                                         'address_line3': '',
                                                                         'city': 'Teynham',
                                                                         'company_name': 'ISP School',
                                                                         'country_code': 'GB',
                                                                         'county': None,
                                                                         'full_name': 'Kerry Edwards',
                                                                         'postcode': 'ME9 9EA'},
                                                          'address_book_reference': None,
                                                          'email_address': 'Kerry.Edwards@ispschools.org.uk',
                                                          'phone_number': '01795523900'},
                                         'sender': None,
                                         'shipping_cost_charged': 0.0,
                                         'special_instructions': None,
                                         'subtotal': 0.0,
                                         'tags': [],
                                         'total': 0.0}}],
   'success_count': 0} | "C:\prdev\amdev\royal-mail-combined\src\royal_mail_combined\click_and_drop_api\client.py:52"
[   'Order reference "ISP School" failed, errors=[Error in [\'Field=PostageDetails.ServiceCode: Value=TPN24\', '
   "'Field=Packages.PackageFormatIdentifier: Value=SmallParcel']: 33 - Package size 'SmallParcel' is not valid for "
   "the service 'TPN24'.])"]
```
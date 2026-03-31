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

```json
{
  "created_orders": [],
  "errors_count": 1,
  "failed_orders": [
    {
      "errors": [
        {
          "error_code": 33,
          "error_message": "Package size 'SmallParcel' is not valid for the service 'TPN24'.",
          "fields": [
            {
              "field_name": "PostageDetails.ServiceCode",
              "value": "TPN24"
            },
            {
              "field_name": "Packages.PackageFormatIdentifier",
              "value": "SmallParcel"
            }
          ]
        }
      ],
      "order": {
        "billing": {
          "address": {
            "address_line1": "70 Kingsgate Road",
            "address_line2": "Kilburn",
            "address_line3": "",
            "city": "London",
            "company_name": "Amherst Radio Centre",
            "country_code": "GB",
            "county": null,
            "full_name": "Giles Toman",
            "postcode": "NW6 4TE"
          },
          "email_address": "radios@amherst.co.uk",
          "phone_number": "07973147257"
        },
        "contains_dangerous_goods": false,
        "currency_code": null,
        "customs_duty_costs": null,
        "dangerous_goods_description": null,
        "dangerous_goods_quantity": null,
        "dangerous_goods_un_code": null,
        "importer": null,
        "is_recipient_a_business": null,
        "label": null,
        "order_date": "2026-04-04T00:00:00",
        "order_reference": "Test Reference",
        "order_tax": null,
        "other_costs": 0.0,
        "packages": [
          {
            "contents": [],
            "custom_package_format_identifier": null,
            "dimensions": null,
            "package_format_identifier": "smallParcel",
            "weight_in_grams": 2000
          }
        ],
        "planned_despatch_date": "2026-04-04T00:00:00",
        "postage_details": {
          "air_number": null,
          "carrier_name": null,
          "commercial_invoice_date": null,
          "commercial_invoice_number": null,
          "consequential_loss": null,
          "department": null,
          "guaranteed_saturday_delivery": null,
          "ioss_number": null,
          "is_local_collect": null,
          "receive_email_notification": true,
          "receive_sms_notification": true,
          "recipient_eori_number": null,
          "request_signature_upon_delivery": null,
          "requires_export_license": null,
          "safe_place": null,
          "send_notifications_to": "recipient",
          "service_code": "TPN24",
          "service_register_code": null
        },
        "recipient": {
          "address": {
            "address_line1": "25 Bennet Close",
            "address_line2": "",
            "address_line3": "",
            "city": "Welling",
            "company_name": "Test Company",
            "country_code": "GB",
            "county": null,
            "full_name": "Test Contact name",
            "postcode": "DA16 3HU"
          },
          "address_book_reference": null,
          "email_address": "sdgsdg@sdgsdg.com",
          "phone_number": "07666666666"
        },
        "sender": null,
        "shipping_cost_charged": 0.0,
        "special_instructions": null,
        "subtotal": 0.0,
        "tags": [],
        "total": 0.0
      }
    }
  ],
  "success_count": 0
}


```
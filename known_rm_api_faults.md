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
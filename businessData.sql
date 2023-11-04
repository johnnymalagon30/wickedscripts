select o."name" as "Business_Name",
o.config -> 'info' -> 'orgWebsiteUrl' as "Corporate_Website",
o.config -> 'info' -> 'address' as "Business_Addr1",
o.config -> 'info' -> 'addressLine2' as "Business_Addr2",
o.config -> 'info' -> 'city' as "City",
o.config -> 'info' -> 'state' as "State",
o.config -> 'info' -> 'zipCode' as "Zip",
SPLIT_PART(cast(o.config -> 'info' -> 'contactName' as varchar),' ',1) as "Business_Contact_First_Name",
regexp_replace(cast(o.config -> 'info' -> 'contactName' as varchar),'^.* ','') as "Business_Contact_Last_Name",
o.config -> 'info' -> 'contactEmail' as "Business_Contact_Email",
o.config -> 'info' -> 'contactNumber' as "Business_Contact_Phone_Number",
o.config -> 'smsNumber' as "Assigned TFN"
from "BandwidthVerificationRequests" b
join "Organizations" o on cast(o.config ->> 'smsNumber'  as varchar) = cast(b."phone" as varchar)
where b."bandwidthStatus" = 'UNVERIFIED'
and o."id" not in (
SELECT o."id" from "Organizations" o
where "config"::text iLIKE any (array['%"smsNumber": %1800%', '%"smsNumber": %1888%', '%"smsNumber": %1877%','%"smsNumber": %1866%','%"smsNumber": %1855%','%"smsNumber": %1844%','%"smsNumber": %1833%']))

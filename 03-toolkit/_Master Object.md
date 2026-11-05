#### Main Dimensions + Taxonomy
#datasource/cc9
#datasource/ofi


#employee
#employee/user -- an employee may have multiple user (logins)
#employee/job_title

#location -- cost center then location
#location/clinic -- rolls up (Team ↑ Region ↑ Division)


#date
#date/iso_week
#date/business_enrichment
#patient -- from patient, contract, transaction
#patient/patient_status
#patient/referral

#taxonomy/patient_status
#taxonomy/appointment_type
#taxonomy/appointment_status
#taxonomy/transaction_type
#taxonomy/transaction_type/contract_type
#taxonomy/transaction_type/contract_type/rollup -- #txplangroup
#taxonomy/transaction_type/add_on_type

#scd2/snapshots/patient_status
#scd2/snapshots/patient_employee
#scd2/snapshots/patient_location
every taxonomy needs an scd2

#### Facts
#appointment
#apppointment/create -- includes created_by (app vs emp)
#appointment/occurence

#appointment/is_npe vs #appointment/is_clinical
#appointment/is_npc

#appointment/scheduled_day_prior
#appointment/dismissed_after_5days

#appointment/show_up_rate = #appointment/dismissed_after_5days / #appointment/scheduled_day_prior 
- conversion
- win-back vs re-capture

#contract
#contract/contract_start
#contract/contract_start_not_ph1 -- exclude ph1 identified
#contract/contract_sds

#contract/add_on -- diff for cc9 vs ofi
#contract/discount
#contract/payment_plan


#appointment/outcome -- until 5 days after #appointment 
#patient/prospect_status -- new concept

#### Facts2
#financial/invoice -- if it has a due date
#financial/accounts_receivable


### Important History Tables
[[Patient Status History - Start Needed - By EOM]]

# Measure
#measure/npe/added
#measure/npe/dismissed
#measure/npe/slots_fill_rate

#measure/contract_start/count
#measure/contract_start/discount_amount

#measure/net_production 

#metric/conversion_rate
#metric/show_up_rate
#metric/average_contract_value
#metric/addon_attachment_rate/retainer_assurance
#metric/addon_attachment_rate/whitening
#metric/recapture_rate/start_needed
#metric/initial_investment_pct
# DataSources

#datasource/cc9/midatlantic_128
#datasource/cc9/mountainwest_129
#datasource/cc9/midwest_130
#datasource/cc9/gulfcoast_131
#datasource/cc9/southeast_132
#datasource/cc9/mideast_133
#datasource/cc9/northtexas_134
#datasource/cc9/southtexas_135
#datasource/cc9/spillers_136
#datasource/workday
#datasource/activedirectory
#datasource/dentalmonitoring
#datasource/aligntech
#datasource/easyrx
#datasource/swell
#datasource/equifax
#datasource/calls/momentum_g12
#datasource/calls/weave
#datasource/calls/talkdesk
#datasource/salesforce/marketing_instance
#datasource/salesforce/business_development
#datasource/salesforce/marketing_cloud
#datasource/ads/marketing_funnel
#datasource/ads/facebook_ad_insights
#datasource/ads/google_analytics_funnel_io
#datasource/ads/google_apis
#datasource/ads/podium
#datasource/ads/bing
#datasource/ads/cardinal
#datasource/ads/leadsigma

# Datasets
#datsets/kpi_golden_dataset -- no orthofi. legacy
#datasets/platinum_dataset -- no orthofi
#datasets/platinum_dataset_2 -- has orthofi ("PDS2.0")
# Semantic
#scd2/synonym_normalizer -- from a source and concept name
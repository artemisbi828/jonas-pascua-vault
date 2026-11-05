[[WH_DEV_Data_Solutions.gold.contract__sd]]
- patient_id__cc9 can be null -- b/c we don't have bridges
- does **NOT** have pre-conversion

[[WH_DEV_Data_Solutions.gold.patient__sd]]
- should never have **dangling** records. must be used in appointments or contracts.



# Overall Flow
1. pre-flight check
	1. model checks -- did I seed something and forget anything? 
		[[Quotables -- Data Architecture#^885909]] 
2. assert taxonomy -- direct
	1. #taxonomy/appointment-type 
	2. #taxonomy/appointment-status 
	3. #taxonomy/transaction-type -- txcode
	4. #employee 
	5. #location/clinic
3. stage tables -- #appointment ; #contract
	1. assert dimension integrity
	2. load-type
		1. incremental-via-watermark
		2. trunc-reload
			1. #taxonomy
4. enrich
	1. orphan patient_id__cc9 from **gold.contract__sd** and **gold.patient__sd**
	2. dangling patient_id from gold.patient__sd
5. load appointments
6. load contracts
	1. fill patient_id__cc9 for wherever we can find
		1. cross reference
		2. fill with proc
7. unify 
	1. gold -- #appointment, #contra 


---
# LEGACY


be agile!
- use mature tables (legacy state) as source --> scd2 tracking --> provided added value faster
- traverse-up-raw-source only if path is broken (undocumented, corrupted, inconsistent)
- slowly build raw source after
- 


staging pulls in **incrementals** | **get-all--trunc-reload**
- only the fields we need --> [1:M] scd2 components
staging [1:M] scd2 components


--- 


### procedures
1. data ops
   tables + columns -- insert only 
   ⚠️ replaced_by --> like end_date
	procs -- list the sources
	  includes -- manual-dev + dev-owner (0)
	
2. xchk for inserts
	scd2 for inserts 
		source proc -- can get sources from proc
		manual inserts

3. xchk for deletions --> scd2


### procedures--adhoc
1. orchestrator
	1. obsidian or json
		1. config thresholds: min, max, taxonomy, flags
	2. dev
		1. internal integrity checks --> if procs are clean with RN, should be no problem
	3. npc
		1. appointment-patient touches --> appt + ash
		2. appointment
		3. patient
		4. contract conversion
2. parts

### procedures--daily
#### prep
1. stage -- watermark incremental (or only **net-new-atomic-id**)
	1. **appointment__cc9**
	2. **contract__cc9**
	3. **transaction__cc9** --> **addon__cc9**
	4. other cc9
		1. **discount__cc9**
		2. **payment_length__cc9**
		3. **down_payment__cc9**
		4. **ar_collections__cc9**
	5. **contract__ofi**
	6. **patient__xref__ofi_cc9**
	7. **addon__ofi** <-- source.ofi__miscelllaneous_charges
2. stage -- dims
	1. union stack facts for patient_dim
		1. appointment__cc9, contract__cc9, transaction__cc9 --> staging.patient__cc9
	2. union stack dims
		1. contracts__ofi --> **staging.patient__ofi**
		2. lake.extenders.offices --> **staging.clinic__cc9**
		3. lake.sd.employees --> **staging.employee__wd**
		4. contracts__ofi --> **staging.clinic__ofi**
3. stage -- taxonomy
	1. staging.appointment_status__cc9
	2. staging.appointment_type__cc9
	3. staging.patient_status__cc9
	4. staging.addon__cc9
	5. staging.addon__ofi
	6. staging.job_title__lake_sd
4. snapshots -- patient_table
	1. staging.patient_status__cc9 (only guids in patient_dim) <-- source.patient
	2. staging.patient_tc <-- source.patient__cc9
	3. staging.patient_dr <-- source.patient__cc9 + source.transaction__cc9

#### scd2 + gold
1. stage --> scd2 (identified columns); ⚠️ inserts-only
	1. staging.patient__cc9 --> **scd2.patient__cc9**
	2. staging.patient__xref__ofi_cc9 --> **scd2.patient__ofi** (patGUID + other attributes)
	3. scd2.patient__cc9, scd2.patient__ofi --> gold.patient (cc9 base) --> **scd2.patient__sd**
	
	4. scd2.clinic__cc9 --> **scd2.clinic__sd**
	5. scd2.clinic__ofi --> **scd2.clinic__sd**
	6. scd2.employee__wd --> **scd2.employee__sd**
	7. 
2. scd2 --> unified raw
3. config --> calculated fields 
	1. appointment__create
	2. appointment__outcome (5 days)
	3. xref
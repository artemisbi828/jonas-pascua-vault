```sql
-- ============================================================================
-- NPE ADDED METRIC - SELF-CONTAINED VALIDATION QUERY
-- ============================================================================
-- Purpose: Standalone query with parametrized/temp tables
-- Output: Conforms to gold_fct_appointment_npe_added structure
-- No permanent table creation - uses temp tables for development/validation
-- ============================================================================

USE EDW;
GO

-- ============================================================================
-- PARAMETERS
-- ============================================================================
DECLARE @start_date DATE = '2026-06-04';
DECLARE @end_date DATE = DATEADD(DAY, 1, @start_date);
DECLARE @lookback_months INT = 6;
DECLARE @lookback_start_date DATE = DATEADD(MONTH, -@lookback_months, @start_date);

-- ============================================================================
-- LAYER 0: BRONZE SOURCE DATA (Temp Tables)
-- ============================================================================
-- Simulating raw source tables for development/testing

CREATE TABLE #bronze_appointments (
    source_system_id INT,
    appt_guid UNIQUEIDENTIFIER,
    pat_guid UNIQUEIDENTIFIER,
    apptttyp_guid UNIQUEIDENTIFIER,
    schdvw_guid UNIQUEIDENTIFIER,
    emp_guid UNIQUEIDENTIFIER,
    appt_datetime DATETIME2(3),
    appt_added_date DATE,
    appt_added_datetime DATETIME2(3),
    is_pre_conversion BIT,
    src_sys VARCHAR(50)
);

CREATE TABLE #bronze_appointment_types (
    source_system_id INT,
    apptttyp_guid UNIQUEIDENTIFIER,
    apptttyp_code VARCHAR(50),
    apptttyp_desc VARCHAR(255),
    is_npe BIT,
    npe_semantic_group VARCHAR(100),
    src_sys VARCHAR(50)
);

CREATE TABLE #bronze_appointment_status_history (
    source_system_id INT,
    appt_guid UNIQUEIDENTIFIER,
    status_code VARCHAR(50),
    status_changed_datetime DATETIME2(3),
    status_seq INT,
    src_sys VARCHAR(50)
);

CREATE TABLE #bronze_patients (
    source_system_id INT,
    pat_guid UNIQUEIDENTIFIER,
    patient_id VARCHAR(50),
    patient_name VARCHAR(200),
    date_of_birth DATE,
    src_sys VARCHAR(50)
);

CREATE TABLE #bronze_locations (
    source_system_id INT,
    schdvw_guid UNIQUEIDENTIFIER,
    location_id VARCHAR(50),
    location_code VARCHAR(50),
    location_name VARCHAR(255),
    src_sys VARCHAR(50)
);

-- ============================================================================
-- INSERT SAMPLE DATA FOR TESTING
-- ============================================================================

INSERT INTO #bronze_appointments (source_system_id, appt_guid, pat_guid, apptttyp_guid, schdvw_guid, emp_guid, appt_datetime, appt_added_date, appt_added_datetime, is_pre_conversion, src_sys)
VALUES
    (1, NEWID(), NEWID(), NEWID(), NEWID(), NEWID(), '2026-06-04 10:00:00', '2026-06-04', '2026-06-04 08:30:00', 0, 'CentralC9'),
    (1, NEWID(), NEWID(), NEWID(), NEWID(), NEWID(), '2026-06-04 14:00:00', '2026-06-04', '2026-06-04 08:45:00', 0, 'CentralC9'),
    (1, NEWID(), NEWID(), NEWID(), NEWID(), NEWID(), '2026-06-04 16:00:00', '2026-06-03', '2026-06-03 09:00:00', 0, 'CentralC9');

INSERT INTO #bronze_appointment_types (source_system_id, apptttyp_guid, apptttyp_code, apptttyp_desc, is_npe, npe_semantic_group, src_sys)
VALUES
    (1, NEWID(), 'NPE', 'New Patient Exam', 1, 'Initial', 'CentralC9'),
    (1, NEWID(), 'ADJ', 'Adjustment', 0, NULL, 'CentralC9');

INSERT INTO #bronze_patients (source_system_id, pat_guid, patient_id, patient_name, date_of_birth, src_sys)
VALUES
    (1, NEWID(), 'PAT001', 'John Doe', '1990-01-15', 'CentralC9'),
    (1, NEWID(), 'PAT002', 'Jane Smith', '1985-05-22', 'CentralC9');

INSERT INTO #bronze_locations (source_system_id, schdvw_guid, location_id, location_code, location_name, src_sys)
VALUES
    (1, NEWID(), 'LOC001', 'NYC-01', 'New York Clinic', 'CentralC9'),
    (1, NEWID(), 'LOC002', 'LA-01', 'Los Angeles Clinic', 'CentralC9');

-- ============================================================================
-- LAYER 1: SILVER TRANSFORMATIONS (CTEs with business logic)
-- ============================================================================

WITH silver_appointments_base AS (
    -- Deduplicate and add row numbers for filtering
    SELECT
        ba.source_system_id,
        ba.appt_guid,
        ba.pat_guid,
        ba.apptttyp_guid,
        ba.schdvw_guid,
        ba.emp_guid,
        ba.appt_datetime,
        ba.appt_added_date,
        ba.appt_added_datetime,
        ba.is_pre_conversion,
        ba.src_sys,
        ROW_NUMBER() OVER (PARTITION BY ba.source_system_id, ba.appt_guid ORDER BY ba.appt_added_datetime DESC) AS rn
    FROM #bronze_appointments ba
    WHERE ba.appt_added_datetime >= @start_date
      AND ba.appt_added_datetime < @end_date
),

silver_appointments AS (
    -- Get non-duplicated appointments for the period
    SELECT
        source_system_id,
        appt_guid,
        pat_guid,
        apptttyp_guid,
        schdvw_guid,
        emp_guid,
        appt_datetime,
        appt_added_date,
        appt_added_datetime,
        is_pre_conversion,
        src_sys
    FROM silver_appointments_base
    WHERE rn = 1
),

silver_appointment_status_history AS (
    -- Create SCD2-style ranges for status changes
    SELECT
        source_system_id,
        appt_guid,
        status_code,
        status_changed_datetime,
        LEAD(status_changed_datetime) OVER (PARTITION BY source_system_id, appt_guid ORDER BY status_changed_datetime) AS status_end_datetime,
        status_seq
    FROM #bronze_appointment_status_history
),

silver_patients AS (
    SELECT
        source_system_id,
        pat_guid,
        patient_id,
        patient_name,
        date_of_birth,
        src_sys
    FROM #bronze_patients
),

silver_locations AS (
    SELECT
        source_system_id,
        schdvw_guid,
        location_id,
        location_code,
        location_name,
        src_sys
    FROM #bronze_locations
),

silver_appointment_types AS (
    SELECT
        source_system_id,
        apptttyp_guid,
        apptttyp_code,
        apptttyp_desc,
        is_npe,
        npe_semantic_group,
        src_sys
    FROM #bronze_appointment_types
),

-- ============================================================================
-- LAYER 2: GOLD TRANSFORMATIONS (Business logic and surrogate keys)
-- ============================================================================

gold_appointments_with_surrogate_keys AS (
    -- Generate surrogate keys via hashing (parallel-pipeline pattern)
    SELECT
        CONVERT(BIGINT, HASHBYTES('SHA2_256', 
            CONVERT(VARCHAR(50), sa.source_system_id) + '|' + 
            CONVERT(VARCHAR(50), sp.patient_id))) AS patient_sk,
        
        CONVERT(BIGINT, HASHBYTES('SHA2_256', 
            CONVERT(VARCHAR(50), sl.source_system_id) + '|' + 
            CONVERT(VARCHAR(50), sl.location_id))) AS location_sk,
        
        CONVERT(BIGINT, HASHBYTES('SHA2_256', 
            CONVERT(VARCHAR(50), sat.source_system_id) + '|' + 
            CONVERT(VARCHAR(50), sat.apptttyp_code))) AS appointment_type_sk,
        
        CONVERT(BIGINT, HASHBYTES('SHA2_256', 
            CONVERT(VARCHAR(50), sa.source_system_id) + '|' + 
            CONVERT(VARCHAR(50), sa.appt_guid))) AS appointment_identity_sk,
        
        CONVERT(BIGINT, HASHBYTES('SHA2_256', 
            CONVERT(VARCHAR(50), sa.source_system_id) + '|' + 
            CONVERT(VARCHAR(50), sa.pat_guid) + '|' + 
            CONVERT(VARCHAR(50), sl.location_id) + '|' + 
            FORMAT(sa.appt_added_date, 'yyyy-MM-dd'))) AS npe_added_sk,
        
        sa.source_system_id,
        sa.appt_guid,
        sa.pat_guid,
        sa.appt_added_date,
        sa.appt_added_datetime,
        sa.appt_datetime,
        sat.is_npe,
        sat.npe_semantic_group,
        sl.location_id,
        sp.patient_id,
        sa.src_sys
    FROM silver_appointments sa
    INNER JOIN silver_patients sp 
        ON sp.source_system_id = sa.source_system_id 
       AND sp.pat_guid = sa.pat_guid
    INNER JOIN silver_locations sl 
        ON sl.source_system_id = sa.source_system_id 
       AND sl.schdvw_guid = sa.schdvw_guid
    INNER JOIN silver_appointment_types sat 
        ON sat.source_system_id = sa.source_system_id 
       AND sat.apptttyp_guid = sa.apptttyp_guid
),

npe_added_candidates AS (
    -- Filter to NPE appointments only
    SELECT
        *
    FROM gold_appointments_with_surrogate_keys
    WHERE is_npe = 1
),

previous_npe_check AS (
    -- Check for previous NPE within 6-month window (same patient, same location)
    SELECT
        nac.npe_added_sk,
        nac.patient_sk,
        nac.location_sk,
        nac.appointment_type_sk,
        nac.appointment_identity_sk,
        nac.appt_added_date,
        nac.appt_added_datetime,
        nac.appt_datetime,
        nac.source_system_id,
        nac.appt_guid,
        nac.pat_guid,
        nac.location_id,
        nac.patient_id,
        nac.src_sys,
        
        -- has_previous_npe: does this patient have another NPE at this location within lookback?
        CASE 
            WHEN EXISTS (
                SELECT 1
                FROM npe_added_candidates nac2
                WHERE nac2.patient_id = nac.patient_id
                  AND nac2.location_id = nac.location_id
                  AND nac2.appt_added_date < nac.appt_added_date
                  AND nac2.appt_added_date >= @lookback_start_date
            ) THEN 1
            ELSE 0
        END AS has_previous_npe_same_window
    FROM npe_added_candidates nac
),

same_day_cancel_check AS (
    -- Check for same-day cancellation
    SELECT
        pnc.*,
        CASE 
            WHEN EXISTS (
                SELECT 1
                FROM silver_appointment_status_history sash
                WHERE sash.source_system_id = pnc.source_system_id
                  AND sash.appt_guid = pnc.appt_guid
                  AND sash.status_code IN ('CANCELLED', 'CANCEL')
                  AND CAST(sash.status_changed_datetime AS DATE) = pnc.appt_added_date
            ) THEN 1
            ELSE 0
        END AS same_day_cancel_flag
    FROM previous_npe_check pnc
),

gold_fct_appointment_npe_added_final AS (
    -- Determine if this is a net-new NPE (no prior + not cancelled same day)
    SELECT
        npe_added_sk,
        appointment_identity_sk,
        patient_sk,
        location_sk,
        appointment_type_sk,
        CASE 
            WHEN has_previous_npe_same_window = 0 AND same_day_cancel_flag = 0 THEN 1
            ELSE 0
        END AS is_net_new,
        has_previous_npe_same_window,
        same_day_cancel_flag,
        appt_added_date,
        appt_added_datetime,
        appt_datetime,
        source_system_id,
        patient_id AS patient_id_nk,
        location_id AS location_id_nk,
        src_sys,
        GETUTCDATE() AS crt_ts,
        GETUTCDATE() AS upd_ts
    FROM same_day_cancel_check
)

-- ============================================================================
-- FINAL OUTPUT: Gold Layer Fact Table Structure
-- ============================================================================

SELECT
    npe_added_sk,
    appointment_identity_sk,
    patient_sk,
    location_sk,
    appointment_type_sk,
    is_net_new,
    has_previous_npe_same_window,
    same_day_cancel_flag,
    appt_added_date,
    appt_added_datetime,
    appt_datetime,
    source_system_id,
    patient_id_nk,
    location_id_nk,
    src_sys,
    crt_ts,
    upd_ts
FROM gold_fct_appointment_npe_added_final
ORDER BY appt_added_date DESC, appt_added_datetime DESC;

-- ============================================================================
-- CLEANUP
-- ============================================================================

DROP TABLE IF EXISTS #bronze_appointments;
DROP TABLE IF EXISTS #bronze_appointment_types;
DROP TABLE IF EXISTS #bronze_appointment_status_history;
DROP TABLE IF EXISTS #bronze_patients;
DROP TABLE IF EXISTS #bronze_locations;

-- ============================================================================
-- OUTPUT SCHEMA NOTES
-- ============================================================================
-- Expected columns in result set (gold_fct_appointment_npe_added):
-- 
-- npe_added_sk (BIGINT)                          - Surrogate key hash(source_system_id + patient_id + location_id + appt_added_date)
-- appointment_identity_sk (BIGINT)               - FK to appointment identity dimension
-- patient_sk (BIGINT)                            - FK to patient dimension
-- location_sk (BIGINT)                           - FK to location dimension (for 6-month scoping)
-- appointment_type_sk (BIGINT)                   - FK to appointment type dimension
-- is_net_new (BIT)                               - 1 if first NPE in 6-month window and not cancelled same day
-- has_previous_npe_same_window (BIT)             - 1 if patient has prior NPE at location in past 6 months
-- same_day_cancel_flag (BIT)                     - 1 if appointment was cancelled on the same day it was added
-- appt_added_date (DATE)                         - Date appointment was added to system
-- appt_added_datetime (DATETIME2(3))             - Datetime appointment was added (timestamp of data load)
-- appt_datetime (DATETIME2(3))                   - Actual appointment date/time
-- source_system_id (INT)                         - Source system identifier
-- patient_id_nk (VARCHAR(50))                    - Natural key for lineage tracking
-- location_id_nk (VARCHAR(50))                   - Natural key for lineage tracking
-- src_sys (VARCHAR(50))                          - Source system name (e.g., 'CentralC9')
-- crt_ts (DATETIME2(3))                          - Gold layer creation timestamp (UTC)
-- upd_ts (DATETIME2(3))                          - Gold layer update timestamp (UTC)
--
-- ============================================================================

```
# Fabric
```sql
create table scd2.patient_id_ofi__x__patient_id_cc9 (
    audit_id bigint not null identity,
    load_datetime_utc datetime2(6),
    -- tracked columns
    patient_id__ofi int not null,
    patient_id__cc9 uniqueidentifier not null,
    system_id__cc9 int not null,
    /* enrichment */
    load_process_id int,
    comment varchar(2500),
    end_datetime_utc datetime2(6),
    end_comment varchar(250)
);
```

```sql
CREATE OR ALTER PROCEDURE edw.usp_snapshot_patient_status
    @snapshot_time datetime2(7) = NULL
AS
BEGIN
    SET NOCOUNT ON;
    SET XACT_ABORT ON;

    SET @snapshot_time = COALESCE(@snapshot_time, SYSUTCDATETIME());

    /*==============================================================
      1. Capture today's source snapshot

      Assumption:
      - Source returns exactly one row per patient_id__cc9.
    ==============================================================*/
    DROP TABLE IF EXISTS #snapshot;

    SELECT
        patient_id__cc9,
        patient_status
    INTO #snapshot
    FROM staging.patient_current;


 

    /*==============================================================
      4. Identify new or changed patients before modifying target
    ==============================================================*/
    DROP TABLE IF EXISTS #delta;

    SELECT
        s.patient_id__cc9,
        s.patient_status,
        CASE
            WHEN h.patient_id__cc9 IS NULL THEN 'NEW'
            ELSE 'CHANGED'
        END AS change_type
    INTO #delta
    FROM #snapshot AS s
    LEFT JOIN edw.patient_status_history AS h
        ON  h.patient_id__cc9 = s.patient_id__cc9
        AND h.valid_to IS NULL
    WHERE
           h.patient_id__cc9 IS NULL
        OR EXISTS
        (
            SELECT s.patient_status
            EXCEPT
            SELECT h.patient_status
        );


    /*==============================================================
      5. Persist SCD2 changes atomically
    ==============================================================*/
    BEGIN TRY
        BEGIN TRANSACTION;

        /* Close the previous state for changed patients */
        UPDATE h
        SET h.valid_to = @snapshot_time
        FROM edw.patient_status_history AS h
        INNER JOIN #delta AS d
            ON  d.patient_id__cc9 = h.patient_id__cc9
            AND d.change_type = 'CHANGED'
        WHERE h.valid_to IS NULL;


        /* Insert the new current state */
        INSERT INTO edw.patient_status_history
        (
            patient_id__cc9,
            patient_status,
            valid_from,
            valid_to
        )
        SELECT
            patient_id__cc9,
            patient_status,
            @snapshot_time,
            NULL
        FROM #delta;

        COMMIT TRANSACTION;

    END TRY
    BEGIN CATCH

        IF @@TRANCOUNT > 0
            ROLLBACK TRANSACTION;

        THROW;

    END CATCH;


    /*==============================================================
      6. Flight debrief
    ==============================================================*/
    SELECT
        @snapshot_time AS snapshot_time,
        COUNT(*) AS persisted_count,
        SUM(CASE WHEN change_type = 'NEW'     THEN 1 ELSE 0 END) AS new_count,
        SUM(CASE WHEN change_type = 'CHANGED' THEN 1 ELSE 0 END) AS changed_count
    FROM #delta;

END;
```
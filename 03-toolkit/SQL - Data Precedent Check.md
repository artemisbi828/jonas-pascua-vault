
```sql
	--Added this check to not mess things up when DayForce Sync does not finish
	if not exists(select top (1) 1 FROM Dayforce.dbo.EmployeeWorkAssignment) 
	or not exists(select top (1) 1 from Dayforce.dbo.DeptJob)
	or not exists(select top (1) 1 from Dayforce.dbo.EmployeeEmploymentStatus)
	or not exists(select top (1) 1 from Dayforce.dbo.Job)
	or not exists(select top (1) 1 from Dayforce.dbo.Department)
	or not exists(select top (1) 1 from Dayforce.dbo.OrgUnit)
	or not exists(select top (1) 1 from Dayforce.dbo.OrgUnitParent)
	or not exists(select 1 from Dayforce.dbo.Employee) begin
		--This error should trigger an email to OpsGenie when running in a job.
		set @msg = 'Possible missing data in Dayforce'
		raiserror(@msg, 16,1);
		return 
	end
```
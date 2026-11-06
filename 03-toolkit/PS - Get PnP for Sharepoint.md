Import-Module "PnP.PowerShell"
# SharePoint site URL
$siteUrl = "https://smiledoctors.sharepoint.com/sites/GRPCES-LegacyPMSInformationTechnology/WebForms"
$listName = "Form Entries"
# Connect to SharePoint
Connect-PnPOnline -Url $siteUrl -Interactive


$listItems = Get-PnPListItem -List $listName -Id 1 -IncludeContentType
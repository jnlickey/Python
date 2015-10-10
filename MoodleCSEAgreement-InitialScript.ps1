Import-Module ActiveDirectory

Set-ExecutionPolicy RemoteSigned
#Set-ExecutionPolicy Unrestricted

$path_to_Moodle_list = "X:\\Desktop\Moodle_Info\\Agreements_1 Grades-comma_separated.csv"
$path_to_excluded_list = "X:\\Desktop\Moodle_Info\\Moodle_excluded_list.csv"
$path_to_pMoodle_Not_Signed_Agreement = "X:\\Desktop\Moodle_Info\\pMoodle_Not_Signed_Agreement.CSV"
$path_to_pMoodle_Signed_Agreement = "X:\\Desktop\Moodle_Info\\pMoodle_Signed_Agreement.CSV"

# Create Array's
$UserNotSigned_Output = @()
$UserSignedOutput = @()

#Import CSV files
$Moodle_list_NotSigned = import-csv -path $path_to_Moodle_list | where-object {$_."Course total (Real)" -eq "-"} | select "Email Address", "Course total (Real)"
$excluded_list = import-csv -path $path_to_excluded_list

# Regretfully took from http://powershell.org/wp/forums/topic/compare-two-csv-files-and-remove-the-same-values/ to check for duplicates
$duplcates_NotSigned = Compare-Object $Moodle_list_NotSigned $excluded_list -Property "Email Address" -IncludeEqual -ExcludeDifferent -PassThru | Select-Object -ExpandProperty "Email Address"
$Moodle_list_NotSigned | Where-Object {$_."Email Address" -notin $duplcates_NotSigned -and $_."Course total (Real)" -eq "-"} | Export-CSV -Path $path_to_pMoodle_Not_Signed_Agreement -noTypeInformation

# Not Signed Agreement
$UserNotSigned_Output += import-csv -path $path_to_pMoodle_Not_Signed_Agreement
$email = $UserNotSigned_Output | foreach {$_."Email address"}
$user_info_before = $email | foreach-object {Get-ADUser -Filter {EmailAddress -eq $_} -Properties Mail, loginShell, name | Select Mail, loginShell, name}
$user_info_before | foreach-object {Set-ADUser -Identity $_.name -replace @{loginShell="/bin/false"}}
$user_info_after = $email | foreach-object {Get-ADUser -Filter {EmailAddress -eq $_} -Properties Mail, loginShell, name | Select Mail, loginShell, name}

"BEFORE"
$user_info_before

"`nAFTER"
$user_info_after

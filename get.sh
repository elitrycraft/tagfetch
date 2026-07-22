$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

$binary = if ($env:PROCESSOR_ARCHITECTURE -eq "ARM64") { "tagfetch_windows_arm64.exe" } else { "tagfetch_windows_x86_64.exe" }

$release = Invoke-RestMethod https://api.github.com/repos/elitrycraft/tagfetch/releases/latest
$asset = $release.assets | Where-Object { $_.name -eq $binary }

if ($isAdmin) {
    $destDir = "$env:ProgramFiles\TagFetch"
    $scope = "Machine"
} else {
    $destDir = "$env:LOCALAPPDATA\TagFetch"
    $scope = "User"
}

New-Item -ItemType Directory -Force -Path $destDir | Out-Null
Invoke-WebRequest -Uri $asset.browser_download_url -OutFile "$destDir\tagfetch.exe"

$path = [Environment]::GetEnvironmentVariable("Path", $scope)
if ($path -notlike "*TagFetch*") {
    [Environment]::SetEnvironmentVariable("Path", "$path;$destDir", $scope)
}

Write-Host "Installed to $destDir. Restart terminal and run: tagfetch"

Write-Host "Detecting system architecture..." -ForegroundColor Cyan

$arch = $env:PROCESSOR_ARCHITECTURE
if ($arch -eq "AMD64") {
    $binary = "TagFetch_windows_amd64.exe"
    $url = "https://github.com/elitrycraft/tagfetch/releases/download/1.0.3R/$binary"
} elseif ($arch -eq "ARM64") {
    $binary = "TagFetch_windows_arm64.exe"
    $url = "https://github.com/elitrycraft/tagfetch/releases/download/1.0.3R/$binary"
} else {
    Write-Host "Unsupported architecture: $arch" -ForegroundColor Red
    exit 1
}

Write-Host "Detected: $arch" -ForegroundColor Green
Write-Host "Installing TagFetch..." -ForegroundColor Cyan

$destDir = "$env:ProgramFiles\TagFetch"
$dest = "$destDir\tagfetch.exe"

New-Item -ItemType Directory -Force -Path $destDir | Out-Null

try {
    Invoke-WebRequest -Uri $url -OutFile $dest -UseBasicParsing
    Write-Host "Downloaded successfully" -ForegroundColor Green
} catch {
    Write-Host "Download failed: $_" -ForegroundColor Red
    exit 1
}

# add to system PATH
$path = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($path -notlike "*TagFetch*") {
    [Environment]::SetEnvironmentVariable("Path", "$path;$destDir", "Machine")
    Write-Host "Added to system PATH" -ForegroundColor Yellow
}

Write-Host "TagFetch installed to $dest" -ForegroundColor Green
Write-Host "Restart terminal and run: tagfetch" -ForegroundColor Cyan

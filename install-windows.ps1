# Save this as install-winget.ps1

# Download the latest App Installer package (which includes winget)
$downloadUrl = "https://aka.ms/getwinget"
$outputFile = "$env:TEMP\Microsoft.DesktopAppInstaller.msixbundle"

Write-Output "Downloading Winget installer..."
Invoke-WebRequest -Uri $downloadUrl -OutFile $outputFile

# Install the package
Write-Output "Installing Winget..."
Add-AppxPackage -Path $outputFile

Write-Output "✅ Winget installation complete!"

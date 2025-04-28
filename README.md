# ThorLMH
ThorLMH is an local and open source voice assistant, utilizing Google's Gemma 3 4b vision model, combining it with multimodal capabilities such as speech and vision. Planning to add MCP, RAG later

# Linux install:
1. In the project folder, run chmod +x linux-install.sh
2. ./linux-install.sh
3. Done!

# Windows install:
1. Run install-windows.ps1
2. Done. If there are any errors, look below.

If you get this error with the Windows install: 
Invoke-WebRequest : Cannot validate argument on parameter 'Uri'. The argument is null or empty. Provide an argument
that is not null or empty, and then try the command again.
At line:8 char:24
+ Invoke-WebRequest -Uri $downloadUrl -OutFile $outputFile
+                        ~~~~~~~~~~~~
    + CategoryInfo          : InvalidData: (:) [Invoke-WebRequest], ParameterBindingValidationException
    + FullyQualifiedErrorId : ParameterArgumentValidationError,Microsoft.PowerShell.Commands.InvokeWebRequestCommand

please run this:
Set-ExecutionPolicy Bypass -Scope Process -Force
./install-winget.ps1


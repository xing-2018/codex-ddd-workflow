# Human-in-the-loop reproduction loop for native Windows PowerShell.
# Copy this file, edit the steps below, and run it.
# The agent runs the script; the user follows prompts in the terminal.
# Capture only observations the user has already redacted; leave signing in to the user.

$ErrorActionPreference = 'Stop'

function Step([string]$Instruction) {
    Write-Host "`n>>> $Instruction"
    [void](Read-Host '    [Press Enter when done]')
}

function Capture([string]$Question) {
    Write-Host "`n>>> $Question"
    return Read-Host '    >'
}

# --- edit below ---------------------------------------------------------

Step "Open the app at http://localhost:3000 and sign in."

$ERRORED = Capture "Click the 'Export' button. Did it throw an error? (y/n)"
$ERROR_MSG = Capture "Paste the error message only after replacing every secret with <REDACTED> (or enter 'none'):"

# --- edit above ---------------------------------------------------------

Write-Host "`n--- Captured ---"
Write-Host "ERRORED=$ERRORED"
Write-Host "ERROR_MSG=$ERROR_MSG"

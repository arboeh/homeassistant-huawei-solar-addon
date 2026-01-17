# run_local.ps1 - Local development runner (PowerShell)

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "🚀 Huawei Solar MQTT - Local Development" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Cyan

# Load .env (besseres Parsing)
if (Test-Path .env) {
    Write-Host "📄 Loading .env" -ForegroundColor Blue
    Get-Content .env | ForEach-Object {
        $line = $_.Trim()
        # Skip comments and empty lines
        if ($line -and !$line.StartsWith('#')) {
            if ($line -match '^([^=]+)=(.*)$') {
                $key = $matches[1].Trim()
                $value = $matches[2].Trim()
                Set-Item -Path "env:$key" -Value $value
                Write-Host "  $key = $value" -ForegroundColor DarkGray
            }
        }
    }
} else {
    Write-Host "❌ No .env file!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Inverter: $env:HUAWEI_MODBUS_HOST`:$env:HUAWEI_MODBUS_PORT"
Write-Host "MQTT:     $env:HUAWEI_MODBUS_MQTT_BROKER`:$env:HUAWEI_MODBUS_MQTT_PORT"
Write-Host "Log:      $env:HUAWEI_LOG_LEVEL"
Write-Host "========================================================================" -ForegroundColor Cyan

# Check if MQTT broker is reachable
$mqttHost = $env:HUAWEI_MODBUS_MQTT_BROKER
$mqttPort = $env:HUAWEI_MODBUS_MQTT_PORT
try {
    $connection = Test-NetConnection -ComputerName $mqttHost -Port $mqttPort -WarningAction SilentlyContinue
    if (!$connection.TcpTestSucceeded) {
        Write-Host "⚠️  MQTT Broker not reachable at ${mqttHost}:${mqttPort}" -ForegroundColor Yellow
        Write-Host "   Make sure Mosquitto is running!" -ForegroundColor Yellow
    }
} catch {
    Write-Host "⚠️  Cannot test MQTT connection" -ForegroundColor Yellow
}

# Run
Set-Location huawei-solar-modbus-mqtt
python -m modbus_energy_meter.main

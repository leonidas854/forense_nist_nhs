# Practica docente: datos ficticios, sin red, sin malware y sin privilegios elevados.
# Solo escribe en una carpeta nueva bajo LOCALAPPDATA; conserva todos los resultados.
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$host.UI.RawUI.WindowTitle = 'NHS - PRUEBA BENIGNA - SIN MALWARE'
$id = [DateTime]::UtcNow.ToString('yyyyMMddTHHmmssZ') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,8)
$root = Join-Path $env:LOCALAPPDATA ('NHS_Forense_Practica\' + $id)
New-Item -ItemType Directory -Path $root -ErrorAction Stop | Out-Null
$utf8 = [Text.UTF8Encoding]::new($false)
$results = [ordered]@{
    tipo = 'S: ejercicio benigno; resultados observados en laboratorio'
    id = $id
    inicio_utc = [DateTime]::UtcNow.ToString('o')
    script_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash
    sistema = [Environment]::OSVersion.VersionString
    powershell = $PSVersionTable.PSVersion.ToString()
    carpeta = $root
    estado = 'INICIADO'
}
try {
    # Consulta local de estado; no pings, conexiones, descargas ni cambios de red.
    $adapters = @(Get-CimInstance Win32_NetworkAdapter | Where-Object { $_.NetEnabled -eq $true })
    $results.adaptadores_habilitados = $adapters.Count
    if ($adapters.Count -ne 0) { throw 'Hay adaptadores habilitados: practica detenida.' }

    $original = Join-Path $root 'referencia.txt'
    $backup = Join-Path $root 'copia.txt'
    $working = Join-Path $root 'trabajo.txt'
    $text = "NHS: dato ficticio de clase. No es informacion clinica.`r`n"
    [IO.File]::WriteAllText($original, $text, $utf8)
    Copy-Item -LiteralPath $original -Destination $backup -ErrorAction Stop
    Copy-Item -LiteralPath $original -Destination $working -ErrorAction Stop
    $h0 = (Get-FileHash -LiteralPath $original -Algorithm SHA256).Hash
    $hb = (Get-FileHash -LiteralPath $backup -Algorithm SHA256).Hash
    if ($h0 -ne $hb) { throw 'La copia inicial no coincide con la referencia.' }
    $results.hash_referencia = $h0
    $results.hash_copia = $hb

    [IO.File]::WriteAllText($working, "Cambio ficticio controlado para la clase.`r`n", $utf8)
    $h1 = (Get-FileHash -LiteralPath $working -Algorithm SHA256).Hash
    if ($h1 -eq $h0) { throw 'No se detecto el cambio previsto.' }
    $results.hash_modificado = $h1
    $results.deteccion_cambio = 'CORRECTO'

    Copy-Item -LiteralPath $backup -Destination $working -Force -ErrorAction Stop
    $h2 = (Get-FileHash -LiteralPath $working -Algorithm SHA256).Hash
    $restored = [IO.File]::ReadAllText($working, $utf8)
    if (($h2 -ne $h0) -or ($restored -cne $text)) { throw 'Restauracion no validada.' }
    $results.hash_restaurado = $h2
    $results.restauracion_hash_y_lectura = 'CORRECTO'
    $results.limite_respaldo = 'Copia en el mismo disco; no es un respaldo aislado institucional.'

    # Solo se abre y cierra el Bloc de notas creado por esta practica.
    $process = Start-Process -FilePath (Join-Path $env:WINDIR 'System32\notepad.exe') -ArgumentList ('"' + $working + '"') -PassThru
    try {
        if (-not $process.WaitForInputIdle(10000)) { throw 'No se comprobo la interfaz de Bloc de notas.' }
        $observed = Get-Process -Id $process.Id -ErrorAction Stop
        if ($observed.ProcessName -ne 'notepad') { throw 'Proceso inesperado.' }
        $results.proceso = [ordered]@{
            nombre = $observed.ProcessName
            pid = $observed.Id
            inicio_utc = $observed.StartTime.ToUniversalTime().ToString('o')
            observacion = 'Get-Process por el PID devuelto; interfaz lista'
        }
        Start-Sleep -Seconds 2
        if (-not $process.CloseMainWindow()) { throw 'No se pudo solicitar cierre normal.' }
        if (-not $process.WaitForExit(10000)) { throw 'No se comprobo el cierre del proceso.' }
        $results.proceso_cerrado = 'CORRECTO'
        $results.proceso.codigo_salida = $process.ExitCode
    }
    finally {
        $process.Dispose()
    }
    $results.estado = 'COMPLETADO'
}
catch {
    $results.estado = 'FALLO'
    $results.error = $_.Exception.Message
}
finally {
    $results.fin_utc = [DateTime]::UtcNow.ToString('o')
    $report = Join-Path $root 'resultado.json'
    [IO.File]::WriteAllText($report, ($results | ConvertTo-Json -Depth 6), $utf8)
    $reportHash = (Get-FileHash -LiteralPath $report -Algorithm SHA256).Hash
    [IO.File]::WriteAllText((Join-Path $root 'resultado.sha256'), $reportHash + '  resultado.json', $utf8)
    Clear-Host
    Write-Host 'NHS - PRACTICA BENIGNA - SIN MALWARE'
    Write-Host ('ID: ' + $id)
    Write-Host ('ESTADO: ' + $results.estado)
    foreach ($key in @('inicio_utc','fin_utc','adaptadores_habilitados','deteccion_cambio','restauracion_hash_y_lectura','proceso_cerrado','hash_referencia','hash_modificado','hash_restaurado','error')) {
        if ($results.Contains($key)) { Write-Host ($key + ': ' + $results[$key]) }
    }
    if ($results.Contains('proceso')) {
        Write-Host ('PROCESO: ' + $results.proceso.nombre + ' PID=' + $results.proceso.pid)
    }
    Write-Host ('JSON SHA256: ' + $reportHash)
    Write-Host ('RESULTADOS: ' + $root)
    Write-Host 'Limite: copia en el mismo disco; no demuestra recuperacion de ransomware.'
}

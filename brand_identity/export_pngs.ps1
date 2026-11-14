Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$baseDir = "c:\Users\Admin1\Desktop\Marble Contractor Site\brand_identity"
$pngDir = Join-Path $baseDir "png"
if (!(Test-Path $pngDir)) { New-Item -ItemType Directory -Path $pngDir -Force | Out-Null }

$jobs = @(
    # Primary
    @{ Svg = "$baseDir\final\primary\balaji-logo-primary-gold.svg"; Png = "$pngDir\balaji-logo-primary-gold.png"; W = 1800; H = 1240; Bg = "#FF00FF"; Key = [System.Drawing.Color]::FromArgb(255, 0, 255) },
    @{ Svg = "$baseDir\final\primary\balaji-logo-primary-dark.svg"; Png = "$pngDir\balaji-logo-primary-dark.png"; W = 1800; H = 1240; Bg = "#FFFFFF"; Key = [System.Drawing.Color]::White },
    @{ Svg = "$baseDir\final\primary\balaji-logo-primary-white.svg"; Png = "$pngDir\balaji-logo-primary-white.png"; W = 1800; H = 1240; Bg = "#000000"; Key = [System.Drawing.Color]::Black },
    
    # Horizontal
    @{ Svg = "$baseDir\final\horizontal\balaji-logo-horizontal-gold.svg"; Png = "$pngDir\balaji-logo-horizontal-gold.png"; W = 1700; H = 400; Bg = "#FF00FF"; Key = [System.Drawing.Color]::FromArgb(255, 0, 255) },
    @{ Svg = "$baseDir\final\horizontal\balaji-logo-horizontal-dark.svg"; Png = "$pngDir\balaji-logo-horizontal-dark.png"; W = 1700; H = 400; Bg = "#FFFFFF"; Key = [System.Drawing.Color]::White },
    @{ Svg = "$baseDir\final\horizontal\balaji-logo-horizontal-white.svg"; Png = "$pngDir\balaji-logo-horizontal-white.png"; W = 1700; H = 400; Bg = "#000000"; Key = [System.Drawing.Color]::Black },
    
    # Stacked
    @{ Svg = "$baseDir\final\stacked\balaji-logo-stacked-gold.svg"; Png = "$pngDir\balaji-logo-stacked-gold.png"; W = 1400; H = 1120; Bg = "#FF00FF"; Key = [System.Drawing.Color]::FromArgb(255, 0, 255) },
    @{ Svg = "$baseDir\final\stacked\balaji-logo-stacked-dark.svg"; Png = "$pngDir\balaji-logo-stacked-dark.png"; W = 1400; H = 1120; Bg = "#FFFFFF"; Key = [System.Drawing.Color]::White },
    @{ Svg = "$baseDir\final\stacked\balaji-logo-stacked-white.svg"; Png = "$pngDir\balaji-logo-stacked-white.png"; W = 1400; H = 1120; Bg = "#000000"; Key = [System.Drawing.Color]::Black },
    
    # Icon / Monogram
    @{ Svg = "$baseDir\final\icon\balaji-monogram-gold.svg"; Png = "$pngDir\balaji-monogram-gold.png"; W = 1024; H = 1024; Bg = "#FF00FF"; Key = [System.Drawing.Color]::FromArgb(255, 0, 255) },
    @{ Svg = "$baseDir\final\icon\balaji-monogram-dark.svg"; Png = "$pngDir\balaji-monogram-dark.png"; W = 1024; H = 1024; Bg = "#FFFFFF"; Key = [System.Drawing.Color]::White },
    @{ Svg = "$baseDir\final\icon\balaji-monogram-white.svg"; Png = "$pngDir\balaji-monogram-white.png"; W = 1024; H = 1024; Bg = "#000000"; Key = [System.Drawing.Color]::Black },
    @{ Svg = "$baseDir\final\icon\balaji-monogram-badge.svg"; Png = "$pngDir\balaji-monogram-badge.png"; W = 1024; H = 1024; Bg = "#FF00FF"; Key = [System.Drawing.Color]::FromArgb(255, 0, 255) }
)

$wb = New-Object System.Windows.Forms.WebBrowser
$wb.ScrollBarsEnabled = $false
$wb.ScriptErrorsSuppressed = $true

foreach ($job in $jobs) {
    $svgContent = Get-Content -Raw -Encoding UTF8 $job.Svg
    $html = @"
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    background-color: $($job.Bg);
    overflow: hidden;
  }
  svg {
    width: 100%;
    height: 100%;
    display: block;
  }
</style>
</head>
<body>
$svgContent
</body>
</html>
"@
    $tempHtml = "$baseDir\temp_render.html"
    Set-Content -Path $tempHtml -Value $html -Encoding UTF8
    
    $wb.Width = $job.W / 2
    $wb.Height = $job.H / 2
    $wb.Navigate((Resolve-Path $tempHtml).Path)
    
    $timeout = 0
    while ($wb.ReadyState -ne [System.Windows.Forms.WebBrowserReadyState]::Complete -and $timeout -lt 60) {
        [System.Windows.Forms.Application]::DoEvents()
        Start-Sleep -Milliseconds 50
        $timeout++
    }
    Start-Sleep -Milliseconds 100
    
    $bmp = New-Object System.Drawing.Bitmap ($job.W / 2), ($job.H / 2)
    $wb.DrawToBitmap($bmp, (New-Object System.Drawing.Rectangle 0, 0, ($job.W / 2), ($job.H / 2)))
    
    if ($job.Key -ne $null) {
        $bmp.MakeTransparent($job.Key)
    }
    
    $bmp.Save($job.Png, [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output "Exported PNG: $(Split-Path $job.Png -Leaf)"
}

$wb.Dispose()
if (Test-Path "$baseDir\temp_render.html") { Remove-Item "$baseDir\temp_render.html" -Force }
Write-Output "All 13 Transparent PNG previews generated successfully!"


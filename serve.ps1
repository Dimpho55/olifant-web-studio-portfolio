Param(
    [int]$Port = 8000
)

$prefix = "http://localhost:$Port/"
$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($prefix)
$listener.Start()
Write-Output "Serving HTTP on port $Port. Open http://localhost:$Port in your browser. Press Ctrl+C to stop."

function Get-ContentType($ext) {
    switch ($ext.ToLower()) {
        '.html' { 'text/html' }
        '.htm'  { 'text/html' }
        '.css'  { 'text/css' }
        '.js'   { 'application/javascript' }
        '.json' { 'application/json' }
        '.png'  { 'image/png' }
        '.jpg'  { 'image/jpeg' }
        '.jpeg' { 'image/jpeg' }
        '.gif'  { 'image/gif' }
        '.svg'  { 'image/svg+xml' }
        '.txt'  { 'text/plain' }
        default { 'application/octet-stream' }
    }
}

try {
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response

        $urlPath = $request.Url.LocalPath.TrimStart('/')
        if ([string]::IsNullOrEmpty($urlPath)) { $urlPath = 'index.html' }
        $filePath = Join-Path (Get-Location) $urlPath

        if (Test-Path $filePath) {
            try {
                $bytes = [System.IO.File]::ReadAllBytes($filePath)
                $ext = [System.IO.Path]::GetExtension($filePath)
                $response.ContentType = Get-ContentType $ext
                $response.ContentLength64 = $bytes.Length
                $response.OutputStream.Write($bytes, 0, $bytes.Length)
            } catch {
                $response.StatusCode = 500
                $msg = "<h1>500 Internal Server Error</h1><pre>$($_.Exception.Message)</pre>"
                $buf = [System.Text.Encoding]::UTF8.GetBytes($msg)
                $response.ContentType = 'text/html'
                $response.ContentLength64 = $buf.Length
                $response.OutputStream.Write($buf, 0, $buf.Length)
            }
        } else {
            $response.StatusCode = 404
            $msg = "<h1>404 Not Found</h1><p>$urlPath</p>"
            $buf = [System.Text.Encoding]::UTF8.GetBytes($msg)
            $response.ContentType = 'text/html'
            $response.ContentLength64 = $buf.Length
            $response.OutputStream.Write($buf, 0, $buf.Length)
        }
        $response.OutputStream.Close()
    }
} finally {
    $listener.Stop()
    $listener.Close()
}

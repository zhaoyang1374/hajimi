function Load-EnvVariables {
    param (
        [string]$EnvFilePath = ".\.env"
    )

    if (Test-Path -Path $EnvFilePath) {
        $envContent = Get-Content -Path $EnvFilePath
        foreach ($line in $envContent) {
            if ($line -notmatch '^\s*(#|$)') {
                $keyValue = $line -split '=', 2
                if ($keyValue.Length -eq 2) {
                    $key = $keyValue[0].Trim()
                    $value = $keyValue[1].Trim()
                    Set-Item -Path "env:$key" -Value $value
                }
            }
        }
    } else {
        Write-Warning "未找到.env文件: $EnvFilePath"
    }
}

# 调用函数来加载环境变量
Load-EnvVariables    
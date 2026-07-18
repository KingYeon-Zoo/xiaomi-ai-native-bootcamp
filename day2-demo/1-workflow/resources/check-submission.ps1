param(
    [string]$ProjectDir = "D:\code\xiaomi\day1-demo-students\rag-assistant",
    [int]$TimeoutSeconds = 60
)

$ErrorActionPreference = "Stop"

$requiredFiles = @(
    "README.md",
    "docs/spec.md",
    "docs/design.md",
    "docs/ai-log.md",
    "docs/test-record.md",
    "docs/reflection.md"
)

$testCommands = @(
    @{
        Name = "基础结构与接口测试"
        Command = "python"
        Arguments = @("tests/test_basic.py")
        Required = $true
    },
    @{
        Name = "RAG 行为自动化测试"
        Command = "python"
        Arguments = @("tests/test_rag.py")
        Required = $true
    }
)

function Join-ProjectPath {
    param(
        [string]$BasePath,
        [string]$RelativePath
    )

    $parts = $RelativePath -split "/"
    return Join-Path -Path $BasePath -ChildPath ([System.IO.Path]::Combine($parts))
}

function Test-ContentPattern {
    param(
        [string]$Path,
        [string[]]$Patterns
    )

    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        return $false
    }

    $content = Get-Content -Raw -LiteralPath $Path
    foreach ($pattern in $Patterns) {
        if ($content -match $pattern) {
            return $true
        }
    }
    return $false
}

function Invoke-TestCommand {
    param(
        [string]$WorkingDirectory,
        [hashtable]$TestCommand,
        [int]$TimeoutSeconds
    )

    $psi = [System.Diagnostics.ProcessStartInfo]::new()
    $psi.FileName = $TestCommand.Command
    foreach ($arg in $TestCommand.Arguments) {
        [void]$psi.ArgumentList.Add($arg)
    }
    $psi.WorkingDirectory = $WorkingDirectory
    $psi.RedirectStandardOutput = $true
    $psi.RedirectStandardError = $true
    $psi.UseShellExecute = $false
    $psi.CreateNoWindow = $true

    $proc = [System.Diagnostics.Process]::new()
    $proc.StartInfo = $psi

    $started = $false
    try {
        $started = $proc.Start()
        $completed = $proc.WaitForExit($TimeoutSeconds * 1000)
        if (-not $completed) {
            try {
                $proc.Kill($true)
            } catch {
                $proc.Kill()
            }
            return @{
                Name = $TestCommand.Name
                CommandLine = "$($TestCommand.Command) $($TestCommand.Arguments -join ' ')"
                ExitCode = $null
                TimedOut = $true
                Passed = $false
                Stdout = ""
                Stderr = "Timed out after $TimeoutSeconds seconds."
            }
        }

        return @{
            Name = $TestCommand.Name
            CommandLine = "$($TestCommand.Command) $($TestCommand.Arguments -join ' ')"
            ExitCode = $proc.ExitCode
            TimedOut = $false
            Passed = ($proc.ExitCode -eq 0)
            Stdout = $proc.StandardOutput.ReadToEnd()
            Stderr = $proc.StandardError.ReadToEnd()
        }
    } catch {
        if ($started -and -not $proc.HasExited) {
            $proc.Kill()
        }
        return @{
            Name = $TestCommand.Name
            CommandLine = "$($TestCommand.Command) $($TestCommand.Arguments -join ' ')"
            ExitCode = $null
            TimedOut = $false
            Passed = $false
            Stdout = ""
            Stderr = $_.Exception.Message
        }
    } finally {
        $proc.Dispose()
    }
}

function Add-Section {
    param(
        [System.Collections.Generic.List[string]]$Lines,
        [string]$Title
    )

    [void]$Lines.Add("")
    [void]$Lines.Add("## $Title")
    [void]$Lines.Add("")
}

$resolvedProject = [System.IO.Path]::GetFullPath($ProjectDir)
$evidenceDir = Join-Path -Path $resolvedProject -ChildPath ".submission-check"
New-Item -ItemType Directory -Force -Path $evidenceDir | Out-Null

$fileEvidencePath = Join-Path -Path $evidenceDir -ChildPath "file-check.md"
$testEvidencePath = Join-Path -Path $evidenceDir -ChildPath "test-result.md"
$finalReportPath = Join-Path -Path $evidenceDir -ChildPath "final-report.md"

$missingFiles = New-Object System.Collections.Generic.List[string]
$warnings = New-Object System.Collections.Generic.List[string]
$blockedReasons = New-Object System.Collections.Generic.List[string]

if (-not (Test-Path -LiteralPath $resolvedProject -PathType Container)) {
    [void]$blockedReasons.Add("项目目录不存在：$resolvedProject")
}

$fileLines = New-Object System.Collections.Generic.List[string]
[void]$fileLines.Add("# 文件检查")
[void]$fileLines.Add("")
[void]$fileLines.Add("- 项目目录：``$resolvedProject``")
[void]$fileLines.Add("- 检查时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$fileLines.Add("")
[void]$fileLines.Add("## 必需文件")
[void]$fileLines.Add("")
[void]$fileLines.Add("| 文件 | 结果 |")
[void]$fileLines.Add("|------|------|")

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-ProjectPath -BasePath $resolvedProject -RelativePath $relativePath
    if (Test-Path -LiteralPath $fullPath -PathType Leaf) {
        [void]$fileLines.Add("| ``$relativePath`` | PASS |")
    } else {
        [void]$fileLines.Add("| ``$relativePath`` | BLOCKED：缺失 |")
        [void]$missingFiles.Add($relativePath)
        [void]$blockedReasons.Add("缺少必需文件：$relativePath")
    }
}

Add-Section -Lines $fileLines -Title "README 轻量线索"
$readmePath = Join-ProjectPath -BasePath $resolvedProject -RelativePath "README.md"
$readmeChecks = @(
    @{ Label = "安装线索"; Patterns = @("安装", "install", "pip\s+install") },
    @{ Label = "运行线索"; Patterns = @("运行", "run", "python\s+src/main\.py", "python3?\s+src/main\.py") },
    @{ Label = "测试线索"; Patterns = @("测试", "test", "python\s+tests/", "python3?\s+tests/") }
)

[void]$fileLines.Add("| 线索 | 结果 |")
[void]$fileLines.Add("|------|------|")
foreach ($check in $readmeChecks) {
    if (Test-ContentPattern -Path $readmePath -Patterns $check.Patterns) {
        [void]$fileLines.Add("| $($check.Label) | PASS |")
    } else {
        [void]$fileLines.Add("| $($check.Label) | WARNING：未检测到 |")
        [void]$warnings.Add("README 缺少$($check.Label)")
    }
}

Add-Section -Lines $fileLines -Title "ai-log 五字段标签"
$aiLogPath = Join-ProjectPath -BasePath $resolvedProject -RelativePath "docs/ai-log.md"
$aiLogLabels = @("目的", "输入", "建议", "人工判断", "验证")

[void]$fileLines.Add("| 标签 | 结果 |")
[void]$fileLines.Add("|------|------|")
foreach ($label in $aiLogLabels) {
    if (Test-ContentPattern -Path $aiLogPath -Patterns @([regex]::Escape($label))) {
        [void]$fileLines.Add("| $label | PASS |")
    } else {
        [void]$fileLines.Add("| $label | WARNING：未检测到 |")
        [void]$warnings.Add("ai-log 缺少标签：$label")
    }
}

Set-Content -LiteralPath $fileEvidencePath -Value $fileLines -Encoding UTF8

$testLines = New-Object System.Collections.Generic.List[string]
[void]$testLines.Add("# 测试结果")
[void]$testLines.Add("")
[void]$testLines.Add("- 项目目录：``$resolvedProject``")
[void]$testLines.Add("- 检查时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$testLines.Add("- 单条测试超时：$TimeoutSeconds 秒")

$testResults = New-Object System.Collections.Generic.List[object]

if (Test-Path -LiteralPath $resolvedProject -PathType Container) {
    foreach ($testCommand in $testCommands) {
        $result = Invoke-TestCommand -WorkingDirectory $resolvedProject -TestCommand $testCommand -TimeoutSeconds $TimeoutSeconds
        [void]$testResults.Add($result)
        if (-not $result.Passed) {
            if ($result.TimedOut) {
                [void]$blockedReasons.Add("测试超时：$($result.Name)")
            } else {
                [void]$blockedReasons.Add("测试失败：$($result.Name)")
            }
        }
    }
}

foreach ($result in $testResults) {
    Add-Section -Lines $testLines -Title $result.Name
    [void]$testLines.Add("- 命令：``$($result.CommandLine)``")
    [void]$testLines.Add("- 结果：$(if ($result.Passed) { 'PASS' } elseif ($result.TimedOut) { 'BLOCKED：超时' } else { 'BLOCKED：失败' })")
    [void]$testLines.Add("- 退出码：$(if ($null -eq $result.ExitCode) { 'N/A' } else { $result.ExitCode })")
    [void]$testLines.Add("")
    [void]$testLines.Add("### stdout")
    [void]$testLines.Add("")
    [void]$testLines.Add('```text')
    [void]$testLines.Add($result.Stdout.Trim())
    [void]$testLines.Add('```')
    [void]$testLines.Add("")
    [void]$testLines.Add("### stderr")
    [void]$testLines.Add("")
    [void]$testLines.Add('```text')
    [void]$testLines.Add($result.Stderr.Trim())
    [void]$testLines.Add('```')
}

Set-Content -LiteralPath $testEvidencePath -Value $testLines -Encoding UTF8

if ($blockedReasons.Count -gt 0) {
    $status = "BLOCKED"
} elseif ($warnings.Count -gt 0) {
    $status = "WARNING"
} else {
    $status = "PASS"
}

$nextActions = New-Object System.Collections.Generic.List[string]
if ($status -eq "PASS") {
    [void]$nextActions.Add("可以提交，并保留 `.submission-check/final-report.md` 作为检查证据。")
} else {
    foreach ($reason in $blockedReasons) {
        [void]$nextActions.Add("修复阻塞项：$reason")
    }
    foreach ($warning in $warnings) {
        [void]$nextActions.Add("建议改进：$warning")
    }
    [void]$nextActions.Add("修复后重新运行 ``.\resources\check-submission.ps1``。")
}

$reportLines = New-Object System.Collections.Generic.List[string]
[void]$reportLines.Add("# 提交检查报告")
[void]$reportLines.Add("")
[void]$reportLines.Add("## 基本信息")
[void]$reportLines.Add("")
[void]$reportLines.Add("- 项目目录：``$resolvedProject``")
[void]$reportLines.Add("- 检查时间：$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')")
[void]$reportLines.Add("- 综合状态：**$status**")

Add-Section -Lines $reportLines -Title "文件检查"
[void]$reportLines.Add("- 必需文件缺失数：$($missingFiles.Count)")
[void]$reportLines.Add("- WARNING 数：$($warnings.Count)")
[void]$reportLines.Add("- 证据：``$fileEvidencePath``")

Add-Section -Lines $reportLines -Title "测试结果"
if ($testResults.Count -eq 0) {
    [void]$reportLines.Add("- 未运行测试。")
} else {
    [void]$reportLines.Add("| 测试 | 命令 | 结果 |")
    [void]$reportLines.Add("|------|------|------|")
    foreach ($result in $testResults) {
        $resultText = if ($result.Passed) { "PASS" } elseif ($result.TimedOut) { "BLOCKED：超时" } else { "BLOCKED：失败" }
        [void]$reportLines.Add("| $($result.Name) | ``$($result.CommandLine)`` | $resultText |")
    }
}
[void]$reportLines.Add("")
[void]$reportLines.Add("- 证据：``$testEvidencePath``")

Add-Section -Lines $reportLines -Title "综合状态判定"
if ($status -eq "PASS") {
    [void]$reportLines.Add("必需文件全部存在，必跑测试全部通过，轻量检查未发现警告。")
} elseif ($status -eq "WARNING") {
    [void]$reportLines.Add("必需文件全部存在，必跑测试全部通过，但存在轻量文档警告。")
} else {
    [void]$reportLines.Add("存在阻塞项，当前提交包无法被可靠评审或验证。")
}

Add-Section -Lines $reportLines -Title "下一步动作"
foreach ($action in $nextActions) {
    [void]$reportLines.Add("- $action")
}

Add-Section -Lines $reportLines -Title "证据文件"
[void]$reportLines.Add("- ``$fileEvidencePath``")
[void]$reportLines.Add("- ``$testEvidencePath``")
[void]$reportLines.Add("- ``$finalReportPath``")

Set-Content -LiteralPath $finalReportPath -Value $reportLines -Encoding UTF8

Write-Host "综合状态：$status"
Write-Host "最终报告：$finalReportPath"

if ($status -eq "BLOCKED") {
    exit 2
}
if ($status -eq "WARNING") {
    exit 1
}
exit 0

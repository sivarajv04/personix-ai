$ignore = @(
    "venv",".venv","env",
    "__pycache__","*.pyc",".pytest_cache",".mypy_cache",".ruff_cache",
    ".git",".idea",".vscode",
    "node_modules",".next",".nuxt",".cache",
    "dist","build","out","coverage","htmlcov",
    "*.egg-info",".DS_Store"
)

function ShouldIgnore($name) {
    foreach ($pattern in $ignore) {
        if ($name -like $pattern) { return $true }
    }
    return $false
}

function Show-Tree($path, $prefix="") {

    $items = Get-ChildItem -LiteralPath $path -Force |
             Where-Object { -not (ShouldIgnore $_.Name) } |
             Sort-Object -Property PSIsContainer, Name -Descending

    for ($i = 0; $i -lt $items.Count; $i++) {

        $item = $items[$i]
        $isLast = ($i -eq $items.Count - 1)

        $connector = if ($isLast) { "+-- " } else { "|-- " }

        "$prefix$connector$($item.Name)"

        if ($item.PSIsContainer) {
            $newPrefix = if ($isLast) { "$prefix    " } else { "$prefix|   " }
            Show-Tree $item.FullName $newPrefix
        }
    }
}

"." | Out-File project_structure.txt -Encoding utf8
Show-Tree "." | Out-File project_structure.txt -Append -Encoding utf8

Write-Host "project_structure.txt generated"

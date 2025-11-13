param(
    [ValidateSet('patch','minor','major')]
    [string]$Bump = 'patch',
    [string]$Pre = '',
    [switch]$Auto,
    [switch]$NoPush
)

$ErrorActionPreference = 'Stop'

function Ensure-Tool($name) {
    if (-not (Get-Command $name -ErrorAction SilentlyContinue)) {
        throw "Required tool '$name' not found in PATH."
    }
}

function Get-LastTag() {
    try { (git describe --tags --abbrev=0) } catch { $null }
}

function Get-RepoHttpsUrl() {
    $remote = git config --get remote.origin.url
    if (-not $remote) { return $null }
    if ($remote -match '^git@github.com:(.+)\.git$') { return "https://github.com/$($Matches[1])" }
    if ($remote -match '^https?://') { return ($remote -replace '\.git$','') }
    return $remote
}

function Get-CurrentVersion($path) {
    $text = Get-Content -Raw -Encoding UTF8 -Path $path
    $m = [regex]::Match($text, '__version__\s*=\s*"([^"]+)"')
    if (-not $m.Success) { throw "Could not find __version__ in $path" }
    return $m.Groups[1].Value
}

function Set-CurrentVersion($path, $newVersion) {
    $text = Get-Content -Raw -Encoding UTF8 -Path $path
    $text = [regex]::Replace($text, '__version__\s*=\s*"([^"]+)"', "__version__ = \"$newVersion\"")
    Set-Content -NoNewline -Encoding UTF8 -Path $path -Value $text
}

function Increment-Version($version, $bump) {
    # Strip pre-release if present
    $core = $version.Split('-')[0]
    $parts = $core.Split('.') | ForEach-Object {[int]$_}
    if ($parts.Count -ne 3) { throw "Version must be MAJOR.MINOR.PATCH, got '$version'" }
    $major,$minor,$patch = $parts
    switch ($bump) {
        'major' { $major++; $minor=0; $patch=0 }
        'minor' { $minor++; $patch=0 }
        default  { $patch++ }
    }
    return "$major.$minor.$patch"
}

function Detect-BumpFromCommits($range) {
    $logs = if ($range) { git log --pretty=format:'%s' $range } else { git log --pretty=format:'%s' }
    $subjects = @($logs)
    if ($subjects -match 'BREAKING CHANGE|!:') { return 'major' }
    if ($subjects -match '^(feat|feature)(\(|:)?') { return 'minor' }
    return 'patch'
}

function Get-CommitBullets($range) {
    if ($range) {
        git log --pretty=format:'- %s' $range
    } else {
        git log --pretty=format:'- %s'
    }
}

function Update-ReadmeVersion($readmePath, $newVersion) {
    if (-not (Test-Path $readmePath)) { return }
    $text = Get-Content -Raw -Encoding UTF8 -Path $readmePath
    if ($text -match '\*\*Version\*\*:\s*([0-9A-Za-z\.-]+)') {
        $text = [regex]::Replace($text, '\*\*Version\*\*:\s*([0-9A-Za-z\.-]+)', "**Version**: $newVersion")
        Set-Content -NoNewline -Encoding UTF8 -Path $readmePath -Value $text
    }
}

function Prepend-Changelog($changelogPath, $section) {
    $existing = ''
    if (Test-Path $changelogPath) {
        $existing = Get-Content -Raw -Encoding UTF8 -Path $changelogPath
    }
    $new = "$section`n`n$existing"
    Set-Content -NoNewline -Encoding UTF8 -Path $changelogPath -Value $new
}

# 1) Checks
Ensure-Tool git

# 2) Determine last tag and range
$lastTag = Get-LastTag
$range = if ($lastTag) { "$lastTag..HEAD" } else { $null }

# 3) Detect bump if requested
if ($Auto) {
    $Bump = Detect-BumpFromCommits -range $range
    Write-Host "[auto] Bump determined from commits since '$lastTag': $Bump" -ForegroundColor Cyan
}

# 4) Compute new version
$versionFile = Join-Path (Get-Location) 'app_version.py'
$current = Get-CurrentVersion $versionFile
$coreNew = Increment-Version $current $Bump
$newVersion = if ($Pre) { "$coreNew-$Pre" } else { $coreNew }

# 5) Gather changes
$bullets = @(Get-CommitBullets -range $range)
if ($bullets.Count -eq 0) { $bullets = @('- Maintenance updates') }

# 6) Update files
Set-CurrentVersion $versionFile $newVersion
Update-ReadmeVersion (Join-Path (Get-Location) 'README.md') $newVersion

# Changelog section
$today = Get-Date -Format 'yyyy-MM-dd'
$repoUrl = Get-RepoHttpsUrl
$tag = "v$newVersion"
$changelogSection = @()
$changelogSection += "## [$newVersion] - $today"
$changelogSection += "### Changes"
$changelogSection += ($bullets -join "`n")
if ($repoUrl) {
    $changelogSection += ""
    $changelogSection += "[$newVersion]: $repoUrl/releases/tag/$tag"
}
$sectionText = $changelogSection -join "`n"

Prepend-Changelog (Join-Path (Get-Location) 'CHANGELOG.md') $sectionText

# 7) Commit and tag
 git add app_version.py README.md CHANGELOG.md | Out-Null
 git commit -m "chore(release): $newVersion" | Out-Null
 git tag -a $tag -m "Release $newVersion"

if (-not $NoPush) {
    git push
    git push origin $tag
}

Write-Host "Release $newVersion complete." -ForegroundColor Green
Write-Host "Run: python main.py --version  (should show $newVersion)" -ForegroundColor Green

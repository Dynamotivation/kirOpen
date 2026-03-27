Commands MUST be adapted to your Windows system running on win32 with {{SHELL}} shell.

### Windows PowerShell Command Examples

- List files: Get-ChildItem
- Remove file: Remove-Item file.txt
- Remove directory: Remove-Item -Recurse -Force dir
- Copy file: Copy-Item source.txt destination.txt
- Copy directory: Copy-Item -Recurse source destination
- Create directory: New-Item -ItemType Directory -Path dir
- View file content: Get-Content file.txt
- Find in files: Select-String -Path *.txt -Pattern "search"
- Command separator: ; (Always replace && with ;)

# Platform-Specific Command Blocks

These blocks are infilled into the `{{PLATFORM_COMMANDS}}` token in system-prompt.md based on the detected platform.

---

## win32

```
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

### Windows CMD Command Examples
- List files: dir
- Remove file: del file.txt
- Remove directory: rmdir /s /q dir
- Copy file: copy source.txt destination.txt
- Create directory: mkdir dir
- View file content: type file.txt
- Command separator: &
```

---

## darwin

```
Commands MUST be adapted to your macOS system running on darwin with {{SHELL}} shell.

### macOS (Bash/Zsh) Command Examples
- List files: ls -la
- Remove file: rm file.txt
- Remove directory: rm -rf dir
- Copy file: cp source.txt destination.txt
- Copy directory: cp -r source destination
- Create directory: mkdir -p dir
- View file content: cat file.txt
- Find in files: grep -r "search" *.txt
- Command separator: &&
```

---

## linux

```
Commands MUST be adapted to your Linux system running on linux with {{SHELL}} shell.

### Linux (Bash) Command Examples
- List files: ls -la
- Remove file: rm file.txt
- Remove directory: rm -rf dir
- Copy file: cp source.txt destination.txt
- Copy directory: cp -r source destination
- Create directory: mkdir -p dir
- View file content: cat file.txt
- Find in files: grep -r "search" *.txt
- Command separator: &&
```

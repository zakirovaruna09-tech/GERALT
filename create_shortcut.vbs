' ══════════════════════════════════════════════════════════════════════
'  create_shortcut.vbs
'  Создаёт ярлык .lnk на рабочем столе.
'  Аргументы: TargetExe  Arguments  WorkingDir  IconPath  ShortcutPath
'  Вызывается из install.bat — не запускай вручную без аргументов.
' ══════════════════════════════════════════════════════════════════════

If WScript.Arguments.Count < 5 Then
    WScript.Echo "Использование: create_shortcut.vbs <exe> <args> <workdir> <icon> <lnk_path>"
    WScript.Quit 1
End If

targetExe   = WScript.Arguments(0)
targetArgs  = WScript.Arguments(1)
workDir     = WScript.Arguments(2)
iconPath    = WScript.Arguments(3)
shortcutLnk = WScript.Arguments(4)

Set oWS = CreateObject("WScript.Shell")
Set oLink = oWS.CreateShortcut(shortcutLnk)

oLink.TargetPath       = targetExe
oLink.Arguments        = targetArgs
oLink.WorkingDirectory = workDir
oLink.IconLocation     = iconPath & ", 0"
oLink.WindowStyle      = 1
oLink.Description      = "GERALT — Personal AI Assistant"
oLink.Save

WScript.Echo "Ярлык создан: " & shortcutLnk

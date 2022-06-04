
Function FormatNumberLeadingZeros(expr, digits)
    remain = expr

    Do 
        result = CStr(remain mod 10) & result
        remain = remain \ 10
    Loop Until (remain = 0) and (Len(result) >= digits)

    FormatNumberLeadingZeros = result
End Function

Function ExportSlides(ppt_file, out_format, megapixels)

    Set fso = CreateObject("Scripting.FileSystemObject")
    ppt_file_abs = fso.GetAbsolutePathName(ppt_file)

    Set pptApp = CreateObject("PowerPoint.Application")
    Set ppt = pptApp.Presentations.Open(ppt_file_abs, True, , False)

    out_folder = fso.BuildPath(fso.GetParentFolderName(ppt_file_abs), fso.GetBaseName(ppt_file))
    If Not fso.FolderExists(out_folder) Then
        fso.CreateFolder(out_folder)
    End If


    With ppt.PageSetup
        sh = .SlideHeight
        sw = .SlideWidth
    End With

    sA = sh * sw * 4
    ' factor = Sqr(1000000.0 * megapixels / sA)
    factor = 1000000.0 * megapixels / sA
    imageheight = Round(factor * sh, 0)
    imagewidth = Round(factor * sw, 0)
    num_exported = 0

    For Each slide In ppt.Slides
        
        slide.Export fso.BuildPath(out_folder, "img") _
            & FormatNumberLeadingZeros(slide.SlideIndex, 4) _
            & "." & LCase(out_format), _
            out_format, imagewidth, imageheight

        num_exported = num_exported + 1
    Next

    ExportSlides = num_exported
End Function

For Each arg In WScript.Arguments
    ' adjust megapixels here in the last argument
    num_exported = 0
    Set fso = CreateObject("Scripting.FileSystemObject")
    arg_path = fso.GetAbsolutePathName(arg)
    If fso.FileExists(arg_path) Then
        num_exported = num_exported + ExportSlides(arg, "JPG", 4)
    ElseIf fso.FolderExists(arg_path) Then
        Set dir = fso.GetFolder(arg_path)
        For Each f in dir.Files
            If f.attributes = 32 Then
                num_exported = num_exported + ExportSlides(f.Path, "JPG", 4)
            End If
        Next
    End If
    WScript.Echo "Done with ", arg, ". ", num_exported, " slides exported."
Next

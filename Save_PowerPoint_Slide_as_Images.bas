Sub Save_PowerPoint_Slide_as_Images()
    Dim oSlide As Slide '* Slide Object
    On Error GoTo Err_ImageSave

    For Each oSlide In ActivePresentation.Slides
        oSlide.Export ActivePresentation.Path & "\Slide" & Right(String(4, "0") & oSlide.SlideIndex, 4) & ".jpg", "JPG"
    Next oSlide

Err_ImageSave:
    If Err <> 0 Then
    MsgBox Err.Description
    End If
End Sub


Sub Save_PowerPoint_Slide_as_Png()
    Dim oSlide As Slide '* Slide Object
    On Error GoTo Err_ImageSave

    For Each oSlide In ActivePresentation.Slides
        oSlide.Select
        oSlide.Shapes.SelectAll
        Set shGroup = ActiveWindow.Selection.ShapeRange
        shGroup.Export ap.Path & "\Slide" & Right(String(4, "0") & oSlide.SlideIndex, 4) & ".png", ppShapeFormatPNG, , , ppRelativeToSlide
    Next oSlide

Err_ImageSave:
    If Err <> 0 Then
    MsgBox Err.Description
    End If
End Sub


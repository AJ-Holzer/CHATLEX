@REM Clear terminal
cls

@REM Build apk
flet build apk ^
    --description "ZEPHRA -- one of the most secure messengers." ^
    --project "ZEPHRA" ^
    --product "ZEPHRA" ^
    --org "ajservers.site" ^
    --clear-cache ^
    -v
    @REM --android-permissions android.permission.READ_EXTERNAL_STORAGE=True,android.permission.WRITE_EXTERNAL_STORAGE=True,android.permission.INTERNET=True ^

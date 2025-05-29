flet build apk ^
    --description "ZEPHRA -- one of the most secure messengers." ^
    --project "ZEPHRA" ^
    --product "ZEPHRA" ^
    --org "ajservers.site" ^
    --android-permissions android.permission.READ_EXTERNAL_STORAGE=True,android.permission.WRITE_EXTERNAL_STORAGE=True,android.permission.INTERNET=True ^
    --clear-cache ^
    -v

flet build apk ^
    --description "This is a secure messenger app." ^
    --project "ChatLex" ^
    --product "ChatLex" ^
    --org "ajservers.site" ^
    --android-permissions android.permission.READ_EXTERNAL_STORAGE=True,android.permission.WRITE_EXTERNAL_STORAGE=True,android.permission.INTERNET=True ^
    -v

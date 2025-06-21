@REM Clear terminal
cls

@REM Build apk
flet build apk ^
    --description "ZEPHRA -- Secure. Anonymous. Decentralized." ^
    --project "ZEPHRA" ^
    --product "ZEPHRA" ^
    --org "sites.ajservers" ^
    --source-packages certifi pyaes argon2 ^
    --clear-cache ^
    --exclude ".trunk" ^
    -v
    @REM --cleanup-packages ^
    @REM --compile-packages ^
    @REM --android-permissions android.permission.READ_EXTERNAL_STORAGE=True,android.permission.WRITE_EXTERNAL_STORAGE=True,android.permission.INTERNET=True ^

@REM Clear terminal
cls

@REM Build apk
flet build apk ^
    --description "CHATLEX - Secure. Anonymous. Decentralized." ^
    --project "CHATLEX" ^
    --product "CHATLEX" ^
    --org "sites.ajservers" ^
    --source-packages certifi pyaes argon2 ^
    --exclude ".trunk" ^
    -v
    @REM --clear-cache ^
    @REM --cleanup-packages ^
    @REM --compile-packages ^
    @REM --android-permissions android.permission.READ_EXTERNAL_STORAGE=True,android.permission.WRITE_EXTERNAL_STORAGE=True,android.permission.INTERNET=True ^

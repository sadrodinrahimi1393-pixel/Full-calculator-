[app]
title = ماشین‌حساب فوق‌العاده
package.name = calculatorfa
package.domain = org.example
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas
version = 1.0
orientation = portrait
requirements = python3,kivy,sympy,mpmath
android.api = 35
android.minapi = 23
android.sdk = 35
android.ndk = 28c
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = @android:style/Theme.Material.Light.NoActionBar
android.archs = arm64-v8a, armeabi-v7a
fullscreen = 0
android.permissions =
android.allow_backup = True
android.debug_artifact = apk

[buildozer]
log_level = 2
warn_on_root = 1

[app]
title = My Player
package.name = myplayer
package.domain = org.test
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3, kivy==2.3.0, kivymd==1.2.0, ffpyplayer, openssl
orientation = portrait
fullscreen = 0
android.api = 34
android.minapi = 21
android.sdk = 34
android.ndk = 26b
android.private_storage = True
android.permissions = READ_MEDIA_AUDIO, READ_MEDIA_VIDEO, FOREGROUND_SERVICE, WAKE_LOCK
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1

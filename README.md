# ماشین‌حساب فوق‌العاده — Android

نسخه‌ی موبایلی برنامه‌ی Tkinter شما با Kivy آماده شده است.

## ساخت APK در Linux یا WSL2

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev cmake libffi-dev libssl-dev
python3 -m pip install --upgrade pip
python3 -m pip install buildozer cython
buildozer android debug
```

پس از اتمام، APK داخل پوشه `bin/` ساخته می‌شود.

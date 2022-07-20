import zipfile
import os
import platform
if platform.platform() == "Windows":
    renxel = "./dist/renxel.exe"
    renxel_zip = "./dist/renxel-windows.zip"
    zip = zipfile.ZipFile(renxel_zip, "w", zipfile.ZIP_DEFLATED)
    zip.write(renxel, os.path.basename(renxel))
    zip.close()
elif platform.platform() == "Ubuntu":
    renxel = "./dist/renxel"
    renxel_zip = "./dist/renxel-linux.zip"
    zip = zipfile.ZipFile(renxel_zip, "w", zipfile.ZIP_DEFLATED)
    zip.write(renxel, os.path.basename(renxel))
    zip.close()
else:
    print("I can't zip on this OS")

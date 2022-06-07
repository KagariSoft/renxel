import zipfile
import os
renxel = "./dist/renxel"
renxel_zip = "./dist/renxel-linux.zip"
zip = zipfile.ZipFile(renxel_zip, "w", zipfile.ZIP_DEFLATED)
zip.write(renxel, os.path.basename(renxel))
zip.close()

#!/usr/bin/env python

import ghostscript
import sys
import os
import shutil
import locale

class PdfSlidesService:
   def clear_stale_data(self, output_path):
      if(os.path.exists(output_path)):
         shutil.rmtree(output_path)

   def start(self, source_path, output_path):
      if ".pdf" not in source_path:
         return

      if(os.path.exists(output_path)):
         shutil.rmtree(output_path)
      
      os.makedirs(output_path)
         
      args = ['pdf2jpeg',
            '-dNOPAUSE', '-dBATCH', '-dSAFER',
            '-sDEVICE=png16m',
            '-r50x50',
            '-sOutputFile=' + output_path + '/page-%03d.jpg',
            source_path]

      encoding = locale.getpreferredencoding()
      args = [a.encode(encoding) for a in args]

      ghostscript.Ghostscript(*args)
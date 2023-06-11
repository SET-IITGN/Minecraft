import re
import subprocess
from typing import Literal

def git_diff(repo_path: Literal["Git repository path"], commit_1:Literal['Commit 1'], 
             commit_2:Literal['Commit 2'], file_path:Literal['File path to do fit diff on']):
    ''''
    return git diff of two commits.
    Commit 1 and Commit 2 arre hashes
    '''
    # print(commit_1, commit_2, file_path)
    cmd = ['git', 'diff',commit_1, commit_2, file_path]
    result = subprocess.run(cmd, cwd=repo_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8')





def get_pairs(diff:str, output='number'):
    '''
    returns pairs of deletions and addition
    when diff output is provided as input 
    output [optional]: default is number, 
    if you need pair of added and deleted line
    use line
    '''
    

    deletion_regex = r'^-(?![\s+]).*'
    addition_regex = r'^\+(?![\s-]).*'
    pairs = []
    current_pair = []
    is_negative = False
    is_positive = False
    line_no = 1
    at_found = False
    for line in diff.splitlines():    
        # try:
        #     print(line_no_old, line_no_new,line)
        # except:
        #     pass
        if line.startswith("@@"):
            at_found = True
            line_no = int(re.findall(r"\+(\d+)", line)[0])
            line_no_new = int(line.split('+')[1].split(',')[0])
            line_no_old = int(line.split('-')[1].split(',')[0])
            # print(line_no_old, line_no_new)
            if current_pair:
                current_pair[1] = current_pair[1].rstrip(", ")
                pairs.append(current_pair)
            current_pair = []
            is_negative = False
            is_positive = False
        elif line.startswith("-") and not line.startswith("---"):
            if not is_negative:
                current_pair = [str(line_no_old), ""]
                is_negative = True
            elif is_negative and not is_positive:
                current_pair[0] += ", " + str(line_no_old)
            elif is_negative and is_positive:
                current_pair[1] = current_pair[1].rstrip(", ")
                pairs.append(current_pair)
                current_pair = [str(line_no_old), ""]
                is_positive = False
            line_no_old += 1
            
                
        elif line.startswith("+") and not line.startswith("+++") and is_negative:

            is_positive = True
            if is_negative and is_positive:
                
                current_pair[1] += str(line_no_new)+", "
            line_no_new += 1
            
        elif line == '\ No newline at end of file':
            continue
        elif line.startswith("+") and not line.startswith("+++") and not is_negative:
            line_no_new += 1
        elif at_found:
            line_no_new += 1
            line_no_old += 1

    # Process the last pair if any
    if current_pair:
        current_pair[1] = current_pair[1].rstrip(", ")
        pairs.append(current_pair)
    
    # Print all the pairs
    del_add=[]
    for pair in pairs:
        deletion, addition = pair
        if addition and deletion:
            del_add.append([deletion,addition])
    return del_add

diff = '''diff --git a/geocoder/bing_batch_reverse.py b/geocoder/bing_batch_reverse.py
index 1350efc..09bbd16 100644
--- a/geocoder/bing_batch_reverse.py
+++ b/geocoder/bing_batch_reverse.py
@@ -2,56 +2,95 @@
 # coding: utf8
 
 from __future__ import absolute_import, print_function
-from geocoder.bing_batch import BingBatch, BingBatchResult
+from geocoder.base import OneResult
+from geocoder.bing_batch import BingBatch
+
 import io
 import csv
+import sys
+
+PY2 = sys.version_info < (3, 0)
+csv_io = io.BytesIO if PY2 else io.StringIO
+csv_encode = (lambda input: input) if PY2 else (lambda input: input.encode('utf-8'))
+csv_decode = (lambda input: input) if PY2 else (lambda input: input.decode('utf-8'))
 
 
-class BingBatchReverseResult(BingBatchResult):
+class BingBatchReverseResult(OneResult):
+
+    def __init__(self, content):
+        self._content = content
 
     @property
     def address(self):
-        coord = self._content
-        if coord:
-            return coord[0]
+        address = self._content
+        if address:
+            return address[0]
 
     @property
     def city(self):
-        coord = self._content
-        if coord:
-            return coord[1]
+        city = self._content
+        if city:
+            return city[1]
 
     @property
     def postal(self):
-        coord = self._content
-        if coord:
-            return coord[2]
+        postal = self._content
+        if postal:
+            return postal[2]
 
     @property
     def state(self):
-        coord = self._content
-        if coord:
-            return coord[3]
+        state = self._content
+        if state:
+            return state[3]
 
     @property
     def country(self):
-        coord = self._content
-        if coord:
-            return coord[4]
+        country = self._content
+        if country:
+            return country[4]
 
     @property
     def ok(self):
         return bool(self._content)
 
+    def debug(self, verbose=True):
+        with csv_io() as output:
+            print('\n', file=output)
+            print('Bing Batch result\n', file=output)
+            print('-----------\n', file=output)
+            print(self._content, file=output)
 
-class BingBatchReverse(BingBatch):
+            if verbose:
+                print(output.getvalue())
 
+            return [None, None]
+
+
+class BingBatchReverse(BingBatch):
+    """
+    Bing Maps REST Services
+    =======================
+    The Bing™ Maps REST Services Application Programming Interface (API)
+    provides a Representational State Transfer (REST) interface to
+    perform tasks such as creating a static map with pushpins, geocoding
+    an address, retrieving imagery metadata, or creating a route.
+
+    API Reference
+    -------------
+    http://msdn.microsoft.com/en-us/library/ff701714.aspx
+
+    Dataflow Reference
+    ------------------
+    https://msdn.microsoft.com/en-us/library/ff701733.aspx
+
+    """
     method = 'batch_reverse'
 
     _RESULT_CLASS = BingBatchReverseResult
 
     def generate_batch(self, locations):
-        out = io.BytesIO()
+        out = csv_io()
         writer = csv.writer(out)
         writer.writerow([
             'Id',
@@ -61,31 +100,31 @@ class BingBatchReverse(BingBatch):
             'GeocodeResponse/Address/Locality',
             'GeocodeResponse/Address/PostalCode',
             'GeocodeResponse/Address/AdminDistrict',
-            'GeocodeResponse/Address/CountryRegion',
+            'GeocodeResponse/Address/CountryRegion'
         ])
 
         for idx, location in enumerate(locations):
             writer.writerow([idx, location[0], location[1], None, None, None, None, None])
 
-        return "Bing Spatial Data Services, 2.0\n{}".format(out.getvalue())
+        return csv_encode("Bing Spatial Data Services, 2.0\n{}".format(out.getvalue()))
 
     def _adapt_results(self, response):
-        result = io.BytesIO(response)
+        # print(type(response))
+        result = csv_io(csv_decode(response))
         # Skipping first line with Bing header
         next(result)
 
         rows = {}
         for row in csv.DictReader(result):
-            rows[row['Id']] = [
-                row['GeocodeResponse/Address/FormattedAddress'],
-                row['GeocodeResponse/Address/Locality'],
-                row['GeocodeResponse/Address/PostalCode'],
-                row['GeocodeResponse/Address/AdminDistrict'],
-                row['GeocodeResponse/Address/CountryRegion']
-            ]
+            rows[row['Id']] = [row['GeocodeResponse/Address/FormattedAddress'],
+                               row['GeocodeResponse/Address/Locality'],
+                               row['GeocodeResponse/Address/PostalCode'],
+                               row['GeocodeResponse/Address/AdminDistrict'],
+                               row['GeocodeResponse/Address/CountryRegion']]
 
         return rows
 
+
 if __name__ == '__main__':
     g = BingBatchReverse((40.7943, -73.970859), (48.845580, 2.321807), key=None)
     g.debug()
'''
# for deletion, addition in get_pairs(diff):
#     print("Deletion:", deletion)
#     print("Addition:", addition)
#     print()
import re

import torch
from transformers import T5ForConditionalGeneration, RobertaTokenizer


tokenizer = RobertaTokenizer.from_pretrained("mamiksik/CommitPredictorT5PL", revision="fb08d01")
model = T5ForConditionalGeneration.from_pretrained("mamiksik/CommitPredictorT5PL", revision="fb08d01")


def parse_files(patch):
    accumulator = []
    lines = patch.splitlines()

    filename_before = None
    for line in lines:
        if line.startswith("index") or line.startswith("diff"):
            continue
        if line.startswith("---"):
            try:
                filename_before = line.split(" ", 1)[1][1:]
            except:
                continue

        if line.startswith("+++"):
            try:
                filename_after = line.split(" ", 1)[1][1:]
            except:
                continue
            if filename_before == filename_after:
                accumulator.append(f"<ide><path>{filename_before}")
            else:
                accumulator.append(f"<add><path>{filename_after}")
                accumulator.append(f"<del><path>{filename_before}")
            continue

        line = re.sub("@@[^@@]*@@", "", line)
        if len(line) == 0:
            continue

        if line[0] == "+":
            line = line.replace("+", "<add>", 1)
        elif line[0] == "-":
            line = line.replace("-", "<del>", 1)
        else:
            line = f"<ide>{line}"

        accumulator.append(line)

    return '\n'.join(accumulator)


def predict_msg(patch, max_length, min_length, num_beams, prediction_count):
    input_text = parse_files(patch)
    with torch.no_grad():
        token_count = tokenizer(input_text, return_tensors="pt").input_ids.shape[1]

        input_ids = tokenizer(
            input_text,
            truncation=True,
            padding=True,
            return_tensors="pt",
        ).input_ids

        outputs = model.generate(
            input_ids,
            max_length=max_length,
            min_length=min_length,
            num_beams=num_beams,
            num_return_sequences=prediction_count,
        )

    result = tokenizer.batch_decode(outputs, skip_special_tokens=True)
    return result[0]

def predict(patch):
    return predict_msg(patch, max_length=40, min_length=5, num_beams=7, prediction_count=1)


if __name__ == '__main__':
    patch = """
diff --git a/geocoder/location.py b/geocoder/location.py
index 46983a1..e1beccf 100644
--- a/geocoder/location.py
+++ b/geocoder/location.py
@@ -168,10 +168,10 @@ class BBox(object):
     def __init__(self, bbox=None, bounds=None,
                  lat=None, lng=None,
                  west=None, south=None, east=None, north=None):
-        if bounds is not None:
+        if bounds is not None and bounds.get('southwest') and bounds.get('northeast'):
             self.south, self.west = map(float, bounds['southwest'])
             self.north, self.east = map(float, bounds['northeast'])
-        elif bbox is not None:
+        elif bbox is not None and all(bbox):
             self.west, self.south, self.east, self.north = map(float, bbox)
         elif lat is not None and lng is not None:
             self.south = float(lat) - self.DEGREES_TOLERANCE
"""
    print(predict(patch, max_length=40, min_length=5, num_beams=7, prediction_count=1))


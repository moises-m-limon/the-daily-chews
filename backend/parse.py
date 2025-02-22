import re
import pandas as pd

# Read the TextGrid content from a file
file_path = "alignment_output/1740262481.TextGrid"

with open(file_path, "r", encoding="utf-8") as file:
    textgrid_content = file.read()

# Regular expression to extract only the "words" tier and stop reading at "phones" tier
pattern_words = re.compile(
    r"item \[1\]:\s*class = \"IntervalTier\"\s*name = \"words\"(.*?)item \[2\]:",
    re.DOTALL
)

# Extract only the relevant section of the "words" tier
match_words = pattern_words.search(textgrid_content)
if match_words:
    words_section = match_words.group(1)
else:
    words_section = ""

# Regular expression pattern to extract xmin, xmax, and text from "words" tier
pattern_intervals = re.compile(
    r"intervals \[\d+\]:\s*"
    r"xmin = ([\d\.]+)\s*"
    r"xmax = ([\d\.]+)\s*"
    r'text = "(.*?)"',
    re.DOTALL
)

# Extract matches from the words section
matches = pattern_intervals.findall(words_section)

# Convert to DataFrame
df_parsed = pd.DataFrame(matches, columns=["start", "stop", "text"])

# Convert start and stop to float
df_parsed["start"] = df_parsed["start"].astype(float)
df_parsed["stop"] = df_parsed["stop"].astype(float)

# Remove empty text entries
df_parsed = df_parsed[df_parsed["text"].str.strip() != ""]

# Convert to list of tuples for captions format
captions = list(df_parsed.itertuples(index=False, name=None))
# import os
# import re
# import pandas as pd

# # ✅ Directory where alignment TextGrid files are stored
# alignment_dir = "alignment_output"

# # ✅ Find the latest .TextGrid file
# textgrid_files = [f for f in os.listdir(
#     alignment_dir) if f.endswith(".TextGrid")]
# if not textgrid_files:
#     raise FileNotFoundError("❌ No .TextGrid files found in alignment_output")

# print(textgrid_files)

# latest_textgrid_file = max(
#     textgrid_files, key=lambda f: os.path.getctime(os.path.join(alignment_dir, f)))
# textgrid_path = os.path.join(alignment_dir, latest_textgrid_file)

# # ✅ Read the TextGrid content
# with open(textgrid_path, "r", encoding="utf-8") as file:
#     textgrid_content = file.read()

# # ✅ Regular expression to extract only the "words" tier and stop reading at "phones" tier
# pattern_words = re.compile(
#     r"item \[1\]:\s*class = \"IntervalTier\"\s*name = \"words\"(.*?)item \[2\]:",
#     re.DOTALL
# )

# # ✅ Extract only the relevant section of the "words" tier
# match_words = pattern_words.search(textgrid_content)
# words_section = match_words.group(1) if match_words else ""

# # ✅ Regular expression pattern to extract xmin, xmax, and text
# pattern_intervals = re.compile(
#     r"intervals \[\d+\]:\s*"
#     r"xmin = ([\d\.]+)\s*"
#     r"xmax = ([\d\.]+)\s*"
#     r'text = "(.*?)"',
#     re.DOTALL
# )

# # ✅ Extract matches from the words section
# matches = pattern_intervals.findall(words_section)

# # ✅ Convert to DataFrame
# df_parsed = pd.DataFrame(matches, columns=["start", "stop", "text"])

# # ✅ Convert start and stop times to float
# df_parsed["start"] = df_parsed["start"].astype(float)
# df_parsed["stop"] = df_parsed["stop"].astype(float)

# # ✅ Remove empty text entries
# df_parsed = df_parsed[df_parsed["text"].str.strip() != ""]

# # ✅ Convert to list of tuples for captions format
# captions = list(df_parsed.itertuples(index=False, name=None))

# print(captions)

# print(f"✅ Parsed {len(captions)} captions from {latest_textgrid_file}:")
# print(captions)

import os
import shutil
import csv

# === CONFIGURATION ===
evaluation_csv = 'evaluation_no_blur_final.csv'
labels_csv = 'image_labels.csv'
image_folder = 'new_evaluation_no_blur'
output_folder = 'final_evaluation_no_blur'
output_csv = 'final_image_labels.csv'

# === Prepare ===
os.makedirs(output_folder, exist_ok=True)

# === Step 1: Load all label data ===
label_map = {}
with open(labels_csv, newline='', encoding='utf-8') as lf:
    reader = csv.DictReader(lf)
    for row in reader:
        # Assuming image_labels.csv already has just the basename, e.g., '0.jpg'
        name = row['file_path'].strip().lower() # No need for os.path.basename here
        label_map[name] = row['label_text'].strip()

# === Step 2: Read evaluation CSV and normalize filenames ===
selected_files_with_original_paths = [] # Store original path to find the image later
with open(evaluation_csv, newline='', encoding='utf-8') as ef:
    reader = csv.DictReader(ef)
    for row in reader:
        original_full_path = row['file_path'].strip()
        filename = os.path.basename(original_full_path).strip().lower()
        selected_files_with_original_paths.append({'filename': filename, 'original_full_path': original_full_path})

# === Step 3: Match and copy ===
output_data = []
missing = 0
index = 0

for item in selected_files_with_original_paths:
    fname = item['filename']
    original_full_path = item['original_full_path']

    if fname not in label_map:
        print(f"No label found for {fname}")
        missing += 1
        continue

    # Use the original full path to construct the source path
    # Assuming new_evaluation_no_blur is the parent directory of these images
    src = os.path.join(image_folder, fname)
    if not os.path.exists(src):
        print(f"Image file not found: {src}")
        continue

    new_name = f"{index}.jpg"
    shutil.copyfile(src, os.path.join(output_folder, new_name))
    output_data.append({'file_path': new_name, 'label_text': label_map[fname]})
    index += 1

# === Step 4: Write new labels CSV ===
with open(output_csv, 'w', newline='', encoding='utf-8') as out_csv:
    writer = csv.DictWriter(out_csv, fieldnames=['file_path', 'label_text'])
    writer.writeheader()
    writer.writerows(output_data)

print(f"\nCopied {index} images to '{output_folder}' and wrote labels to '{output_csv}'")
print(f"{missing} images were skipped due to missing labels.")
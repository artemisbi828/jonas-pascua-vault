
New-Item -ItemType Directory -Path "testing_artifacts" -Force
Move-Item -Path "debug_pdf_text.py", "debug_table_extract.py" -Destination "testing_artifacts\" -Force
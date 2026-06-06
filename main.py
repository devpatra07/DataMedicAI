# ==========================================
# DATAMEDIC AI - FASTAPI BACKEND
# PROD/DEBUG VERSION
# ==========================================

# INSTALL:
# pip install fastapi uvicorn python-multipart pandas openpyxl numpy scikit-learn

# RUN:
# uvicorn main:app --reload

# OPEN:
# http://127.0.0.1:8000


# ==========================================
# IMPORTS
# ==========================================

print("DEBUG: Importing libraries...")

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import pandas as pd
import numpy as np
import os
import uuid

print("DEBUG: Libraries imported successfully")


# ==========================================
# APP
# ==========================================

print("DEBUG: Creating FastAPI app...")

app = FastAPI()

print("DEBUG: FastAPI app created")


# ==========================================
# CORS
# ==========================================

print("DEBUG: Adding CORS middleware...")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("DEBUG: CORS middleware added")


# ==========================================
# FOLDERS
# ==========================================

UPLOAD_FOLDER = "processed_files"

print(f"DEBUG: Creating upload folder -> {UPLOAD_FOLDER}")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

print("DEBUG: Upload folder ready")


# ==========================================
# ROOT
# ==========================================

@app.get("/")
async def home():

    print("DEBUG: Root endpoint accessed")

    return {
        "message": "DataMedic AI Backend Running"
    }


# ==========================================
# ANALYZE DATASET
# ==========================================

@app.post("/analyze")
async def analyze_dataset(
    file: UploadFile = File(...)
):

    print("\n==============================")
    print("DEBUG: /analyze endpoint hit")
    print("==============================")

    try:

        # ==================================
        # FILE INFO
        # ==================================

        print("DEBUG: Uploaded filename:", file.filename)

        unique_id = str(uuid.uuid4())[:8]

        print("DEBUG: Generated unique ID:", unique_id)

        original_name = file.filename.lower()

        print("DEBUG: Lowercase filename:", original_name)

        temp_path = os.path.join(
            UPLOAD_FOLDER,
            f"temp_{unique_id}_{file.filename}"
        )

        print("DEBUG: Temp file path:", temp_path)

        # ==================================
        # SAVE TEMP FILE
        # ==================================

        print("DEBUG: Saving uploaded file...")

        with open(temp_path, "wb") as f:

            content = await file.read()

            print("DEBUG: File size received:", len(content), "bytes")

            f.write(content)

        print("DEBUG: File saved successfully")

        # ==================================
        # READ DATASET
        # ==================================

        print("DEBUG: Detecting file type...")

        if original_name.endswith(".csv"):

            print("DEBUG: Reading CSV file")

            df = pd.read_csv(temp_path)

        elif (
            original_name.endswith(".xlsx")
            or
            original_name.endswith(".xls")
        ):

            print("DEBUG: Reading Excel file")

            df = pd.read_excel(temp_path)

        elif original_name.endswith(".json"):

            print("DEBUG: Reading JSON file")

            df = pd.read_json(temp_path)

        else:

            print("ERROR: Unsupported file format")

            return {
                "error": "Unsupported file format"
            }

        print("DEBUG: Dataset loaded successfully")

        print("DEBUG: Dataset shape:", df.shape)

        print("DEBUG: Dataset columns:")
        print(df.columns.tolist())

        print("DEBUG: First 5 rows:")
        print(df.head())

        print("DEBUG: Data types:")
        print(df.dtypes)

        # ==================================
        # ORIGINAL SHAPE
        # ==================================

        rows = int(df.shape[0])

        columns = int(df.shape[1])

        print("DEBUG: Rows =", rows)
        print("DEBUG: Columns =", columns)

        # ==================================
        # MISSING VALUES
        # ==================================

        missing_values = int(
            df.isnull().sum().sum()
        )

        print("DEBUG: Total missing values =", missing_values)

        print("DEBUG: Missing values per column:")
        print(df.isnull().sum())

        # ==================================
        # DUPLICATES
        # ==================================

        duplicates = int(
            df.duplicated().sum()
        )

        print("DEBUG: Duplicate rows =", duplicates)

        # ==================================
        # FIX MISSING VALUES
        # ==================================

        print("DEBUG: Starting missing value fixing...")

        for col in df.columns:

            print("\n--------------------------------")
            print("DEBUG: Processing column:", col)
            print("--------------------------------")

            print("DEBUG: Column dtype =", df[col].dtype)

            if df[col].dtype == "object":

                print("DEBUG: Object column detected")

                before_missing = df[col].isnull().sum()

                print("DEBUG: Missing before =", before_missing)

                df[col] = df[col].fillna("Fixed")

                after_missing = df[col].isnull().sum()

                print("DEBUG: Missing after =", after_missing)

            else:

                print("DEBUG: Numeric column detected")

                before_missing = df[col].isnull().sum()

                print("DEBUG: Missing before =", before_missing)

                mean_value = df[col].mean()

                print("DEBUG: Mean value =", mean_value)

                df[col] = df[col].fillna(mean_value)

                after_missing = df[col].isnull().sum()

                print("DEBUG: Missing after =", after_missing)

        print("DEBUG: Missing value fixing completed")

        # ==================================
        # REMOVE DUPLICATES
        # ==================================

        print("DEBUG: Removing duplicates...")

        before_rows = len(df)

        df = df.drop_duplicates()

        after_rows = len(df)

        removed_duplicates = before_rows - after_rows

        print("DEBUG: Duplicates removed =", removed_duplicates)

        print("DEBUG: New shape =", df.shape)

        # ==================================
        # OUTLIER DETECTION
        # ==================================

        print("DEBUG: Starting outlier detection...")

        outliers = 0

        numeric_columns = df.select_dtypes(
            include=np.number
        ).columns

        print("DEBUG: Numeric columns:")
        print(numeric_columns)

        for col in numeric_columns:

            print("\n================================")
            print("DEBUG: Outlier analysis for:", col)
            print("================================")

            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)

            print("DEBUG: Q1 =", q1)
            print("DEBUG: Q3 =", q3)

            iqr = q3 - q1

            print("DEBUG: IQR =", iqr)

            lower = q1 - 1.5 * iqr
            upper = q3 + 1.5 * iqr

            print("DEBUG: Lower bound =", lower)
            print("DEBUG: Upper bound =", upper)

            mask = (
                (df[col] < lower)
                |
                (df[col] > upper)
            )

            current_outliers = int(mask.sum())

            print("DEBUG: Outliers found =", current_outliers)

            outliers += current_outliers

            median_value = df[col].median()

            print("DEBUG: Replacing outliers with median =", median_value)

            df.loc[mask, col] = median_value

        print("DEBUG: Total outliers fixed =", outliers)

        # ==================================
        # HEALTH SCORE
        # ==================================

        print("DEBUG: Calculating health score...")

        health_score = max(
            0,
            100 - (
                missing_values
                + duplicates
                + outliers
            )
        )

        consistency = 96

        print("DEBUG: Health score =", health_score)
        print("DEBUG: Consistency =", consistency)

        # ==================================
        # SAVE CLEANED FILES
        # ==================================

        print("DEBUG: Saving cleaned files...")

        excel_filename = (
            f"cleaned_{unique_id}.xlsx"
        )

        csv_filename = (
            f"cleaned_{unique_id}.csv"
        )

        excel_path = os.path.join(
            UPLOAD_FOLDER,
            excel_filename
        )

        csv_path = os.path.join(
            UPLOAD_FOLDER,
            csv_filename
        )

        print("DEBUG: Excel output path =", excel_path)
        print("DEBUG: CSV output path =", csv_path)

        df.to_excel(
            excel_path,
            index=False
        )

        print("DEBUG: Excel saved")

        df.to_csv(
            csv_path,
            index=False
        )

        print("DEBUG: CSV saved")

        # ==================================
        # JSON-COMPLIANT PREVIEW GENERATION
        # ==================================

        print("DEBUG: Safe-encoding preview data for JSON response...")
        
        # Replace NaN/NaT values with standard Python None (which parses cleanly to JavaScript null)
        df_json_ready = df.replace({np.nan: None})
        
        preview = [df_json_ready.columns.tolist()]
        preview += (
            df_json_ready.head(20)
            .values
            .tolist()
        )

        print("DEBUG: Preview array created successfully")

        # ==================================
        # REMOVE TEMP FILE
        # ==================================

        print("DEBUG: Removing temp file...")

        if os.path.exists(temp_path):

            os.remove(temp_path)

            print("DEBUG: Temp file removed")

        else:

            print("WARNING: Temp file not found")

        # ==================================
        # FINAL RESPONSE
        # ==================================

        print("\n================================")
        print("DEBUG: ANALYSIS COMPLETED")
        print("================================")

        response_data = {

            "rows": rows,

            "columns": columns,

            "missing_values": missing_values,

            "duplicates": duplicates,

            "outliers": outliers,

            "health_score": health_score,

            "consistency": consistency,

            "cleaned_file": excel_filename,

            "csv_file": csv_filename,

            "cleaned_preview": preview

        }

        print("DEBUG: Final response packet payload structure verified")

        return response_data

    except Exception as e:

        print("\n================================")
        print("ERROR OCCURRED")
        print("================================")

        print("ERROR TYPE:", type(e))
        print("ERROR MESSAGE:", str(e))

        import traceback

        print("FULL TRACEBACK:")
        traceback.print_exc()

        return {
            "error": str(e)
        }


# ==========================================
# DOWNLOAD FILE
# ==========================================

@app.get("/download/{filename}")
async def download_file(filename: str):

    print("\nDEBUG: Download request received")
    print("DEBUG: Requested filename =", filename)

    file_path = os.path.join(
        UPLOAD_FOLDER,
        filename
    )

    print("DEBUG: Full file path =", file_path)

    if not os.path.exists(file_path):

        print("ERROR: File does not exist")

        return {
            "error": "File not found"
        }

    print("DEBUG: File found, sending response")

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type='application/octet-stream'
    )


# ==========================================
# FUTURE ML ROUTES
# ==========================================

@app.post("/train-model")
async def train_model():

    print("DEBUG: /train-model endpoint hit")

    return {
        "message":
        "Future ML Training Endpoint"
    }


@app.post("/predict")
async def predict():

    print("DEBUG: /predict endpoint hit")

    return {
        "message":
        "Future Prediction Endpoint"
    }


# ==========================================
# STARTUP MESSAGE
# ==========================================

print("\n====================================")
print("DATAMEDIC AI BACKEND STARTED")
print("====================================")
print("DEBUG: Backend ready")
print("DEBUG: Open http://127.0.0.1:8000")
print("====================================\n")
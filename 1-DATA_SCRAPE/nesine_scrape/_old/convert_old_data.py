"""
Script to convert old data format to new format:
- Extract week numbers only for "Hafta" column
- Add year to "Tarih" column based on "Hafta" date range
"""
import pandas as pd
import re
from pathlib import Path

# File paths
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "fikstur_tum_ligler_all_seasons.xlsx"
OUTPUT_FILE = SCRIPT_DIR / "fikstur_tum_ligler_all_seasons_converted.xlsx"
CSV_OUTPUT_FILE = OUTPUT_FILE.with_suffix(".csv")


def extract_year_from_week(week_name, date_str):
    """
    Extract the year from week_name (format: '1 (5.08.2022 - 7.08.2022)')
    and add it to date_str (format: '05/08').
    Handles cases where a week spans two different years.
    Returns date in format 'DD/MM/YYYY' or original date_str if parsing fails.
    """
    if not week_name or not date_str:
        return date_str
    
    # Convert to string if not already
    week_name = str(week_name)
    date_str = str(date_str)
    
    # Try to extract date range from week_name
    # Format: "1 (5.08.2022 - 7.08.2022)" or "1 (28.12.2024 - 2.01.2025)"
    date_range_match = re.search(r'\((\d{1,2}\.\d{2}\.\d{4})\s*-\s*(\d{1,2}\.\d{2}\.\d{4})\)', week_name)
    
    if not date_range_match:
        return date_str
    
    start_date_str = date_range_match.group(1)  # e.g., "5.08.2022"
    end_date_str = date_range_match.group(2)    # e.g., "7.08.2022"
    
    # Parse the date_str (format: "05/08" or "DD/MM")
    date_match = re.match(r'(\d{2})/(\d{2})', date_str)
    if not date_match:
        return date_str
    
    day = date_match.group(1)
    month = date_match.group(2)
    
    # Parse start and end dates from week_name
    start_parts = start_date_str.split('.')  # [day, month, year]
    end_parts = end_date_str.split('.')      # [day, month, year]
    
    if len(start_parts) != 3 or len(end_parts) != 3:
        return date_str
    
    start_month = start_parts[1].zfill(2)
    start_year = start_parts[2]
    end_month = end_parts[1].zfill(2)
    end_year = end_parts[2]
    
    # Determine which year to use based on the month
    if month == start_month:
        year = start_year
    elif month == end_month:
        year = end_year
    else:
        # If the month doesn't match either, try to infer
        # This handles edge cases
        month_int = int(month)
        start_month_int = int(start_month)
        end_month_int = int(end_month)
        
        # If week spans two years, pick the appropriate year
        if start_year != end_year:
            if month_int == 12 or month_int >= start_month_int:
                year = start_year
            else:
                year = end_year
        else:
            year = start_year
    
    return f"{day}/{month}/{year}"


def extract_week_number_only(week_name):
    """
    Extract just the week number from week_name.
    Format: '1 (5.08.2022 - 7.08.2022)' -> '1'
    Returns the week number as a string, or the original week_name if no number found.
    """
    if not week_name:
        return week_name
    
    # Convert to string if not already
    week_name = str(week_name)
    
    # Extract the number before the parenthesis
    match = re.match(r'^(\d+)\s*\(', week_name)
    if match:
        return match.group(1)
    
    # Fallback: try to extract any number
    match = re.search(r'(\d+)', week_name)
    if match:
        return match.group(1)
    
    return week_name


def normalize_season_format(season_str):
    """
    Convert season format from '2024-25' to '2024/2025'.
    Also handles formats like '2024/25', '2024 25', and already correct '2024/2025'.
    Returns the normalized season string.
    """
    if not season_str or pd.isna(season_str):
        return season_str
    
    # Convert to string
    season_str = str(season_str).strip()
    
    # Pattern: YYYY-YY or YYYY/YY or YYYY YY (where YY is 2 digits)
    match = re.match(r'^(\d{4})[\-/\s](\d{2})$', season_str)
    if match:
        start_year = int(match.group(1))
        end_year_short = match.group(2)
        
        # Calculate full end year
        base_century = (start_year // 100) * 100
        end_year = base_century + int(end_year_short)
        
        # If end year is less than or equal to start year, add 100
        if end_year <= start_year:
            end_year += 100
        
        return f"{start_year}/{end_year}"
    
    # Pattern: YYYY-YYYY or YYYY/YYYY (already has 4 digit end year)
    match = re.match(r'^(\d{4})[\-/\s](\d{4})$', season_str)
    if match:
        start_year = match.group(1)
        end_year = match.group(2)
        return f"{start_year}/{end_year}"
    
    # Return as-is if no pattern matches
    return season_str


def convert_data(input_path, output_path, csv_output_path):
    """
    Convert old data format to new format.
    """
    print(f"Reading data from: {input_path}")
    
    # Read the Excel file
    try:
        df = pd.read_excel(input_path)
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
        return False
    
    print(f"Loaded {len(df)} rows")
    print(f"Columns: {df.columns.tolist()}")
    
    # Check if required columns exist
    if 'Hafta' not in df.columns or 'Tarih' not in df.columns:
        print("Error: Required columns 'Hafta' and 'Tarih' not found!")
        return False
    
    # Determine the season column name
    season_col = 'Season' if 'Season' in df.columns else 'season_year'
    if season_col not in df.columns:
        print("Warning: No season column found!")
        season_col = None
    
    # Create a copy for conversion
    df_converted = df.copy()
    
    # Convert season format first
    if season_col:
        print(f"\nConverting season format in column '{season_col}'...")
        df_converted[season_col] = df_converted[season_col].apply(normalize_season_format)
        print("✓ Season format converted")
    
    # Convert each row
    print("\nConverting Hafta and Tarih columns...")
    converted_count = 0
    skipped_count = 0
    
    for idx, row in df_converted.iterrows():
        week_name = row['Hafta']
        date_str = row['Tarih']
        
        # Skip if already converted (week is just a number)
        if pd.notna(week_name) and re.match(r'^\d+$', str(week_name).strip()):
            # Check if date already has year
            if pd.notna(date_str) and re.match(r'\d{2}/\d{2}/\d{4}', str(date_str)):
                skipped_count += 1
                continue
        
        # Convert Hafta to just week number
        if pd.notna(week_name):
            df_converted.at[idx, 'Hafta'] = extract_week_number_only(week_name)
        
        # Convert Tarih to include year
        if pd.notna(date_str) and pd.notna(week_name):
            df_converted.at[idx, 'Tarih'] = extract_year_from_week(week_name, date_str)
            converted_count += 1
        
        # Progress indicator
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1} rows...")
    
    print(f"\nConversion complete:")
    print(f"  - Converted: {converted_count} rows")
    print(f"  - Skipped (already converted): {skipped_count} rows")
    print(f"  - Total: {len(df_converted)} rows")
    
    # Save to Excel
    print(f"\nSaving to Excel: {output_path}")
    df_converted.to_excel(output_path, index=False, engine='openpyxl')
    print("✓ Excel file saved")
    
    # Save to CSV
    print(f"Saving to CSV: {csv_output_path}")
    df_converted.to_csv(csv_output_path, index=False)
    print("✓ CSV file saved")
    
    # Show sample of converted data
    print("\nSample of converted data (first 5 rows):")
    # Use the actual column name (season_year or Season)
    if season_col:
        display_cols = [season_col, 'Lig', 'Hafta', 'Tarih', 'EvSahibi', 'Deplasman']
    else:
        display_cols = ['Lig', 'Hafta', 'Tarih', 'EvSahibi', 'Deplasman']
    print(df_converted[display_cols].head())
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Converting old data format to new format")
    print("=" * 60)
    print()
    
    success = convert_data(INPUT_FILE, OUTPUT_FILE, CSV_OUTPUT_FILE)
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Conversion completed successfully!")
        print("=" * 60)
        print(f"\nOutput files:")
        print(f"  - Excel: {OUTPUT_FILE}")
        print(f"  - CSV: {CSV_OUTPUT_FILE}")
        print("\nTo replace the original file, run:")
        print(f"  mv {OUTPUT_FILE} {INPUT_FILE}")
        print(f"  mv {CSV_OUTPUT_FILE} {INPUT_FILE.with_suffix('.csv')}")
    else:
        print("\n" + "=" * 60)
        print("✗ Conversion failed!")
        print("=" * 60)

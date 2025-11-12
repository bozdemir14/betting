"""
Script to remove all matches where Kod != "MS" from the existing data file.
"""
import pandas as pd
from pathlib import Path

# File paths
SCRIPT_DIR = Path(__file__).parent
INPUT_FILE = SCRIPT_DIR / "fikstur_tum_ligler_all_seasons.xlsx"
OUTPUT_FILE = SCRIPT_DIR / "fikstur_tum_ligler_all_seasons_cleaned.xlsx"
CSV_OUTPUT_FILE = OUTPUT_FILE.with_suffix(".csv")


def clean_non_ms_matches(input_path, output_path, csv_output_path):
    """
    Remove all rows where Kod != "MS".
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
    
    # Check if Kod column exists
    if 'Kod' not in df.columns:
        print("Error: 'Kod' column not found!")
        return False
    
    # Show current Kod distribution
    print("\nCurrent Kod distribution:")
    print(df['Kod'].value_counts())
    
    # Count rows before filtering
    total_before = len(df)
    
    # Filter to keep only MS matches
    df_cleaned = df[df['Kod'] == 'MS'].copy()
    
    # Count rows after filtering
    total_after = len(df_cleaned)
    removed_count = total_before - total_after
    
    print(f"\nFiltering results:")
    print(f"  - Total rows before: {total_before}")
    print(f"  - Total rows after: {total_after}")
    print(f"  - Rows removed: {removed_count}")
    
    if removed_count == 0:
        print("\n✓ No non-MS matches found. File is already clean!")
        return True
    
    # Save to Excel
    print(f"\nSaving to Excel: {output_path}")
    df_cleaned.to_excel(output_path, index=False, engine='openpyxl')
    print("✓ Excel file saved")
    
    # Save to CSV
    print(f"Saving to CSV: {csv_output_path}")
    df_cleaned.to_csv(csv_output_path, index=False)
    print("✓ CSV file saved")
    
    # Show sample of cleaned data
    print("\nSample of cleaned data (first 5 rows):")
    # Determine the season column name
    season_col = 'Season' if 'Season' in df_cleaned.columns else 'season_year'
    if season_col in df_cleaned.columns:
        display_cols = [season_col, 'Lig', 'Hafta', 'Tarih', 'Kod', 'EvSahibi', 'Deplasman']
    else:
        display_cols = ['Lig', 'Hafta', 'Tarih', 'Kod', 'EvSahibi', 'Deplasman']
    
    # Only show columns that exist
    display_cols = [col for col in display_cols if col in df_cleaned.columns]
    print(df_cleaned[display_cols].head())
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("Cleaning non-MS matches from data file")
    print("=" * 60)
    print()
    
    success = clean_non_ms_matches(INPUT_FILE, OUTPUT_FILE, CSV_OUTPUT_FILE)
    
    if success:
        print("\n" + "=" * 60)
        print("✓ Cleaning completed successfully!")
        print("=" * 60)
        print(f"\nOutput files:")
        print(f"  - Excel: {OUTPUT_FILE}")
        print(f"  - CSV: {CSV_OUTPUT_FILE}")
        print("\nTo replace the original file, run:")
        print(f"  mv {OUTPUT_FILE} {INPUT_FILE}")
        print(f"  mv {CSV_OUTPUT_FILE} {INPUT_FILE.with_suffix('.csv')}")
    else:
        print("\n" + "=" * 60)
        print("✗ Cleaning failed!")
        print("=" * 60)

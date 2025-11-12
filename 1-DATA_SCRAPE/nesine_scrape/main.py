from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
import time
import os
import re
from pathlib import Path

# ----------------------------- #
# AYARLAR
# ----------------------------- #

URL = "https://arsiv.mackolik.com/Standings/Default.aspx"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
UBLOCK_PATH = os.path.join(SCRIPT_DIR, "ublock_origin-1.67.0.xpi")
HEADLESS = True
WAIT_TIME = 10
AGGREGATE_FILENAME = "fikstur_tum_ligler_all_seasons.xlsx"
OUTPUT_PATH = Path(SCRIPT_DIR) / AGGREGATE_FILENAME
TEMP_OUTPUT_PATH = OUTPUT_PATH.with_name(f"{OUTPUT_PATH.stem}_temp{OUTPUT_PATH.suffix}")
CSV_OUTPUT_PATH = OUTPUT_PATH.with_suffix(".csv")
EXPECTED_COLUMNS = [
    "Season",
    "Lig",
    "Hafta",
    "Tarih",
    "Kod",
    "EvSahibi",
    "Deplasman",
    "Skor",
    "IY_Skor",
    "1",
    "0",
    "2",
    "1&0",
    "1&2",
    "2&0",
    "Alt",
    "Üst",
]

# ----------------------------- #
# SELENIUM AYARLARI
# ----------------------------- #

options = Options()
options.headless = HEADLESS
driver = webdriver.Firefox(options=options)
driver.install_addon(UBLOCK_PATH, temporary=True)
driver.get(URL)

wait = WebDriverWait(driver, WAIT_TIME)

# ----------------------------- #
# FİLTRE AYARLARI
# ----------------------------- #

LEAGUE_URLS = {
    "Türkiye Süper Lig": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67287",
    "İngiltere Premier League": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67180",
    "İspanya La Liga": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67194",
    "İtalya Serie A": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67286",
    "Almanya Bundesliga": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67285",
    "Fransa Ligue 1": "https://arsiv.mackolik.com/Standings/Default.aspx?sId=67238",
}


def normalize_season_label(raw_value):
    """Return season labels in canonical 'YYYY/YYYY' form."""
    if not raw_value:
        return ""

    label = str(raw_value).strip()

    def _format_years(start_str, end_str):
        start_year = int(start_str)
        if len(end_str) == 2:
            base_century = (start_year // 100) * 100
            end_year = base_century + int(end_str)
            if end_year <= start_year:
                end_year += 100
        else:
            end_year = int(end_str)
        return f"{start_year}/{end_year}"

    match = re.match(r"^(\d{4})[\-/](\d{2}|\d{4})$", label)
    if match:
        return _format_years(match.group(1), match.group(2))

    match = re.match(r"^(\d{4})\s+(\d{2}|\d{4})$", label)
    if match:
        return _format_years(match.group(1), match.group(2))

    return label.replace("-", "/")


def parse_week_number(week_name):
    """Extract numeric portion from a week label; fall back to -1 if absent."""
    if not week_name:
        return -1
    match = re.search(r"(\d+)", week_name)
    if match:
        try:
            return int(match.group(1))
        except ValueError:
            return -1
    return -1


def extract_year_from_week(week_name, date_str):
    """
    Extract the year from week_name (format: '1 (5.08.2022 - 7.08.2022)')
    and add it to date_str (format: '05/08').
    Handles cases where a week spans two different years.
    Returns date in format 'DD/MM/YYYY' or original date_str if parsing fails.
    """
    if not week_name or not date_str:
        return date_str
    
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
    
    # Extract the number before the parenthesis
    match = re.match(r'^(\d+)\s*\(', week_name)
    if match:
        return match.group(1)
    
    # Fallback: try to extract any number
    match = re.search(r'(\d+)', week_name)
    if match:
        return match.group(1)
    
    return week_name


def load_existing_dataset(path):
    """Load prior scrape results and standardize schema for incremental updates."""
    if not path.exists():
        return pd.DataFrame(columns=EXPECTED_COLUMNS)

    df = pd.read_excel(path)
    rename_map = {}
    if "season_year" in df.columns and "Season" not in df.columns:
        rename_map["season_year"] = "Season"
    if rename_map:
        df = df.rename(columns=rename_map)

    for column in EXPECTED_COLUMNS:
        if column not in df.columns:
            df[column] = None

    df = df[EXPECTED_COLUMNS]
    for column in ("Season", "Lig", "Hafta"):
        df[column] = df[column].fillna("").astype(str).str.strip()
    df["Season"] = df["Season"].apply(normalize_season_label)
    return df


def merge_existing_and_new(existing_df, new_df):
    """Merge new rows with historic data, replacing overlapping league/week slices."""
    if new_df.empty:
        return existing_df.copy()

    new_df = new_df.reindex(columns=EXPECTED_COLUMNS)
    new_df["Season"] = new_df["Season"].apply(normalize_season_label)

    if existing_df.empty:
        combined = new_df.copy()
    else:
        key_df = new_df[["Season", "Lig", "Hafta"]].drop_duplicates()
        filtered_existing = existing_df.merge(
            key_df,
            on=["Season", "Lig", "Hafta"],
            how="left",
            indicator=True,
        )
        filtered_existing = filtered_existing[filtered_existing["_merge"] == "left_only"].drop(columns="_merge")
        combined = pd.concat([filtered_existing, new_df], ignore_index=True)

    combined = combined.drop_duplicates(
        subset=["Season", "Lig", "Hafta", "Kod", "Tarih", "EvSahibi", "Deplasman", "Skor"],
        keep="last",
    )
    combined["Season"] = combined["Season"].apply(normalize_season_label)
    combined = combined.sort_values(["Season", "Lig", "Hafta", "Tarih"], ignore_index=True)
    return combined


def get_last_week(existing_df, league_name, season_name):
    """Return the most recent week label stored for the given league-season pair."""
    if existing_df.empty:
        return None

    mask = (existing_df["Lig"] == league_name) & (existing_df["Season"] == season_name)
    subset = existing_df.loc[mask]
    if subset.empty:
        return None

    subset = subset.copy()
    subset["_week_number"] = subset["Hafta"].apply(parse_week_number)
    subset = subset.sort_values(["_week_number", "Hafta"])
    return subset.iloc[-1]["Hafta"]

existing_data_df = load_existing_dataset(OUTPUT_PATH)

all_dfs = []
interrupted = False

def save_progress(verbose=True):
    """Geçici olarak toplanan verileri kaydet"""
    global existing_data_df
    if not all_dfs:
        return False

    temp_df = pd.concat(all_dfs, ignore_index=True)
    merged_df = merge_existing_and_new(existing_data_df, temp_df)
    existing_data_df = merged_df

    try:
        merged_df.to_excel(TEMP_OUTPUT_PATH, index=False, engine="openpyxl")
        if verbose:
            print(f"  → İlerleme kaydedildi: {str(TEMP_OUTPUT_PATH)} ({len(merged_df)} satır)")
        return True
    except ModuleNotFoundError:
        print("  → Uyarı: openpyxl bulunamadı, ilerleme kaydedilemedi. 'python -m pip install openpyxl' komutunu çalıştırın.")
    except Exception as err:
        print(f"  → Uyarı: ilerleme kaydedilirken hata oluştu: {err}")
    return False


def normalize_text(value):
    if not value:
        return ""
    cleaned = value.strip().replace("\xa0", " ")
    cleaned = cleaned.replace("–", "-").replace("—", "-").replace("−", "-")
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = re.sub(r"\s*-\s*", "-", cleaned)
    return cleaned


def is_played_score(value):
    cleaned = normalize_text(value).lower()
    if cleaned in {"", "-", "vs", "v", "ert", "tbd"}:
        return False
    if re.search(r"\d+\s*-\s*\d+", cleaned):
        return True
    return False

# ----------------------------- #
# TÜM LİGLERİ TEK TEK DOLAŞ
# ----------------------------- #
try:
    for idx, (league_name, url) in enumerate(LEAGUE_URLS.items(), start=1):
        print(f"\n[{idx}/{len(LEAGUE_URLS)}] {league_name} işleniyor...")

        league_has_data = False

        try:
            driver.get(url)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cboSeason")))
            time.sleep(1.5)

            season_select = driver.find_element(By.CSS_SELECTOR, "#cboSeason")
            season_elements = season_select.find_elements(By.TAG_NAME, "option")
            season_names = [opt.text.strip() for opt in season_elements if opt.text.strip()]

            if not season_names:
                print(f"{league_name}: sezon listesi bulunamadı, atlanıyor.")
                continue

            # Only process the last (most recent) season
            season_name = season_names[0]  # First option is usually the most recent season
            normalized_season = normalize_season_label(season_name)
            print(f"  → Sezon: {normalized_season} (en son sezon)")

            season_select = driver.find_element(By.CSS_SELECTOR, "#cboSeason")
            season_options = season_select.find_elements(By.TAG_NAME, "option")
            target_option = None
            for option in season_options:
                if option.text.strip() == season_name:
                    target_option = option
                    break

            if not target_option:
                print(f"    Sezon '{season_name}' bulunamadı, atlanıyor.")
                continue

            target_option.click()
            time.sleep(1.5)

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tab-list")))
            time.sleep(1)

            navbar = driver.find_element(By.CSS_SELECTOR, "#tab-list")
            fikstur_btn = navbar.find_element(By.CSS_SELECTOR, "li.ui-state-default:nth-child(3) a")
            fikstur_btn.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#cboWeek")))
            time.sleep(1)

            date_filter = driver.find_element(By.CSS_SELECTOR, "#cboWeek")
            week_elements = date_filter.find_elements(By.TAG_NAME, "option")
            indexed_weeks = [(i, opt.text.strip()) for i, opt in enumerate(week_elements) if opt.text.strip()]

            if not indexed_weeks:
                print("    → Haftalar bulunamadı, sezon atlanıyor.")
                continue

            last_week_name = get_last_week(existing_data_df, league_name, normalized_season)
            start_position = 0
            if last_week_name:
                last_week_number = parse_week_number(last_week_name)
                matched = False
                for pos, (_, week_name) in enumerate(indexed_weeks):
                    if week_name == last_week_name:
                        start_position = pos
                        matched = True
                        break
                if not matched and last_week_number > 0:
                    for pos, (_, week_name) in enumerate(indexed_weeks):
                        if parse_week_number(week_name) == last_week_number:
                            start_position = pos
                            matched = True
                            break
                if not matched and last_week_number > 0:
                    for pos, (_, week_name) in enumerate(indexed_weeks):
                        if parse_week_number(week_name) >= last_week_number:
                            start_position = max(0, pos - 1)
                            matched = True
                            break
                if not matched:
                    print(
                        f"    -> Kaydedilmiş hafta '{last_week_name}' seçeneklerde bulunamadı, sezon başından taranacak."
                    )

            season_has_data = False

            for relative_idx in range(start_position, len(indexed_weeks)):
                option_index, week_name = indexed_weeks[relative_idx]

                date_filter = driver.find_element(By.CSS_SELECTOR, "#cboWeek")
                week_options = date_filter.find_elements(By.TAG_NAME, "option")

                progress_total = max(1, len(indexed_weeks) - start_position)
                progress_current = relative_idx - start_position + 1
                print(f"    {week_name} ({progress_current}/{progress_total})")

                try:
                    week_options[option_index].click()
                except Exception:
                    date_filter = driver.find_element(By.CSS_SELECTOR, "#cboWeek")
                    week_options = date_filter.find_elements(By.TAG_NAME, "option")
                    week_options[option_index].click()

                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#dvFixtureInner > table:nth-child(1)")))
                time.sleep(1.2)

                table = driver.find_element(By.CSS_SELECTOR, "#dvFixtureInner > table:nth-child(1)")
                html = table.get_attribute("outerHTML")
                soup = BeautifulSoup(html, "html.parser")

                rows = []
                for tr in soup.find_all("tr"):
                    tds = [td.get_text(" ", strip=True) for td in tr.find_all("td")]
                    if not tds or "Fikstür" in "".join(tds):
                        continue
                    if len(tds) < 10:
                        continue

                    tarih = normalize_text(tds[0]) if len(tds) > 0 else ""
                    kod = normalize_text(tds[1]) if len(tds) > 1 else ""
                    if kod.upper() != "MS":
                        continue
                    ev_sahibi = normalize_text(tds[3]) if len(tds) > 3 else ""
                    skor = normalize_text(tds[5]) if len(tds) > 5 else ""
                    deplasman = normalize_text(tds[7]) if len(tds) > 7 else ""
                    iy_skor_raw = normalize_text(tds[8]) if len(tds) > 8 else ""

                    if not is_played_score(skor):
                        continue

                    iy_skor = iy_skor_raw if is_played_score(iy_skor_raw) else (iy_skor_raw if iy_skor_raw else None)

                    # Add year to the date using week_name information
                    tarih_with_year = extract_year_from_week(week_name, tarih)
                    
                    # Extract only the week number for storage
                    week_number_only = extract_week_number_only(week_name)

                    oran_index = 12 if len(tds) > 12 else 11
                    oranlar = [normalize_text(val) or None for val in tds[oran_index:]]
                    while len(oranlar) < 8:
                        oranlar.append(None)

                    row = [
                        normalized_season,
                        league_name,
                        week_number_only,
                        tarih_with_year or None,
                        kod or None,
                        ev_sahibi or None,
                        deplasman or None,
                        skor,
                        iy_skor,
                    ] + oranlar[:8]
                    rows.append(row)

                cols = [
                    "Season",
                    "Lig",
                    "Hafta",
                    "Tarih",
                    "Kod",
                    "EvSahibi",
                    "Deplasman",
                    "Skor",
                    "IY_Skor",
                    "1",
                    "0",
                    "2",
                    "1&0",
                    "1&2",
                    "2&0",
                    "Alt",
                    "Üst",
                ]

                if rows:
                    df = pd.DataFrame(rows, columns=cols)
                    all_dfs.append(df)
                    season_has_data = True
                    league_has_data = True
                    print(f"      → {len(rows)} oynanmış maç bulundu")
                else:
                    if relative_idx == start_position:
                        print("      → Haftada oynanmış maç bulunamadı, sonraki haftalar kontrol ediliyor.")
                        continue
                    print("      → Haftada oynanmış maç yok, kalan haftalar atlanıyor.")
                    break

            if season_has_data:
                print(f"  ✓ {season_name} sezonu işlendi.")
                save_progress()
            else:
                print(f"  → {season_name} sezonu için yeni veri bulunamadı.")

            if league_has_data:
                print(f"{league_name} tamamlandı.")
            else:
                print(f"{league_name} veri bulunamadı, atlandı.")

        except Exception as e:
            print(f"{league_name} hata verdi: {e}")
            continue
except KeyboardInterrupt:
    interrupted = True
    print("\n! İşlem kullanıcı tarafından durduruldu, mevcut veriler kaydediliyor...")
    save_progress()
except Exception as exc:
    interrupted = True
    print(f"\n! Beklenmeyen bir hata oluştu: {exc}")
    save_progress()
finally:
    try:
        driver.quit()
    except Exception:
        pass

# ----------------------------- #
# TÜM DF'LERİ BİRLEŞTİR VE KAYDET
# ----------------------------- #

new_data_df = pd.concat(all_dfs, ignore_index=True) if all_dfs else pd.DataFrame(columns=EXPECTED_COLUMNS)

if new_data_df.empty and existing_data_df.empty:
    print("\n✗ Hiç veri bulunamadı!")
    if interrupted:
        print("! İşlem kullanıcı tarafından durduruldu.")
else:
    if new_data_df.empty:
        final_df = existing_data_df.copy()
    else:
        final_df = merge_existing_and_new(existing_data_df, new_data_df)

    final_df = final_df.reindex(columns=EXPECTED_COLUMNS)
    final_df["Season"] = final_df["Season"].apply(normalize_season_label)
    final_df.to_excel(OUTPUT_PATH, index=False, engine="openpyxl")
    final_df.to_csv(CSV_OUTPUT_PATH, index=False)

    if not interrupted and TEMP_OUTPUT_PATH.exists():
        TEMP_OUTPUT_PATH.unlink()

    if new_data_df.empty:
        print(f"\nInfo: Yeni veri bulunamadı, mevcut kayıt güncellendi ({len(final_df)} satır).")
    else:
        print(f"\n✓ Tüm ligler tamamlandı ({len(final_df)} satır).")
    print(f"✓ Excel kaydı: {str(OUTPUT_PATH)}")
    print(f"✓ CSV kaydı: {str(CSV_OUTPUT_PATH)}")

    if interrupted:
        print(f"! İşlem tamamlanmadan durduruldu, ara kayıt {str(TEMP_OUTPUT_PATH)} dosyasında saklandı.")

if not HEADLESS and not interrupted:
    input("Enter'a basınca kapatılacak...")

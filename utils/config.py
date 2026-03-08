from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

RAW_DATA_DIR = PROJECT_ROOT / 'data' / 'raw'
CLEAN_DATA_DIR = PROJECT_ROOT / 'data' / 'clean'
VISUALIZATIONS_DIR = PROJECT_ROOT / 'visualizations'

RAW_DATASETS = {
    'apps_originating': 'asylum_applications_originating_tur.csv',
    'apps_residing': 'asylum_applications_residing_tur.csv',
    'decisions_residing': 'asylum_decisions_residing_tur.csv',
    'decisions_originating': 'asylum_decisions_originating_tur.csv'
}

CLEAN_DATASETS = {
    'apps_to_turkey': 'applications_to_turkey_clean.csv',
    'apps_from_turkey': 'applications_from_turkey_clean.csv',
    'decisions_turkey': 'decisions_from_turkey_clean.csv',
    'decisions_others': 'decisions_from_other_countries_clean.csv'
}
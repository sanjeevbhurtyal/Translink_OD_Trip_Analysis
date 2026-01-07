# TransLink Origin-Destination Patronage Analysis

## Overview

This repository provides a reproducible pipeline for downloading, processing, and analyzing TransLink OD patronage data.

**Analysis Blog Post:** [Translink Origin-Destination Patronage Analysis](https://sanjeevbhurtyal.github.io/TAI/translink-od/)

**Interactive Dashboard:** [Tableau Patronage Analysis](https://public.tableau.com/views/TranslinkPatronageAnlaysis/SuburbProfile?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Repository Structure
```
├── main.py
├── analysis/
│   └── figures/ # stores generated figures
├── config/
│   ├── __init__.py
│   ├── config_loader.py # loads configuration settings
│   ├── files_to_move.py # lists files to be moved
│   ├── mapping.py # contains mapping dictionaries
│   ├── schema.py # defines data schemas
├── notebooks/
│   ├── analysis.ipynb # main analysis notebook
└── src/
    ├── __init__.py 
    ├── combine_data.py # combines raw data files
    ├── download_data.py # downloads raw data
    ├── move_files.py # moves files to appropriate directories
    ├── process_data.py # processes raw data
```

## Data Source

1. Patronage data is sourced from the Queensland Government [Open Data Portal](https://www.data.qld.gov.au/dataset/translink-origin-destination-trips-2022-onwards).
2. Suburb boundaries shapefile is obtained from the [Queensland Spatial Catalogue](https://qldspatial.information.qld.gov.au/catalogue/custom/detail.page?fid={8F24D271-EE3B-491C-915C-E7DD617F95DC}).

**Important Notes:**
- Raw data files are **not included** in this repository due to size constraints (~several GB)
- Historical datasets (pre-April 2025) currently exclude EMV transactions; Queensland Government plans to update these retroactively

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup

1. Clone the repository:
```bash
git clone https://github.com/sanjeevbhurtyal/Translink_OD_Trip_Analysis.git
cd Translink_OD_Trip_Analysis
```
2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage
1. Download Suburb Boundaries Shapefile from [Queensland Spatial Catalogue](https://qldspatial.information.qld.gov.au/catalogue/custom/detail.page?fid={8F24D271-EE3B-491C-915C-E7DD617F95DC}) and place it in the `data/suburbs/` directory.
2. Update configuration settings in `config/config.yaml` as needed.
3. Run the main analysis script:
    ```bash
    python main.py
    ```
    This will download and process the OD data and store the processed data in the `data/processed/` directory.
4. Open and run the analysis notebook:
    ```bash 
    jupyter notebook notebooks/analysis.ipynb
    ```

## Future Work
- Travel time analysis using GTFS data
- Trip purpose imputation using survey data
- Socioeconomic equity analysis (overlay with census data)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Sanjeev Bhurtyal**

- GitHub: [@sanjeevbhurtyal](https://github.com/sanjeevbhurtyal)
- LinkedIn: [Sanjeev Bhurtyal](https://www.linkedin.com/in/sanjeev-bhurtyal/)

*Last Updated: January 2026*
from pathlib import Path
import pandas as pd
import geopandas as gpd
from config.mapping import TIME_PERIOD_MAP, OPERATOR_MODE_MAP   
import logging

def process_data(COMBINED_DATA_DIR: Path,
                 COMBINED_OUTPUT_FILE: Path, 
                 SUBURBS_PATH: Path, 
                 OUTPUT_DIR: Path, 
                 OUTPUT_FILE: Path) -> None:
    
    # CRS
    CRS_WGS84 = "EPSG:4326"

    # Paths
    STOP_MAPPING_PATH = COMBINED_DATA_DIR / "stop_id_mapping.csv"

    # ---------------------------------------------------------------------
    # Load data
    # ---------------------------------------------------------------------
    logging.info("Loading OD data...")
    trips_df = pd.read_csv(COMBINED_OUTPUT_FILE, low_memory=False)

    logging.info("Loading Stop ID Mapping...")
    stops_df = pd.read_csv(STOP_MAPPING_PATH)

    logging.info("Loading suburb shapefile...")
    stops_gdf = gpd.GeoDataFrame(
        stops_df,
        geometry=gpd.points_from_xy(stops_df.stop_lon, stops_df.stop_lat),
        crs=CRS_WGS84,
    )

    stops_gdf["stop_id"] = stops_gdf["stop_id"].astype(str)

    suburbs_gdf = gpd.read_file(SUBURBS_PATH).to_crs(CRS_WGS84)

    # ---------------------------------------------------------------------
    # Spatial join: assign locality to each stop
    # ---------------------------------------------------------------------
    logging.info("Spatial join: assign locality to each stop...")
    stops_gdf = gpd.sjoin(
        stops_gdf,
        suburbs_gdf,
        how="left",
        predicate="within",
    )

    # ---------------------------------------------------------------------
    # Spatial Attributes
    # ---------------------------------------------------------------------
    trips_df = (
        trips_df
        .merge(
            stops_gdf[["stop_id", "loc_code"]],
            left_on="origin_stop",
            right_on="stop_id",
            how="left",
        )
        .rename(columns={"loc_code": "origin_loc_code"})
        .drop(columns="stop_id")
        .merge(
            stops_gdf[["stop_id", "loc_code"]],
            left_on="destination_stop",
            right_on="stop_id",
            how="left",
        )
        .rename(columns={"loc_code": "destination_loc_code"})
        .drop(columns="stop_id")
    )

    # Fill missing values with "Unknown"
    trips_df["origin_loc_code"] = trips_df["origin_loc_code"].fillna("Unknown")
    trips_df["destination_loc_code"] = trips_df["destination_loc_code"].fillna("Unknown")

    # ---------------------------------------------------------------------
    # Temporal attributes
    # ---------------------------------------------------------------------
    trips_df["time_period"] = trips_df["time"].map(TIME_PERIOD_MAP)

    # ---------------------------------------------------------------------
    # Add mode
    # ---------------------------------------------------------------------
    trips_df["mode"] = trips_df["operator"].map(OPERATOR_MODE_MAP)

    # Drop unused fields
    trips_df = trips_df.drop(
        columns=["origin_stop", "destination_stop", "time"]
    )

    # ---------------------------------------------------------------------
    # Aggregate OD flows
    # ---------------------------------------------------------------------
    logging.info("Aggregating OD flows...")
    od_df = (
        trips_df
        .groupby(
            [
                "operator",
                "month",
                "route",
                "mode",
                "time_period",
                "ticket_type",
                "origin_loc_code",
                "destination_loc_code",
            ],
            as_index=False,
        )
        .agg(quantity=("quantity", "sum"))
    )

    # ---------------------------------------------------------------------
    # Export
    # ---------------------------------------------------------------------
    logging.info("Exporting data...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    od_df.to_csv(OUTPUT_FILE, index=False)

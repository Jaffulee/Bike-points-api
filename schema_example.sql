-- Set the working database and schema
USE DATABASE til_data_engineering;
USE SCHEMA JM_DES2_STAGING;

-- Copy raw bike point data to personal staging area
CREATE OR REPLACE TABLE jt_deng3_staging.bike_point_raw AS
SELECT * 
FROM JM_DES2_STAGING.bike_point_raw;

-- Switch to personal staging schema
USE SCHEMA jt_deng3_staging;

-- Preview the copied raw data
SELECT * 
FROM jt_deng3_staging.bike_point_raw;

-- Confirm database and schema context
USE DATABASE til_data_engineering;
USE SCHEMA jt_deng3_staging;

-- Unnest top-level fields from raw JSON
CREATE OR REPLACE TABLE bike_point_unnest_l1 AS
    SELECT
        json:id::string as id,
        json:commonName::string as street_borough,
        json:lat::float as latitude,
        json:lon::float as longitude,
        json:placeType::string as placeType,
        json:url::string as url,
        json:additionalProperties::variant as additional_properties_json
    FROM bike_point_raw
    ORDER BY id
    -- limit 10;

-- Preview unnested level 1
SELECT * FROM bike_point_unnest_l1;

-- Flatten nested array of additionalProperties from level 1
CREATE OR REPLACE TABLE bike_point_unnest_l2 AS
    SELECT
        id,
        value:key::varchar as key,
        value:value::varchar as value,
        value:modified::datetime as modified
    FROM bike_point_unnest_l1,
    LATERAL flatten(additional_properties_json) -- one row per key-value-modified in the nested array
    ORDER BY id
    -- LIMIT 20;

-- Preview unnested level 2
SELECT * FROM bike_point_unnest_l2
ORDER BY ID, MODIFIED;

-- Create historic details table by pivoting key-value pairs
CREATE OR REPLACE TABLE bike_details_historic AS
WITH deduped AS (
    SELECT
        id,
        TO_VARCHAR(modified) AS modified,
        id || '_' || TO_VARCHAR(modified) AS id_mod, -- Unique ID for pivoting
        key,
        value
    FROM bike_point_unnest_l2
),
pivoted AS (
    SELECT
        id,
        modified,
        TerminalName,
        Installed,
        Locked,
        InstallDate,
        RemovalDate,
        Temporary,
        NULLIF(NbBikes, '') AS number_bikes,
        NULLIF(NbEmptyDocks, '') AS number_empty_docks,
        NULLIF(NbDocks, '') AS number_docks,
        NULLIF(NbStandardBikes, '') AS number_standard_bikes,
        NULLIF(NbEBikes, '') AS number_e_bikes
    FROM (
        SELECT id_mod, key, value, id, modified
        FROM deduped
    )
    PIVOT (
        MAX(value) FOR key IN (
            'TerminalName',
            'Installed',
            'Locked',
            'InstallDate',
            'RemovalDate',
            'Temporary',
            'NbBikes',
            'NbEmptyDocks',
            'NbDocks',
            'NbStandardBikes',
            'NbEBikes'
        )
    ) AS p (
        id_mod,
        id,
        modified,
        TerminalName,
        Installed,
        Locked,
        InstallDate,
        RemovalDate,
        Temporary,
        NbBikes,
        NbEmptyDocks,
        NbDocks,
        NbStandardBikes,
        NbEBikes
    )
)
SELECT * FROM pivoted;

-- Preview the full historic record
SELECT * FROM bike_details_historic
ORDER BY ID;

-- Create fact table with bike location metadata (deduplicated)
CREATE OR REPLACE TABLE bike_point_fact AS
    (
    SELECT ID, STREET_BOROUGH, LATITUDE, LONGITUDE, PLACETYPE, URL
    FROM bike_point_unnest_l1
    GROUP BY ALL
    ORDER BY ID
    );

-- Preview fact table
SELECT * FROM bike_point_fact;

-- Create latest snapshot of bike details using most recent modified timestamp
CREATE OR REPLACE TABLE bike_details AS
    WITH latest_date_bike AS (
        SELECT
            id AS latest_id,
            MAX(modified) AS latest_modified
        FROM bike_details_historic
        GROUP BY id
    )
    SELECT
        id,
        modified,
        TerminalName,
        Installed,
        Locked,
        InstallDate,
        RemovalDate,
        Temporary,
        number_bikes,
        number_empty_docks,
        number_docks,
        number_standard_bikes,
        number_e_bikes
    FROM bike_details_historic
    INNER JOIN latest_date_bike 
        ON modified = latest_modified AND id = latest_id;

-- Preview all output tables
SELECT * FROM bike_point_fact ORDER BY ID;    
SELECT * FROM bike_details ORDER BY ID, MODIFIED;
SELECT * FROM bike_details_historic ORDER BY ID, MODIFIED;

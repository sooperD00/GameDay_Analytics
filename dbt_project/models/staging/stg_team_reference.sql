-- Staging: Team Reference Data (curated mapping table)
-- Grain: One row per team per active period
-- Purpose: Standardize team identity, handle relocations/rebrands, 
--          provide conference/division enrichment for cross-source joins
-- Source: dbt seed (team_reference_seed.csv), maintained by non-technical staff

WITH source AS (
    SELECT * FROM {{ ref('team_reference_seed') }}
),

renamed AS (
    SELECT
        -- Keys
        espn_team_id,
        
        -- Team identity
        team_city AS team_location,
        team_name,
        team_city || ' ' || team_name AS full_name,
        
        -- Organization
        conference,
        division,
        
        -- Temporal validity (for relocation tracking)
        active_years,
        SUBSTR(active_years, 1, 4) AS active_from,
        SUBSTR(active_years, -4) AS active_to

    FROM source
)

SELECT * FROM renamed

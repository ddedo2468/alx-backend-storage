-- old school bands

SELECT band_name, COALESCE(split, 2022) - 2022 AS lifespan FROM metal_bands
WHERE style LIKE '%Glam rock%'
ORDER BY lifespan DESC;

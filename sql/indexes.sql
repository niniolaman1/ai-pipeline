-- Speeds up "latest reading for a route at a stop" (bus API).
-- Built 16 Nov 2026: query time went from 18 s to 38 ms. Size about 1 GB.
CREATE INDEX CONCURRENTLY trip_updates_stop_route_time_idx
ON trip_updates (stop_id, route_id, recorded_at);
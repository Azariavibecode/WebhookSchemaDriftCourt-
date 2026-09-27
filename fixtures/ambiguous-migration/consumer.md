# Account consumer migration
The consumer currently requires `/data/owner_id`. Migrate to `/data/owner/id`; deploy dual-read support before the provider removes the old field.

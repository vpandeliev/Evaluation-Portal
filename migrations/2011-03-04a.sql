BEGIN;
ALTER TABLE "studies_data" ADD COLUMN "stage_stub" varchar(3) NOT NULL DEFAULT '';
COMMIT;
BEGIN;
ALTER TABLE "studies_stage" ADD COLUMN "stub" varchar(3) NOT NULL DEFAULT '';
COMMIT;
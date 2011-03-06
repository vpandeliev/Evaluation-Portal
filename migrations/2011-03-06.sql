BEGIN;
ALTER TABLE "studies_study" ADD COLUMN "assess_blocks" int NOT NULL DEFAULT 8;
ALTER TABLE "studies_study" ADD COLUMN "assess_trials" int NOT NULL DEFAULT 30;
COMMIT;

BEGIN;
ALTER TABLE "studies_study" ADD COLUMN "boggle_duration" int NOT NULL DEFAULT 180;
ALTER TABLE "studies_study" ADD COLUMN "boggle_rounds" int NOT NULL DEFAULT 10;
ALTER TABLE "studies_study" ADD COLUMN "task_session_dur" int NOT NULL DEFAULT 45;
COMMIT;

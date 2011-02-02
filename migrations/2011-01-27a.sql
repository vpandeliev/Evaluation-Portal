BEGIN;
ALTER TABLE "boggle_game" ADD COLUMN "round_duration" int NOT NULL DEFAULT 180;
COMMIT;

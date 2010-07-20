BEGIN;
ALTER TABLE "boggle_round" ADD COLUMN "mode" integer unsigned NOT NULL DEFAULT 0;
COMMIT;
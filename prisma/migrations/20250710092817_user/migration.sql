/*
  Warnings:

  - The primary key for the `User` table will be changed. If it partially fails, the table could be left without primary key constraint.

*/
-- AlterTable
ALTER TABLE "User" DROP CONSTRAINT "User_pkey",
ALTER COLUMN "id" DROP DEFAULT,
ALTER COLUMN "id" SET DATA TYPE TEXT,
ADD CONSTRAINT "User_pkey" PRIMARY KEY ("id");
DROP SEQUENCE "User_id_seq";

-- CreateTable
CREATE TABLE "quiz_result" (
    "id" TEXT NOT NULL,
    "userId" TEXT NOT NULL,
    "correct_answer" INTEGER NOT NULL,
    "Wrong_Answer" INTEGER NOT NULL,
    "Total_question" INTEGER NOT NULL,
    "level" TEXT NOT NULL,
    "Total_Marks" INTEGER NOT NULL,
    "score" INTEGER NOT NULL,
    "percentage" INTEGER NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "quiz_result_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "quiz_result" ADD CONSTRAINT "quiz_result_userId_fkey" FOREIGN KEY ("userId") REFERENCES "User"("clerk_id") ON DELETE RESTRICT ON UPDATE CASCADE;

/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

export interface Option {
  id: string;
  formula: string;
  name: string;
  emoji?: string;
}

export interface Step {
  id: string;
  formula: string[]; // e.g. ["HCl", "+", "NaOH", "→", "?", "+", "H2O"]
  blankIndex: number;
  answer: string;
  options: Option[];
  condition?: string;
  explanation?: string;
}

export interface Level {
  id: number;
  name: string;
  difficulty: "Easy" | "Medium" | "Hard";
  maxMoves: number;
  steps: Step[];
  themeColor: string;
  emoji: string;
}

export interface UserProgress {
  unlockedLevels: number[];
  levelStars: Record<number, number>; // levelId -> stars (1-3)
  highScores: Record<number, number>;
  lives: number;
  lastLifeRefill: number;
  powerups: {
    hints: number;
    skips: number;
    zaps: number;
  };
}

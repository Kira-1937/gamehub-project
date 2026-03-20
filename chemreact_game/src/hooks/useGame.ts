/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useEffect, useCallback } from "react";
import { Level, UserProgress } from "../types";
import { LEVELS } from "../data/levels";

const INITIAL_PROGRESS: UserProgress = {
  unlockedLevels: [1],
  levelStars: {},
  highScores: {},
  lives: 5,
  lastLifeRefill: Date.now(),
  powerups: {
    hints: 3,
    skips: 1,
    zaps: 3,
  },
};

export function useGame() {
  const [progress, setProgress] = useState<UserProgress>(() => {
    const saved = localStorage.getItem("chemreact_progress");
    return saved ? JSON.parse(saved) : INITIAL_PROGRESS;
  });

  const [gameState, setGameState] = useState<{
    currentLevel: Level | null;
    currentStepIndex: number;
    score: number;
    moves: number;
    combo: number;
    maxCombo: number;
    status: "idle" | "playing" | "won" | "lost";
    eliminatedOptions: string[]; // IDs of options removed by Zap
  }>({
    currentLevel: null,
    currentStepIndex: 0,
    score: 0,
    moves: 0,
    combo: 0,
    maxCombo: 0,
    status: "idle",
    eliminatedOptions: [],
  });

  // Save progress whenever it changes
  useEffect(() => {
    localStorage.setItem("chemreact_progress", JSON.stringify(progress));
  }, [progress]);

  // Life regeneration logic (1 life every 30 mins)
  useEffect(() => {
    const interval = setInterval(() => {
      if (progress.lives < 5) {
        const now = Date.now();
        const diff = now - progress.lastLifeRefill;
        const refillTime = 30 * 60 * 1000; // 30 mins

        if (diff >= refillTime) {
          const livesToAdd = Math.floor(diff / refillTime);
          setProgress((prev) => ({
            ...prev,
            lives: Math.min(5, prev.lives + livesToAdd),
            lastLifeRefill: now - (diff % refillTime),
          }));
        }
      }
    }, 60000); // Check every minute

    return () => clearInterval(interval);
  }, [progress.lives, progress.lastLifeRefill]);

  const startLevel = useCallback((levelId: number) => {
    const level = LEVELS.find((l) => l.id === levelId);
    if (!level) return;

    if (progress.lives <= 0) {
      alert("No lives left! Wait for refill.");
      return;
    }

    setGameState({
      currentLevel: level,
      currentStepIndex: 0,
      score: 0,
      moves: level.maxMoves,
      combo: 0,
      maxCombo: 0,
      status: "playing",
      eliminatedOptions: [],
    });
  }, [progress.lives]);

  const makeChoice = useCallback((optionId: string) => {
    if (gameState.status !== "playing" || !gameState.currentLevel) return;

    const currentStep = gameState.currentLevel.steps[gameState.currentStepIndex];
    if (!currentStep) return;

    const selectedOption = currentStep.options.find((o) => o.id === optionId);

    if (!selectedOption) return;

    const isCorrect = selectedOption.formula === currentStep.answer;

    if (isCorrect) {
      const newCombo = gameState.combo + 1;
      const stepScore = 100 * newCombo;
      const isLastStep = gameState.currentStepIndex === gameState.currentLevel.steps.length - 1;

      setGameState((prev) => ({
        ...prev,
        score: prev.score + stepScore,
        combo: newCombo,
        maxCombo: Math.max(prev.maxCombo, newCombo),
        currentStepIndex: prev.currentStepIndex + 1,
        eliminatedOptions: [],
        status: isLastStep ? "won" : "playing",
      }));

      if (isLastStep) {
        handleWin(gameState.currentLevel.id, gameState.score + stepScore, gameState.moves);
      }
    } else {
      setGameState((prev) => {
        const newMoves = prev.moves - 1;
        const newStatus = newMoves <= 0 ? "lost" : "playing";
        
        if (newStatus === "lost") {
          handleLoss();
        }

        return {
          ...prev,
          moves: newMoves,
          combo: 0,
          status: newStatus,
        };
      });
    }
  }, [gameState]);

  const handleWin = (levelId: number, score: number, movesLeft: number) => {
    const stars = movesLeft > 5 ? 3 : movesLeft > 2 ? 2 : 1;
    
    setProgress((prev) => {
      const nextLevelId = levelId + 1;
      const newUnlocked = prev.unlockedLevels.includes(nextLevelId) 
        ? prev.unlockedLevels 
        : [...prev.unlockedLevels, nextLevelId];
      
      return {
        ...prev,
        unlockedLevels: newUnlocked,
        levelStars: {
          ...prev.levelStars,
          [levelId]: Math.max(prev.levelStars[levelId] || 0, stars),
        },
        highScores: {
          ...prev.highScores,
          [levelId]: Math.max(prev.highScores[levelId] || 0, score),
        },
      };
    });
  };

  const handleLoss = () => {
    setProgress((prev) => ({
      ...prev,
      lives: Math.max(0, prev.lives - 1),
      lastLifeRefill: prev.lives === 5 ? Date.now() : prev.lastLifeRefill,
    }));
  };

  const usePowerup = (type: "hint" | "skip" | "zap") => {
    if (gameState.status !== "playing" || !gameState.currentLevel) return;

    setProgress((prev) => {
      const key = type === "hint" ? "hints" : type === "skip" ? "skips" : "zaps";
      if (prev.powerups[key] <= 0) return prev;

      return {
        ...prev,
        powerups: {
          ...prev.powerups,
          [key]: prev.powerups[key] - 1,
        },
      };
    });

    if (type === "skip") {
      const isLastStep = gameState.currentStepIndex === gameState.currentLevel.steps.length - 1;
      setGameState((prev) => ({
        ...prev,
        currentStepIndex: prev.currentStepIndex + 1,
        status: isLastStep ? "won" : "playing",
      }));
      if (isLastStep) handleWin(gameState.currentLevel.id, gameState.score, gameState.moves);
    } else if (type === "zap") {
      const currentStep = gameState.currentLevel.steps[gameState.currentStepIndex];
      const wrongOptions = currentStep.options.filter(o => o.formula !== currentStep.answer && !gameState.eliminatedOptions.includes(o.id));
      if (wrongOptions.length > 0) {
        const toEliminate = wrongOptions[Math.floor(Math.random() * wrongOptions.length)];
        setGameState(prev => ({
          ...prev,
          eliminatedOptions: [...prev.eliminatedOptions, toEliminate.id]
        }));
      }
    }
  };

  return {
    progress,
    gameState,
    startLevel,
    makeChoice,
    usePowerup,
    resetGame: () => setGameState({ ...gameState, status: "idle", currentLevel: null }),
  };
}

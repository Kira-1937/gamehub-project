/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { useGame } from "./hooks/useGame";
import { SplashScreen } from "./components/SplashScreen";
import { LevelMap } from "./components/LevelMap";
import { GameView } from "./components/GameView";
import { ResultModal } from "./components/ResultModal";
import { HUD } from "./components/HUD";

export default function App() {
  const { progress, gameState, startLevel, makeChoice, usePowerup, resetGame } = useGame();
  const [view, setView] = useState<"splash" | "map" | "game">("splash");

  const handleStart = () => setView("map");
  const handleSelectLevel = (id: number) => {
    startLevel(id);
    setView("game");
  };

  const totalStars = Object.values(progress.levelStars).reduce((a: number, b: number) => a + b, 0);

  return (
    <div className="min-h-screen bg-gray-900 font-sans selection:bg-indigo-500 selection:text-white">
      <AnimatePresence mode="wait">
        {view === "splash" && (
          <motion.div
            key="splash"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <SplashScreen onStart={handleStart} />
          </motion.div>
        )}

        {view === "map" && (
          <motion.div
            key="map"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <HUD 
              lives={progress.lives} 
              stars={totalStars} 
              score={Object.values(progress.highScores).reduce((a: number, b: number) => a + b, 0)} 
            />
            <LevelMap 
              unlockedLevels={progress.unlockedLevels} 
              levelStars={progress.levelStars} 
              onSelectLevel={handleSelectLevel} 
            />
          </motion.div>
        )}

        {view === "game" && gameState.currentLevel && (
          <motion.div
            key="game"
            initial={{ opacity: 0, x: 100 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -100 }}
          >
            <HUD 
              lives={progress.lives} 
              stars={totalStars} 
              score={gameState.score} 
              moves={gameState.moves}
              powerups={progress.powerups}
              onPowerup={usePowerup}
            />
            <GameView 
              level={gameState.currentLevel}
              currentStepIndex={gameState.currentStepIndex}
              score={gameState.score}
              moves={gameState.moves}
              combo={gameState.combo}
              eliminatedOptions={gameState.eliminatedOptions}
              onChoice={makeChoice}
            />
          </motion.div>
        )}
      </AnimatePresence>

      {/* Result Modals */}
      <AnimatePresence>
        {(gameState.status === "won" || gameState.status === "lost") && (
          <ResultModal 
            status={gameState.status}
            score={gameState.score}
            moves={gameState.moves}
            maxCombo={gameState.maxCombo}
            onRetry={() => startLevel(gameState.currentLevel!.id)}
            onMap={() => {
              resetGame();
              setView("map");
            }}
            onNext={gameState.status === 'won' ? () => startLevel(gameState.currentLevel!.id + 1) : undefined}
          />
        )}
      </AnimatePresence>
    </div>
  );
}

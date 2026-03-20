/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "motion/react";
import { ArrowRight, Check, X, Info } from "lucide-react";
import { Level, Step, Option } from "../types";

interface GameViewProps {
  level: Level;
  currentStepIndex: number;
  score: number;
  moves: number;
  combo: number;
  eliminatedOptions: string[];
  onChoice: (optionId: string) => void;
}

export const GameView: React.FC<GameViewProps> = ({ 
  level, 
  currentStepIndex, 
  score, 
  moves, 
  combo, 
  eliminatedOptions,
  onChoice 
}) => {
  const [feedback, setFeedback] = useState<"correct" | "wrong" | null>(null);
  const currentStep = level.steps[currentStepIndex];

  if (!currentStep) return null;

  const handleChoice = (optionId: string) => {
    const isCorrect = currentStep.options.find(o => o.id === optionId)?.formula === currentStep.answer;
    
    if (isCorrect) {
      setFeedback("correct");
      setTimeout(() => {
        setFeedback(null);
        onChoice(optionId);
      }, 800);
    } else {
      setFeedback("wrong");
      onChoice(optionId);
      setTimeout(() => setFeedback(null), 800);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 pt-24 pb-32 px-4 flex flex-col items-center gap-6 overflow-hidden">
      {/* Level Info */}
      <div className="text-center">
        <motion.h2 
          initial={{ y: -20, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          className="text-white font-black text-3xl drop-shadow-lg uppercase tracking-tight"
        >
          {level.name}
        </motion.h2>
        <p className="text-white/70 font-bold text-sm uppercase tracking-widest">{level.difficulty} • Step {currentStepIndex + 1}/{level.steps.length}</p>
      </div>

      {/* Reaction Chain Card */}
      <motion.div 
        layout
        className="w-full max-w-md bg-white/10 backdrop-blur-md rounded-3xl p-6 border border-white/20 shadow-2xl relative overflow-hidden"
      >
        <div className="flex flex-col gap-4">
          {level.steps.map((step, idx) => {
            const isCompleted = idx < currentStepIndex;
            const isActive = idx === currentStepIndex;

            return (
              <motion.div 
                key={step.id}
                initial={{ x: -20, opacity: 0 }}
                animate={{ x: 0, opacity: isActive || isCompleted ? 1 : 0.3 }}
                className={`flex items-center gap-3 p-3 rounded-2xl transition-colors ${isActive ? 'bg-white/20 border border-white/30 shadow-inner' : ''}`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm ${isCompleted ? 'bg-green-400 text-white' : isActive ? 'bg-yellow-400 text-white animate-pulse' : 'bg-white/10 text-white/50'}`}>
                  {isCompleted ? <Check className="w-4 h-4" /> : idx + 1}
                </div>
                
                <div className="flex flex-wrap items-center gap-1 font-mono text-lg font-bold text-white">
                  {step.formula.map((token, tIdx) => (
                    <span key={tIdx} className={tIdx === step.blankIndex && isActive ? "bg-white/20 px-4 py-1 rounded-md border-2 border-dashed border-white/50 min-w-[3rem] text-center text-yellow-300" : ""}>
                      {tIdx === step.blankIndex && isActive ? "?" : isCompleted && tIdx === step.blankIndex ? step.answer : token}
                    </span>
                  ))}
                </div>

                {step.condition && (
                  <div className="ml-auto bg-white/10 px-2 py-0.5 rounded-full text-[10px] font-bold text-white/50 uppercase tracking-tighter">
                    {step.condition}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>

        {/* Combo Indicator */}
        <AnimatePresence>
          {combo > 1 && (
            <motion.div 
              initial={{ scale: 0, rotate: -20 }}
              animate={{ scale: 1, rotate: 0 }}
              exit={{ scale: 0, opacity: 0 }}
              className="absolute top-2 right-2 bg-yellow-400 text-white font-black px-3 py-1 rounded-full shadow-lg border-2 border-white flex items-center gap-1"
            >
              <span className="text-xs uppercase">Combo</span>
              <span>x{combo}</span>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* Options Grid */}
      <div className="w-full max-w-md grid grid-cols-2 gap-4 mt-auto">
        {currentStep.options.map((option) => {
          const isEliminated = eliminatedOptions.includes(option.id);
          
          return (
            <motion.button
              key={option.id}
              whileHover={!isEliminated ? { scale: 1.05, y: -5 } : {}}
              whileTap={!isEliminated ? { scale: 0.95 } : {}}
              onClick={() => !isEliminated && handleChoice(option.id)}
              disabled={isEliminated}
              className={`
                relative h-24 rounded-2xl p-4 flex flex-col items-center justify-center gap-1 shadow-xl border-b-4 transition-all
                ${isEliminated 
                  ? 'bg-gray-800/50 border-gray-900/50 opacity-30 cursor-not-allowed' 
                  : 'bg-white border-gray-200 hover:border-indigo-400'}
              `}
            >
              <span className="font-mono text-xl font-black text-indigo-900">{option.formula}</span>
              <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-widest text-center leading-tight">{option.name}</span>
              
              {/* Feedback Overlays */}
              <AnimatePresence>
                {feedback === "correct" && option.formula === currentStep.answer && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="absolute inset-0 bg-green-500 rounded-2xl flex items-center justify-center text-white"
                  >
                    <Check className="w-10 h-10" />
                  </motion.div>
                )}
                {feedback === "wrong" && option.formula !== currentStep.answer && (
                  <motion.div 
                    initial={{ opacity: 0, scale: 0.5 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className="absolute inset-0 bg-red-500 rounded-2xl flex items-center justify-center text-white"
                  >
                    <X className="w-10 h-10" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.button>
          );
        })}
      </div>

      {/* Explanation Hint (if correct) */}
      <AnimatePresence>
        {feedback === "correct" && (
          <motion.div 
            initial={{ y: 50, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: 50, opacity: 0 }}
            className="fixed bottom-32 left-4 right-4 max-w-md mx-auto bg-green-500 text-white p-4 rounded-2xl shadow-2xl border-2 border-white/30 flex gap-3 items-start"
          >
            <Info className="w-6 h-6 shrink-0" />
            <div>
              <p className="font-black text-sm uppercase tracking-widest mb-1">Reaction Complete!</p>
              <p className="text-xs font-bold leading-relaxed opacity-90">{currentStep.explanation}</p>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

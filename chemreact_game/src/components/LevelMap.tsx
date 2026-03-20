/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from "react";
import { motion } from "motion/react";
import { Lock, Star } from "lucide-react";
import { Level } from "../types";
import { LEVELS } from "../data/levels";

interface LevelMapProps {
  unlockedLevels: number[];
  levelStars: Record<number, number>;
  onSelectLevel: (id: number) => void;
}

export const LevelMap: React.FC<LevelMapProps> = ({ unlockedLevels, levelStars, onSelectLevel }) => {
  // Winding path logic: alternate x positions
  const getX = (index: number) => {
    const row = Math.floor(index / 3);
    const col = index % 3;
    const isEvenRow = row % 2 === 0;
    return isEvenRow ? col * 33 + 16 : (2 - col) * 33 + 16;
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-sky-400 via-emerald-400 to-green-500 p-8 pt-24 pb-32 overflow-y-auto relative">
      {/* Background decorations */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
        {[...Array(20)].map((_, i) => (
          <div 
            key={i}
            className="absolute text-4xl"
            style={{
              top: `${Math.random() * 100}%`,
              left: `${Math.random() * 100}%`,
              transform: `rotate(${Math.random() * 360}deg)`
            }}
          >
            {["🧪", "🔥", "⚡", "🏭", "🌿", "🔴", "🌍", "🍓", "🧼", "💥"][i % 10]}
          </div>
        ))}
      </div>

      <div className="max-w-md mx-auto relative z-10">
        <div className="flex flex-col-reverse gap-12 items-center">
          {LEVELS.map((level, index) => {
            const isUnlocked = unlockedLevels.includes(level.id);
            const stars = levelStars[level.id] || 0;
            const x = getX(index);

            return (
              <motion.div
                key={level.id}
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                transition={{ delay: index * 0.05 }}
                style={{ marginLeft: `${x}%` }}
                className="relative"
              >
                <motion.button
                  whileHover={isUnlocked ? { scale: 1.1 } : {}}
                  whileTap={isUnlocked ? { scale: 0.9 } : {}}
                  onClick={() => isUnlocked && onSelectLevel(level.id)}
                  className={`
                    w-16 h-16 rounded-full flex items-center justify-center text-white font-bold text-2xl shadow-xl border-4
                    ${isUnlocked 
                      ? `${level.themeColor} border-white/50 cursor-pointer` 
                      : 'bg-gray-400 border-gray-300 cursor-not-allowed grayscale'}
                    relative overflow-hidden group
                  `}
                >
                  {isUnlocked ? (
                    <>
                      <span className="relative z-10">{level.id}</span>
                      <div className="absolute inset-0 bg-white/20 group-hover:bg-white/30 transition-colors" />
                    </>
                  ) : (
                    <Lock className="w-6 h-6 text-white/50" />
                  )}
                </motion.button>

                {/* Stars */}
                {isUnlocked && (
                  <div className="absolute -bottom-4 left-1/2 -translate-x-1/2 flex gap-0.5">
                    {[...Array(3)].map((_, i) => (
                      <Star 
                        key={i} 
                        className={`w-4 h-4 ${i < stars ? 'text-yellow-400 fill-yellow-400' : 'text-gray-300 fill-gray-300'}`} 
                      />
                    ))}
                  </div>
                )}

                {/* Level Name Tooltip (on hover) */}
                {isUnlocked && (
                  <div className="absolute -top-8 left-1/2 -translate-x-1/2 whitespace-nowrap bg-white/90 backdrop-blur-sm px-2 py-0.5 rounded-md text-[10px] font-bold text-gray-700 shadow-sm opacity-0 group-hover:opacity-100 transition-opacity">
                    {level.name}
                  </div>
                )}
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Chapter Marker */}
      <div className="mt-12 text-center">
        <div className="inline-block bg-white/20 backdrop-blur-md px-6 py-2 rounded-full border border-white/30 text-white font-bold uppercase tracking-widest text-sm">
          Chapter 1: The Basics
        </div>
      </div>
    </div>
  );
};

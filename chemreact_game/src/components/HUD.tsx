/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from "react";
import { Heart, Star, Trophy, Zap, Lightbulb, FastForward } from "lucide-react";
import { motion } from "motion/react";

interface HUDProps {
  lives: number;
  stars: number;
  score: number;
  moves?: number;
  powerups?: {
    hints: number;
    skips: number;
    zaps: number;
  };
  onPowerup?: (type: "hint" | "skip" | "zap") => void;
}

export const HUD: React.FC<HUDProps> = ({ lives, stars, score, moves, powerups, onPowerup }) => {
  return (
    <div className="fixed top-0 left-0 right-0 z-50 p-4 flex flex-col gap-2 pointer-events-none">
      <div className="flex justify-between items-center w-full max-w-md mx-auto pointer-events-auto">
        <div className="flex gap-2">
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1 shadow-md border border-pink-200"
          >
            <Heart className="w-4 h-4 text-pink-500 fill-pink-500" />
            <span className="font-bold text-pink-700">{lives}</span>
          </motion.div>
          <motion.div 
            whileHover={{ scale: 1.05 }}
            className="bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1 shadow-md border border-yellow-200"
          >
            <Star className="w-4 h-4 text-yellow-500 fill-yellow-500" />
            <span className="font-bold text-yellow-700">{stars}</span>
          </motion.div>
        </div>

        <motion.div 
          whileHover={{ scale: 1.05 }}
          className="bg-white/90 backdrop-blur-sm rounded-full px-4 py-1 flex items-center gap-2 shadow-md border border-indigo-200"
        >
          <Trophy className="w-4 h-4 text-indigo-500" />
          <span className="font-bold text-indigo-700">{score.toLocaleString()}</span>
        </motion.div>

        {moves !== undefined && (
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="bg-white/90 backdrop-blur-sm rounded-full px-3 py-1 flex items-center gap-1 shadow-md border border-orange-200"
          >
            <span className="text-xs font-bold text-orange-400 uppercase tracking-tighter">Moves</span>
            <span className="font-bold text-orange-700">{moves}</span>
          </motion.div>
        )}
      </div>

      {powerups && onPowerup && (
        <div className="flex justify-center gap-4 mt-2 pointer-events-auto">
          <PowerupButton 
            icon={<Lightbulb className="w-5 h-5" />} 
            count={powerups.hints} 
            color="bg-yellow-400" 
            onClick={() => onPowerup("hint")}
            label="Hint"
          />
          <PowerupButton 
            icon={<FastForward className="w-5 h-5" />} 
            count={powerups.skips} 
            color="bg-green-400" 
            onClick={() => onPowerup("skip")}
            label="Skip"
          />
          <PowerupButton 
            icon={<Zap className="w-5 h-5" />} 
            count={powerups.zaps} 
            color="bg-purple-400" 
            onClick={() => onPowerup("zap")}
            label="Zap"
          />
        </div>
      )}
    </div>
  );
};

const PowerupButton: React.FC<{ icon: React.ReactNode; count: number; color: string; onClick: () => void; label: string }> = ({ icon, count, color, onClick, label }) => (
  <motion.button
    whileHover={{ scale: 1.1 }}
    whileTap={{ scale: 0.9 }}
    onClick={onClick}
    disabled={count <= 0}
    className={`relative group flex flex-col items-center gap-1 ${count <= 0 ? 'opacity-50 grayscale' : ''}`}
  >
    <div className={`w-12 h-12 rounded-full ${color} flex items-center justify-center text-white shadow-lg border-2 border-white/50`}>
      {icon}
      <span className="absolute -top-1 -right-1 bg-white text-gray-800 text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center shadow-sm border border-gray-200">
        {count}
      </span>
    </div>
    <span className="text-[10px] font-bold text-white uppercase tracking-widest drop-shadow-md">{label}</span>
  </motion.button>
);

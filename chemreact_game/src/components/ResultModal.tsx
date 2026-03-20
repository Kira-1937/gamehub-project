/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from "react";
import { motion, AnimatePresence } from "motion/react";
import { Star, Trophy, RefreshCw, Map as MapIcon, ChevronRight } from "lucide-react";

interface ResultModalProps {
  status: "won" | "lost";
  score: number;
  moves: number;
  maxCombo: number;
  onRetry: () => void;
  onMap: () => void;
  onNext?: () => void;
}

export const ResultModal: React.FC<ResultModalProps> = ({ status, score, moves, maxCombo, onRetry, onMap, onNext }) => {
  const stars = moves > 5 ? 3 : moves > 2 ? 2 : 1;

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-black/60 backdrop-blur-sm"
    >
      <motion.div 
        initial={{ scale: 0.8, y: 50 }}
        animate={{ scale: 1, y: 0 }}
        className="w-full max-w-sm bg-white rounded-3xl p-8 shadow-2xl relative overflow-hidden"
      >
        {/* Background Sparkles */}
        <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-10">
          {[...Array(10)].map((_, i) => (
            <Star key={i} className="absolute w-8 h-8 text-yellow-500" style={{ top: `${Math.random()*100}%`, left: `${Math.random()*100}%` }} />
          ))}
        </div>

        <div className="relative z-10 flex flex-col items-center gap-6 text-center">
          <motion.div 
            initial={{ rotate: -10, scale: 0 }}
            animate={{ rotate: 0, scale: 1 }}
            transition={{ delay: 0.2, type: "spring" }}
            className={`w-24 h-24 rounded-full flex items-center justify-center shadow-lg border-4 border-white ${status === 'won' ? 'bg-yellow-400' : 'bg-red-400'}`}
          >
            {status === 'won' ? <Trophy className="w-12 h-12 text-white" /> : <RefreshCw className="w-12 h-12 text-white" />}
          </motion.div>

          <div className="space-y-1">
            <h2 className={`text-4xl font-black uppercase tracking-tighter ${status === 'won' ? 'text-yellow-500' : 'text-red-500'}`}>
              {status === 'won' ? 'Level Complete!' : 'Level Failed!'}
            </h2>
            <p className="text-gray-400 font-bold text-sm uppercase tracking-widest">
              {status === 'won' ? 'Great job, chemist!' : 'Keep practicing!'}
            </p>
          </div>

          {status === 'won' && (
            <div className="flex gap-2">
              {[...Array(3)].map((_, i) => (
                <motion.div
                  key={i}
                  initial={{ scale: 0, rotate: -20 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ delay: 0.4 + i * 0.1 }}
                >
                  <Star className={`w-12 h-12 ${i < stars ? 'text-yellow-400 fill-yellow-400' : 'text-gray-200 fill-gray-200'}`} />
                </motion.div>
              ))}
            </div>
          )}

          <div className="w-full grid grid-cols-3 gap-4 bg-gray-50 rounded-2xl p-4 border border-gray-100">
            <div className="flex flex-col items-center">
              <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Score</span>
              <span className="text-xl font-black text-indigo-600">{score.toLocaleString()}</span>
            </div>
            <div className="flex flex-col items-center border-x border-gray-200">
              <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Combo</span>
              <span className="text-xl font-black text-pink-600">x{maxCombo}</span>
            </div>
            <div className="flex flex-col items-center">
              <span className="text-[10px] font-black text-gray-400 uppercase tracking-widest">Moves</span>
              <span className="text-xl font-black text-orange-600">{moves}</span>
            </div>
          </div>

          <div className="w-full flex flex-col gap-3">
            {status === 'won' && onNext && (
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onNext}
                className="w-full bg-indigo-600 text-white font-black py-4 rounded-2xl shadow-lg shadow-indigo-200 flex items-center justify-center gap-2 uppercase tracking-widest"
              >
                Next Level <ChevronRight className="w-5 h-5" />
              </motion.button>
            )}
            
            <div className="flex gap-3">
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onRetry}
                className="flex-1 bg-white border-2 border-gray-100 text-gray-600 font-black py-4 rounded-2xl flex items-center justify-center gap-2 uppercase tracking-widest"
              >
                <RefreshCw className="w-5 h-5" /> Retry
              </motion.button>
              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                onClick={onMap}
                className="flex-1 bg-white border-2 border-gray-100 text-gray-600 font-black py-4 rounded-2xl flex items-center justify-center gap-2 uppercase tracking-widest"
              >
                <MapIcon className="w-5 h-5" /> Map
              </motion.button>
            </div>
          </div>
        </div>
      </motion.div>
    </motion.div>
  );
};

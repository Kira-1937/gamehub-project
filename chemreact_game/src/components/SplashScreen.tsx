/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from "react";
import { motion } from "motion/react";
import { Play, FlaskConical } from "lucide-react";

interface SplashScreenProps {
  onStart: () => void;
}

export const SplashScreen: React.FC<SplashScreenProps> = ({ onStart }) => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 via-purple-600 to-pink-500 flex flex-col items-center justify-center p-8 text-center relative overflow-hidden">
      {/* Background Bubbles */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        {[...Array(15)].map((_, i) => (
          <motion.div
            key={i}
            initial={{ y: "110vh", x: `${Math.random() * 100}vw`, opacity: 0 }}
            animate={{ 
              y: "-10vh", 
              opacity: [0, 0.2, 0.2, 0],
              scale: [1, 1.2, 0.8, 1]
            }}
            transition={{ 
              duration: 5 + Math.random() * 10, 
              repeat: Infinity, 
              delay: Math.random() * 5,
              ease: "linear"
            }}
            className="absolute w-12 h-12 rounded-full bg-white/20 backdrop-blur-sm border border-white/30"
          />
        ))}
      </div>

      <div className="relative z-10 flex flex-col items-center gap-8">
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 100, damping: 10 }}
          className="w-32 h-32 bg-white rounded-full flex items-center justify-center shadow-2xl border-4 border-white/50"
        >
          <FlaskConical className="w-16 h-16 text-indigo-600" />
        </motion.div>

        <div className="space-y-2">
          <motion.h1 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.3 }}
            className="text-6xl font-black text-white uppercase tracking-tighter drop-shadow-2xl"
          >
            ChemReact
          </motion.h1>
          <motion.p 
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ delay: 0.4 }}
            className="text-white/80 font-bold text-lg uppercase tracking-widest"
          >
            Chain Reaction Puzzles
          </motion.p>
        </div>

        <motion.button
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          whileHover={{ scale: 1.1, rotate: 2 }}
          whileTap={{ scale: 0.9 }}
          transition={{ delay: 0.6, type: "spring" }}
          onClick={onStart}
          className="group relative bg-white text-indigo-600 font-black px-12 py-5 rounded-full shadow-2xl shadow-indigo-900/40 flex items-center gap-3 text-2xl uppercase tracking-widest overflow-hidden"
        >
          <div className="absolute inset-0 bg-indigo-50 translate-y-full group-hover:translate-y-0 transition-transform duration-300" />
          <Play className="w-8 h-8 relative z-10 fill-indigo-600" />
          <span className="relative z-10">Play Now</span>
        </motion.button>

        <motion.div 
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 1 }}
          className="mt-12 text-white/50 text-xs font-bold uppercase tracking-widest"
        >
          Master the elements, solve the reactions
        </motion.div>
      </div>
    </div>
  );
};

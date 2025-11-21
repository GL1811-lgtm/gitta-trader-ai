import React from 'react';
import { motion } from 'framer-motion';
import clsx from 'clsx';

interface HolographicCardProps {
    children: React.ReactNode;
    className?: string;
    title?: string;
}

export const HolographicCard: React.FC<HolographicCardProps> = ({ children, className, title }) => {
    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className={clsx(
                'glass-card p-6 relative overflow-hidden',
                className
            )}
        >
            {/* Glowing Border Effect */}
            <div className="absolute inset-0 border border-white/10 rounded-2xl pointer-events-none" />
            <div className="absolute -inset-1 bg-gradient-to-r from-[var(--neon-cyan)] to-[var(--neon-purple)] opacity-20 blur-xl rounded-2xl -z-10" />

            {title && (
                <h3 className="text-xl font-bold mb-4 text-neon tracking-wider uppercase">
                    {title}
                </h3>
            )}

            <div className="relative z-10">
                {children}
            </div>
        </motion.div>
    );
};

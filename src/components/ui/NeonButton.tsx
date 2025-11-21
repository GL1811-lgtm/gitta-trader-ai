import React from 'react';
import { motion, HTMLMotionProps } from 'framer-motion';
import clsx from 'clsx';

interface NeonButtonProps extends Omit<HTMLMotionProps<"button">, "ref"> {
    variant?: 'cyan' | 'purple' | 'danger';
    glow?: boolean;
    children: React.ReactNode;
}

export const NeonButton: React.FC<NeonButtonProps> = ({
    children,
    className,
    variant = 'cyan',
    glow = true,
    ...props
}) => {
    const colors = {
        cyan: 'border-[var(--neon-cyan)] text-[var(--neon-cyan)] hover:bg-[var(--neon-cyan)] hover:text-black',
        purple: 'border-[var(--neon-purple)] text-[var(--neon-purple)] hover:bg-[var(--neon-purple)] hover:text-white',
        danger: 'border-[var(--neon-red)] text-[var(--neon-red)] hover:bg-[var(--neon-red)] hover:text-white',
    };

    return (
        <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className={clsx(
                'px-6 py-2 rounded-lg font-bold uppercase tracking-widest transition-all duration-300',
                'border-2 bg-transparent backdrop-blur-sm',
                colors[variant],
                glow && 'shadow-[0_0_15px_rgba(0,0,0,0.3)] hover:shadow-[0_0_25px_currentColor]',
                className
            )}
            {...props}
        >
            {children}
        </motion.button>
    );
};

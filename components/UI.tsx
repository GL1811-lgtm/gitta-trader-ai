import React, { FC } from 'react';

export const Card: FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => (
    <div className={`glass-card p-4 sm:p-6 transition-transform duration-300 hover:scale-[1.01] ${className || ''}`}>
        {children}
    </div>
);

export const SectionTitle: FC<{ children: React.ReactNode, className?: string }> = ({ children, className }) => (
    <h2 className={`text-xl sm:text-2xl font-bold text-slate-100 mb-4 ${className || ''}`}>{children}</h2>
);

export const Button: FC<{ onClick: () => void; children: React.ReactNode; isLoading?: boolean; className?: string; disabled?: boolean }> = ({ onClick, children, isLoading, className, disabled }) => (
    <button
        onClick={onClick}
        disabled={isLoading || disabled}
        className={`px-6 py-2 rounded-lg font-semibold text-white transition-all duration-300 flex items-center justify-center ${isLoading || disabled ? 'bg-secondary cursor-not-allowed' : 'bg-accent/80 hover:bg-accent text-primary'
            } ${className || ''}`}
    >
        {isLoading ? (
            <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
        ) : (
            children
        )}
    </button>
);

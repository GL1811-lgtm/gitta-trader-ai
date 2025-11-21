// FIX: Import React to resolve 'React' namespace error for React.ElementType.
import React from 'react';

export type Page = 'dashboard' | 'stocksearch' | 'alerts' | 'analysis' | 'airesearch' | 'learning' | 'agents' | 'settings' | 'reports' | 'papertrading';

export interface NavItem {
  id: Page;
  label: string;
  icon: React.ElementType;
}

export interface Alert {
  id: string;
  instrument: string;
  type: 'BUY' | 'SELL';
  confidence: number;
  reason: string;
  timestamp: string;
  strikePrice: number;
  targetPrice: number;
  stopLoss: number;
}

export interface MarketIndex {
  name: string;
  value: number;
  change: number;
  changePercent: number;
}

export interface LearningLogEntry {
  id: string;
  timestamp: string;
  title: string;
  summary: string;
  accuracyChange: number;
}

export interface ChartDataPoint {
  time: string;
  open: number;
  high: number;
  low: number;
  close: number;
}

export type AgentType = 'Collector' | 'Tester' | 'Supervisor' | 'Expert';
export type AgentStatusState = 'Online' | 'Processing' | 'Idle' | 'Error' | 'Fetching';

export interface AgentDetail {
  id: string;
  name: string;
  type: AgentType;
  status: AgentStatusState;
  activity: string;
  cpu: number;
  memory: number;
}


export interface ChatMessage {
  sender: 'user' | 'ai';
  text: string;
}
# Track0r React Native Implementation Plan

## Overview

This document outlines a comprehensive plan to create a React Native mobile application for the track0r system, leveraging the same data-driven architecture proposed in the web refactor. The React Native app will provide native mobile performance, enhanced user experience, and cross-platform compatibility while maintaining the same JSON-based game data structure.

## React Native Advantages & Mobile-First Benefits

### **Why React Native?**

**Cross-Platform Efficiency:**
- Single codebase for iOS, Android, and Web (via React Native Web)
- Shared business logic and data management
- Consistent user experience across platforms
- Reduced development and maintenance costs

**Native Performance Benefits:**
- Native UI components for smooth performance
- Hardware-accelerated animations and transitions
- Native gesture recognition and haptic feedback
- Optimal memory management and rendering

**Mobile-Specific Enhancements:**
- Offline-first architecture with local storage
- Push notifications for turn reminders and game updates
- Camera integration for QR code game loading
- Device-specific features (Dark mode, accessibility)
- Native navigation patterns and gestures

## Architecture Overview

### **Data Layer Compatibility**
The existing JSON data structure from the web refactor works perfectly with React Native:

```typescript
interface GameData {
  gameInfo: {
    title: string;
    subtitle: string;
    version: string;
    description: string;
    rulebookReferences: string[];
  };
  tabs: GameTab[];
  formatting: FormattingRules;
  styles?: CustomStyles;
}

interface GameTab {
  id: string;
  name: string;
  steps: GameStep[];
}

interface GameStep {
  id: string;
  title: string;
  detail: string;
  substeps?: GameSubstep[];
}

interface FormattingRules {
  gameTerms: string[];      // Terms to emphasize with italics
  actionWords: string[];    // Action words to bold
  measurements: string[];   // Measurement patterns to bold
  customRules?: CustomRule[];
}
```

### **Project Structure**
```
track0r-mobile/
├── src/
│   ├── components/              # Reusable UI components
│   │   ├── common/
│   │   │   ├── LoadingScreen.tsx
│   │   │   ├── ErrorScreen.tsx
│   │   │   └── SearchBar.tsx
│   │   ├── game/
│   │   │   ├── GameStep.tsx
│   │   │   ├── GameSubstep.tsx
│   │   │   ├── DetailPanel.tsx
│   │   │   ├── TabNavigator.tsx
│   │   │   ├── NavigationButtons.tsx
│   │   │   └── StepsList.tsx
│   │   └── library/
│   │       ├── GameCard.tsx
│   │       ├── GameGrid.tsx
│   │       └── FilterPanel.tsx
│   ├── screens/                 # Screen components
│   │   ├── GameLibraryScreen.tsx
│   │   ├── GameScreen.tsx
│   │   ├── SettingsScreen.tsx
│   │   ├── AboutScreen.tsx
│   │   └── GameDownloadScreen.tsx
│   ├── navigation/              # Navigation configuration
│   │   ├── AppNavigator.tsx
│   │   ├── TabNavigator.tsx
│   │   └── StackNavigator.tsx
│   ├── services/               # Data management services
│   │   ├── GameDataService.ts
│   │   ├── StorageService.ts
│   │   ├── FormattingService.ts
│   │   ├── NotificationService.ts
│   │   ├── UpdateService.ts
│   │   └── AnalyticsService.ts
│   ├── hooks/                  # Custom React hooks
│   │   ├── useGameData.ts
│   │   ├── useGameNavigation.ts
│   │   ├── useSettings.ts
│   │   ├── useOfflineStorage.ts
│   │   ├── useTurnTimer.ts
│   │   └── useTheme.ts
│   ├── contexts/               # React contexts
│   │   ├── GameContext.tsx
│   │   ├── ThemeContext.tsx
│   │   ├── SettingsContext.tsx
│   │   └── NavigationContext.tsx
│   ├── types/                  # TypeScript interfaces
│   │   ├── Game.ts
│   │   ├── Navigation.ts
│   │   ├── Settings.ts
│   │   ├── Storage.ts
│   │   └── API.ts
│   ├── utils/                  # Helper functions
│   │   ├── formatting.ts
│   │   ├── validation.ts
│   │   ├── dateHelpers.ts
│   │   ├── deviceInfo.ts
│   │   └── accessibility.ts
│   ├── constants/              # App constants
│   │   ├── colors.ts
│   │   ├── dimensions.ts
│   │   ├── fonts.ts
│   │   └── config.ts
│   └── styles/                 # Shared styles
│       ├── global.ts
│       ├── themes.ts
│       └── components.ts
├── assets/                     # Static assets
│   ├── data/                   # Bundled game data
│   │   ├── stalker.json
│   │   ├── star_wars_unlimited.json
│   │   ├── wondrous_creatures.json
│   │   ├── wondrous_creatures_solo.json
│   │   ├── game_index.json
│   │   └── schema.json
│   ├── images/                 # App icons and images
│   │   ├── game-icons/
│   │   ├── splash/
│   │   └── common/
│   └── fonts/                  # Custom fonts
├── scripts/                    # Build and utility scripts
│   ├── validate-game-data.js
│   ├── bundle-game-data.js
│   ├── generate-icons.js
│   └── update-version.js
├── __tests__/                  # Test files
│   ├── components/
│   ├── services/
│   ├── hooks/
│   └── utils/
├── docs/                       # Documentation
│   ├── setup.md
│   ├── game-data-format.md
│   ├── development-guide.md
│   └── deployment.md
├── app.json                    # Expo configuration
├── package.json
├── tsconfig.json
├── babel.config.js
└── metro.config.js
```

## Core Services Implementation

### **GameDataService.ts**
```typescript
interface GameMetadata {
  id: string;
  title: string;
  subtitle: string;
  description: string;
  version: string;
  size: number;
  lastUpdated: string;
  bundled: boolean;
  downloaded: boolean;
  category: string[];
  difficulty: 'Beginner' | 'Intermediate' | 'Advanced';
  playerCount: string;
  playTime: string;
  iconUrl?: string;
}

class GameDataService {
  private static instance: GameDataService;
  private games: Map<string, GameData> = new Map();
  private metadata: Map<string, GameMetadata> = new Map();
  
  static getInstance(): GameDataService {
    if (!GameDataService.instance) {
      GameDataService.instance = new GameDataService();
    }
    return GameDataService.instance;
  }

  async initialize(): Promise<void> {
    await this.loadGameIndex();
    await this.loadBundledGames();
    await this.checkForUpdates();
  }

  async loadGame(gameId: string): Promise<GameData> {
    if (!this.games.has(gameId)) {
      const gameData = await this.loadGameData(gameId);
      this.games.set(gameId, gameData);
    }
    return this.games.get(gameId)!;
  }

  async getAllGames(): Promise<GameMetadata[]> {
    return Array.from(this.metadata.values());
  }

  async searchGames(query: string, filters?: GameFilter): Promise<GameMetadata[]> {
    const allGames = await this.getAllGames();
    return allGames.filter(game => {
      const matchesQuery = game.title.toLowerCase().includes(query.toLowerCase()) ||
                          game.description.toLowerCase().includes(query.toLowerCase());
      
      const matchesFilters = !filters || (
        (!filters.category || filters.category.some(cat => game.category.includes(cat))) &&
        (!filters.difficulty || game.difficulty === filters.difficulty) &&
        (!filters.playerCount || this.matchesPlayerCount(game.playerCount, filters.playerCount))
      );
      
      return matchesQuery && matchesFilters;
    });
  }

  async downloadGame(gameId: string, onProgress?: (progress: number) => void): Promise<void> {
    const metadata = this.metadata.get(gameId);
    if (!metadata) throw new Error(`Game ${gameId} not found`);
    
    if (metadata.bundled) return; // Already available
    
    try {
      const gameData = await this.fetchGameFromServer(gameId, onProgress);
      await StorageService.saveGame(gameId, gameData);
      metadata.downloaded = true;
      this.games.set(gameId, gameData);
    } catch (error) {
      throw new Error(`Failed to download ${gameId}: ${error.message}`);
    }
  }

  async checkForUpdates(): Promise<UpdateInfo[]> {
    try {
      const serverIndex = await this.fetchGameIndex();
      const updates: UpdateInfo[] = [];
      
      for (const [gameId, localMetadata] of this.metadata) {
        const serverMetadata = serverIndex.games.find(g => g.id === gameId);
        if (serverMetadata && serverMetadata.version !== localMetadata.version) {
          updates.push({
            gameId,
            currentVersion: localMetadata.version,
            availableVersion: serverMetadata.version,
            size: serverMetadata.size
          });
        }
      }
      
      return updates;
    } catch (error) {
      console.warn('Update check failed:', error);
      return [];
    }
  }

  private async loadGameIndex(): Promise<void> {
    const gameIndex = require('../../assets/data/game_index.json');
    gameIndex.games.forEach((game: GameMetadata) => {
      this.metadata.set(game.id, game);
    });
  }

  private async loadBundledGames(): Promise<void> {
    const bundledGames = Array.from(this.metadata.values())
      .filter(game => game.bundled);
    
    await Promise.all(
      bundledGames.map(async (game) => {
        try {
          const gameData = require(`../../assets/data/${game.id}.json`);
          this.games.set(game.id, gameData);
        } catch (error) {
          console.error(`Failed to load bundled game ${game.id}:`, error);
        }
      })
    );
  }

  private async loadGameData(gameId: string): Promise<GameData> {
    // Try loading from storage first (downloaded games)
    const stored = await StorageService.loadGame(gameId);
    if (stored) return stored;
    
    // Try loading from bundled assets
    try {
      return require(`../../assets/data/${gameId}.json`);
    } catch (error) {
      throw new Error(`Game ${gameId} not found locally and not available for download`);
    }
  }

  private async fetchGameFromServer(gameId: string, onProgress?: (progress: number) => void): Promise<GameData> {
    // Implementation for downloading games from server
    const response = await fetch(`${CONFIG.API_BASE_URL}/games/${gameId}`);
    
    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }
    
    const contentLength = response.headers.get('content-length');
    if (contentLength && onProgress) {
      const total = parseInt(contentLength, 10);
      let loaded = 0;
      
      const reader = response.body?.getReader();
      const chunks: Uint8Array[] = [];
      
      while (reader) {
        const { done, value } = await reader.read();
        if (done) break;
        
        chunks.push(value);
        loaded += value.length;
        onProgress(loaded / total);
      }
      
      const gameDataText = new TextDecoder().decode(
        new Uint8Array(chunks.reduce((acc, chunk) => acc + chunk.length, 0))
      );
      return JSON.parse(gameDataText);
    }
    
    return response.json();
  }

  private async fetchGameIndex(): Promise<{ games: GameMetadata[] }> {
    const response = await fetch(`${CONFIG.API_BASE_URL}/games/index`);
    return response.json();
  }

  private matchesPlayerCount(gamePlayerCount: string, filterPlayerCount: string): boolean {
    // Implementation for matching player count ranges
    // e.g., "1-4" matches "2", "2-6" matches "3", etc.
    return true; // Simplified for brevity
  }
}
```

### **StorageService.ts**
```typescript
import AsyncStorage from '@react-native-async-storage/async-storage';

interface GameProgress {
  gameId: string;
  currentTab: string;
  selectedIndex: number;
  lastPlayed: string;
  bookmarks: string[];
  notes: { [stepId: string]: string };
}

interface UserSettings {
  theme: 'light' | 'dark' | 'auto';
  fontSize: 'small' | 'medium' | 'large';
  hapticFeedback: boolean;
  notifications: boolean;
  autoSync: boolean;
  language: string;
}

class StorageService {
  private static readonly KEYS = {
    GAME_PROGRESS: 'game_progress_',
    USER_SETTINGS: 'user_settings',
    DOWNLOADED_GAMES: 'downloaded_games',
    BOOKMARKS: 'bookmarks_',
    NOTES: 'notes_',
    RECENT_GAMES: 'recent_games',
    FAVORITES: 'favorite_games'
  };

  // Game Progress Management
  static async saveGameProgress(gameId: string, progress: GameProgress): Promise<void> {
    const key = `${this.KEYS.GAME_PROGRESS}${gameId}`;
    await AsyncStorage.setItem(key, JSON.stringify(progress));
  }

  static async loadGameProgress(gameId: string): Promise<GameProgress | null> {
    const key = `${this.KEYS.GAME_PROGRESS}${gameId}`;
    const stored = await AsyncStorage.getItem(key);
    return stored ? JSON.parse(stored) : null;
  }

  static async clearGameProgress(gameId: string): Promise<void> {
    const key = `${this.KEYS.GAME_PROGRESS}${gameId}`;
    await AsyncStorage.removeItem(key);
  }

  // Downloaded Games Management
  static async saveGame(gameId: string, gameData: GameData): Promise<void> {
    const key = `game_data_${gameId}`;
    await AsyncStorage.setItem(key, JSON.stringify(gameData));
    
    // Update downloaded games list
    const downloaded = await this.getDownloadedGames();
    if (!downloaded.includes(gameId)) {
      downloaded.push(gameId);
      await AsyncStorage.setItem(this.KEYS.DOWNLOADED_GAMES, JSON.stringify(downloaded));
    }
  }

  static async loadGame(gameId: string): Promise<GameData | null> {
    const key = `game_data_${gameId}`;
    const stored = await AsyncStorage.getItem(key);
    return stored ? JSON.parse(stored) : null;
  }

  static async deleteGame(gameId: string): Promise<void> {
    const key = `game_data_${gameId}`;
    await AsyncStorage.removeItem(key);
    
    // Update downloaded games list
    const downloaded = await this.getDownloadedGames();
    const updated = downloaded.filter(id => id !== gameId);
    await AsyncStorage.setItem(this.KEYS.DOWNLOADED_GAMES, JSON.stringify(updated));
  }

  static async getDownloadedGames(): Promise<string[]> {
    const stored = await AsyncStorage.getItem(this.KEYS.DOWNLOADED_GAMES);
    return stored ? JSON.parse(stored) : [];
  }

  // Bookmarks Management
  static async saveBookmarks(gameId: string, bookmarks: string[]): Promise<void> {
    const key = `${this.KEYS.BOOKMARKS}${gameId}`;
    await AsyncStorage.setItem(key, JSON.stringify(bookmarks));
  }

  static async loadBookmarks(gameId: string): Promise<string[]> {
    const key = `${this.KEYS.BOOKMARKS}${gameId}`;
    const stored = await AsyncStorage.getItem(key);
    return stored ? JSON.parse(stored) : [];
  }

  static async addBookmark(gameId: string, stepId: string): Promise<void> {
    const bookmarks = await this.loadBookmarks(gameId);
    if (!bookmarks.includes(stepId)) {
      bookmarks.push(stepId);
      await this.saveBookmarks(gameId, bookmarks);
    }
  }

  static async removeBookmark(gameId: string, stepId: string): Promise<void> {
    const bookmarks = await this.loadBookmarks(gameId);
    const updated = bookmarks.filter(id => id !== stepId);
    await this.saveBookmarks(gameId, updated);
  }

  // Notes Management
  static async saveNote(gameId: string, stepId: string, note: string): Promise<void> {
    const key = `${this.KEYS.NOTES}${gameId}`;
    const notes = await this.loadNotes(gameId);
    notes[stepId] = note;
    await AsyncStorage.setItem(key, JSON.stringify(notes));
  }

  static async loadNotes(gameId: string): Promise<{ [stepId: string]: string }> {
    const key = `${this.KEYS.NOTES}${gameId}`;
    const stored = await AsyncStorage.getItem(key);
    return stored ? JSON.parse(stored) : {};
  }

  static async deleteNote(gameId: string, stepId: string): Promise<void> {
    const key = `${this.KEYS.NOTES}${gameId}`;
    const notes = await this.loadNotes(gameId);
    delete notes[stepId];
    await AsyncStorage.setItem(key, JSON.stringify(notes));
  }

  // User Settings
  static async saveSettings(settings: UserSettings): Promise<void> {
    await AsyncStorage.setItem(this.KEYS.USER_SETTINGS, JSON.stringify(settings));
  }

  static async loadSettings(): Promise<UserSettings> {
    const stored = await AsyncStorage.getItem(this.KEYS.USER_SETTINGS);
    return stored ? JSON.parse(stored) : this.getDefaultSettings();
  }

  static getDefaultSettings(): UserSettings {
    return {
      theme: 'auto',
      fontSize: 'medium',
      hapticFeedback: true,
      notifications: true,
      autoSync: false,
      language: 'en'
    };
  }

  // Recent Games
  static async addRecentGame(gameId: string): Promise<void> {
    const recent = await this.getRecentGames();
    const updated = [gameId, ...recent.filter(id => id !== gameId)].slice(0, 10);
    await AsyncStorage.setItem(this.KEYS.RECENT_GAMES, JSON.stringify(updated));
  }

  static async getRecentGames(): Promise<string[]> {
    const stored = await AsyncStorage.getItem(this.KEYS.RECENT_GAMES);
    return stored ? JSON.parse(stored) : [];
  }

  // Favorites
  static async addFavorite(gameId: string): Promise<void> {
    const favorites = await this.getFavorites();
    if (!favorites.includes(gameId)) {
      favorites.push(gameId);
      await AsyncStorage.setItem(this.KEYS.FAVORITES, JSON.stringify(favorites));
    }
  }

  static async removeFavorite(gameId: string): Promise<void> {
    const favorites = await this.getFavorites();
    const updated = favorites.filter(id => id !== gameId);
    await AsyncStorage.setItem(this.KEYS.FAVORITES, JSON.stringify(updated));
  }

  static async getFavorites(): Promise<string[]> {
    const stored = await AsyncStorage.getItem(this.KEYS.FAVORITES);
    return stored ? JSON.parse(stored) : [];
  }

  static async isFavorite(gameId: string): Promise<boolean> {
    const favorites = await this.getFavorites();
    return favorites.includes(gameId);
  }

  // Utility Methods
  static async clearAllData(): Promise<void> {
    await AsyncStorage.clear();
  }

  static async getStorageSize(): Promise<number> {
    const keys = await AsyncStorage.getAllKeys();
    let totalSize = 0;
    
    for (const key of keys) {
      const value = await AsyncStorage.getItem(key);
      if (value) {
        totalSize += new Blob([value]).size;
      }
    }
    
    return totalSize;
  }
}
```

### **FormattingService.ts**
```typescript
class FormattingService {
  private static formatCache: Map<string, string> = new Map();

  static formatDetailText(text: string, formatting: FormattingRules): string {
    // Check cache first for performance
    const cacheKey = `${text.substring(0, 50)}_${JSON.stringify(formatting)}`;
    if (this.formatCache.has(cacheKey)) {
      return this.formatCache.get(cacheKey)!;
    }

    const formatted = this.processText(text, formatting);
    
    // Cache result (limit cache size)
    if (this.formatCache.size > 100) {
      const firstKey = this.formatCache.keys().next().value;
      this.formatCache.delete(firstKey);
    }
    this.formatCache.set(cacheKey, formatted);
    
    return formatted;
  }

  private static processText(text: string, formatting: FormattingRules): string {
    // Extract page reference
    const pageMatch = text.match(/\(([^)]*p\.\s*[^)]+)\)/);
    const pageRef = pageMatch ? 
      `<span class="page-ref">${pageMatch[1]}</span>` : '';
    const cleanText = text.replace(/\([^)]*p\.\s*[^)]+\)/, '').trim();

    // Check for explicit bullet points first
    if (cleanText.includes('•')) {
      return this.formatBulletPoints(cleanText, pageRef, formatting);
    }

    // Apply formatting rules
    let formatted = this.applyFormattingRules(cleanText, formatting);

    // Split into sentences and create bullet points if multiple sentences
    const sentences = formatted.split(/(?<=[.!?])\s+(?=[A-Z])/);

    if (sentences.length <= 2) {
      return `<p>${formatted}</p>${pageRef}`;
    }

    const bulletPoints = sentences.map(sentence => 
      `<li>${sentence.trim()}</li>`
    ).join('');

    return `<ul>${bulletPoints}</ul>${pageRef}`;
  }

  private static formatBulletPoints(text: string, pageRef: string, formatting: FormattingRules): string {
    const parts = text.split('•').filter(part => part.trim());
    const introText = parts[0].trim();
    const bulletItems = parts.slice(1);

    const formattedIntro = this.applyFormattingRules(introText, formatting);
    const bulletPoints = bulletItems.map(item => 
      `<li>${this.applyFormattingRules(item.trim(), formatting)}</li>`
    ).join('');

    return `<p>${formattedIntro}</p><ul>${bulletPoints}</ul>${pageRef}`;
  }

  private static applyFormattingRules(text: string, formatting: FormattingRules): string {
    let formatted = text;

    // Apply game terms (italics)
    if (formatting.gameTerms && formatting.gameTerms.length > 0) {
      const gameTermsPattern = new RegExp(
        `\\b(${formatting.gameTerms.join('|')})\\b`, 'g'
      );
      formatted = formatted.replace(gameTermsPattern, '<em>$1</em>');
    }

    // Apply action words (bold)
    if (formatting.actionWords && formatting.actionWords.length > 0) {
      const actionPattern = new RegExp(
        `\\b(${formatting.actionWords.join('|')})\\b`, 'gi'
      );
      formatted = formatted.replace(actionPattern, '<strong>$1</strong>');
    }

    // Apply measurements (bold)
    if (formatting.measurements && formatting.measurements.length > 0) {
      formatting.measurements.forEach(pattern => {
        const regex = new RegExp(`\\b(${pattern})\\b`, 'g');
        formatted = formatted.replace(regex, '<strong>$1</strong>');
      });
    }

    // Apply custom rules
    if (formatting.customRules && formatting.customRules.length > 0) {
      formatting.customRules.forEach(rule => {
        const regex = new RegExp(rule.pattern, rule.flags || 'g');
        formatted = formatted.replace(regex, rule.replacement);
      });
    }

    return formatted;
  }

  static clearCache(): void {
    this.formatCache.clear();
  }
}
```

## React Hooks Implementation

### **useGameData.ts**
```typescript
interface UseGameDataReturn {
  gameData: GameData | null;
  loading: boolean;
  error: string | null;
  refetch: () => Promise<void>;
}

export const useGameData = (gameId: string): UseGameDataReturn => {
  const [gameData, setGameData] = useState<GameData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadGame = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      
      const data = await GameDataService.getInstance().loadGame(gameId);
      setGameData(data);
      
      // Track recent game access
      await StorageService.addRecentGame(gameId);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load game data');
      setGameData(null);
    } finally {
      setLoading(false);
    }
  }, [gameId]);

  useEffect(() => {
    if (gameId) {
      loadGame();
    }
  }, [gameId, loadGame]);

  const refetch = useCallback(async () => {
    await loadGame();
  }, [loadGame]);

  return { gameData, loading, error, refetch };
};
```

### **useGameNavigation.ts**
```typescript
interface UseGameNavigationReturn {
  currentTab: string;
  selectedIndex: number;
  setCurrentTab: (tabId: string) => void;
  navigate: (direction: number) => void;
  goToStep: (index: number) => void;
  getCurrentSteps: () => (GameStep | GameSubstep)[];
  getCurrentStep: () => GameStep | GameSubstep | null;
  hasNextStep: boolean;
  hasPreviousStep: boolean;
}

export const useGameNavigation = (gameData: GameData | null): UseGameNavigationReturn => {
  const [currentTab, setCurrentTab] = useState<string>('');
  const [selectedIndices, setSelectedIndices] = useState<{ [tabId: string]: number }>({});

  // Initialize tabs and selection when gameData changes
  useEffect(() => {
    if (gameData && gameData.tabs.length > 0) {
      const firstTab = gameData.tabs[0];
      setCurrentTab(firstTab.id);
      
      // Initialize selection indices for all tabs
      const indices: { [tabId: string]: number } = {};
      gameData.tabs.forEach(tab => {
        indices[tab.id] = 0;
      });
      setSelectedIndices(indices);
    }
  }, [gameData]);

  const selectedIndex = selectedIndices[currentTab] || 0;

  const getCurrentSteps = useCallback((): (GameStep | GameSubstep)[] => {
    if (!gameData || !currentTab) return [];
    
    const tab = gameData.tabs.find(t => t.id === currentTab);
    if (!tab) return [];
    
    const allSteps: (GameStep | GameSubstep)[] = [];
    
    tab.steps.forEach(step => {
      allSteps.push(step);
      if (step.substeps) {
        allSteps.push(...step.substeps);
      }
    });
    
    return allSteps;
  }, [gameData, currentTab]);

  const getCurrentStep = useCallback((): GameStep | GameSubstep | null => {
    const steps = getCurrentSteps();
    return steps[selectedIndex] || null;
  }, [getCurrentSteps, selectedIndex]);

  const navigate = useCallback((direction: number) => {
    const steps = getCurrentSteps();
    if (steps.length === 0) return;
    
    const newIndex = Math.max(0, Math.min(steps.length - 1, selectedIndex + direction));
    setSelectedIndices(prev => ({
      ...prev,
      [currentTab]: newIndex
    }));
  }, [getCurrentSteps, selectedIndex, currentTab]);

  const goToStep = useCallback((index: number) => {
    const steps = getCurrentSteps();
    if (index >= 0 && index < steps.length) {
      setSelectedIndices(prev => ({
        ...prev,
        [currentTab]: index
      }));
    }
  }, [getCurrentSteps, currentTab]);

  const handleSetCurrentTab = useCallback((tabId: string) => {
    setCurrentTab(tabId);
  }, []);

  const steps = getCurrentSteps();
  const hasNextStep = selectedIndex < steps.length - 1;
  const hasPreviousStep = selectedIndex > 0;

  return {
    currentTab,
    selectedIndex,
    setCurrentTab: handleSetCurrentTab,
    navigate,
    goToStep,
    getCurrentSteps,
    getCurrentStep,
    hasNextStep,
    hasPreviousStep
  };
};
```

### **useTurnTimer.ts**
```typescript
interface TimerSettings {
  duration: number; // in seconds
  showWarning: boolean;
  warningThreshold: number; // seconds before end to show warning
  playSound: boolean;
  vibrate: boolean;
}

interface UseTurnTimerReturn {
  timeRemaining: number | null;
  isActive: boolean;
  isWarning: boolean;
  startTimer: (settings: TimerSettings) => void;
  pauseTimer: () => void;
  resumeTimer: () => void;
  stopTimer: () => void;
  resetTimer: () => void;
}

export const useTurnTimer = (): UseTurnTimerReturn => {
  const [timeRemaining, setTimeRemaining] = useState<number | null>(null);
  const [isActive, setIsActive] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [settings, setSettings] = useState<TimerSettings | null>(null);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);

  const isWarning = useMemo(() => {
    if (!timeRemaining || !settings) return false;
    return timeRemaining <= settings.warningThreshold;
  }, [timeRemaining, settings]);

  const startTimer = useCallback((timerSettings: TimerSettings) => {
    setSettings(timerSettings);
    setTimeRemaining(timerSettings.duration);
    setIsActive(true);
    setIsPaused(false);

    // Schedule notification for when timer expires
    NotificationService.scheduleTimerNotification(timerSettings.duration);
  }, []);

  const pauseTimer = useCallback(() => {
    setIsPaused(true);
    NotificationService.cancelTimerNotifications();
  }, []);

  const resumeTimer = useCallback(() => {
    setIsPaused(false);
    if (timeRemaining && settings) {
      NotificationService.scheduleTimerNotification(timeRemaining);
    }
  }, [timeRemaining, settings]);

  const stopTimer = useCallback(() => {
    setIsActive(false);
    setIsPaused(false);
    setTimeRemaining(null);
    setSettings(null);
    NotificationService.cancelTimerNotifications();
  }, []);

  const resetTimer = useCallback(() => {
    if (settings) {
      setTimeRemaining(settings.duration);
      setIsPaused(false);
      NotificationService.cancelTimerNotifications();
      if (isActive) {
        NotificationService.scheduleTimerNotification(settings.duration);
      }
    }
  }, [settings, isActive]);

  // Timer countdown effect
  useEffect(() => {
    if (isActive && !isPaused && timeRemaining !== null) {
      intervalRef.current = setInterval(() => {
        setTimeRemaining(prev => {
          if (prev === null || prev <= 0) {
            setIsActive(false);
            
            // Timer expired - trigger notifications
            if (settings?.playSound) {
              // Play sound
            }
            if (settings?.vibrate) {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);
            }
            
            return 0;
          }
          
          // Warning threshold reached
          if (settings?.showWarning && prev === settings.warningThreshold + 1) {
            if (settings.vibrate) {
              Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
            }
          }
          
          return prev - 1;
        });
      }, 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isActive, isPaused, timeRemaining, settings]);

  return {
    timeRemaining,
    isActive,
    isWarning,
    startTimer,
    pauseTimer,
    resumeTimer,
    stopTimer,
    resetTimer
  };
};
```

## Screen Components

### **GameScreen.tsx**
```typescript
interface GameScreenProps {
  route: { params: { gameId: string } };
  navigation: any;
}

export const GameScreen: React.FC<GameScreenProps> = ({ route, navigation }) => {
  const { gameId } = route.params;
  const { gameData, loading, error, refetch } = useGameData(gameId);
  const {
    currentTab,
    selectedIndex,
    setCurrentTab,
    navigate,
    getCurrentSteps,
    getCurrentStep,
    hasNextStep,
    hasPreviousStep
  } = useGameNavigation(gameData);
  
  const { theme } = useTheme();
  const styles = getStyles(theme);
  
  // Gesture handlers
  const panGesture = Gesture.Pan()
    .onUpdate((event) => {
      // Swipe left/right for tab switching
      if (Math.abs(event.translationX) > 100 && Math.abs(event.translationY) < 50) {
        if (event.translationX > 0 && gameData) {
          // Swipe right - previous tab
          const currentIndex = gameData.tabs.findIndex(tab => tab.id === currentTab);
          if (currentIndex > 0) {
            setCurrentTab(gameData.tabs[currentIndex - 1].id);
          }
        } else if (event.translationX < 0 && gameData) {
          // Swipe left - next tab
          const currentIndex = gameData.tabs.findIndex(tab => tab.id === currentTab);
          if (currentIndex < gameData.tabs.length - 1) {
            setCurrentTab(gameData.tabs[currentIndex + 1].id);
          }
        }
      }
      
      // Swipe up/down for step navigation
      if (Math.abs(event.translationY) > 50 && Math.abs(event.translationX) < 50) {
        if (event.translationY > 0 && hasPreviousStep) {
          navigate(-1);
        } else if (event.translationY < 0 && hasNextStep) {
          navigate(1);
        }
      }
    });

  // Keyboard navigation for external keyboards
  useEffect(() => {
    const keyboardHandler = (event: any) => {
      if (event.key === 'ArrowUp' && hasPreviousStep) {
        navigate(-1);
      } else if (event.key === 'ArrowDown' && hasNextStep) {
        navigate(1);
      }
    };

    // Add keyboard listener if available
    if (Platform.OS === 'web') {
      document.addEventListener('keydown', keyboardHandler);
      return () => document.removeEventListener('keydown', keyboardHandler);
    }
  }, [navigate, hasNextStep, hasPreviousStep]);

  // Header configuration
  useLayoutEffect(() => {
    navigation.setOptions({
      title: gameData?.gameInfo.title || 'Track0r',
      headerStyle: {
        backgroundColor: theme.colors.primary,
      },
      headerTintColor: theme.colors.onPrimary,
      headerRight: () => (
        <View style={styles.headerButtons}>
          <TouchableOpacity
            onPress={() => navigation.navigate('Settings', { gameId })}
            style={styles.headerButton}
          >
            <Icon name="settings" size={24} color={theme.colors.onPrimary} />
          </TouchableOpacity>
        </View>
      ),
    });
  }, [navigation, gameData, theme]);

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={styles.loadingText}>Loading game data...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.centered}>
        <Text style={styles.errorText}>Failed to load game</Text>
        <Text style={styles.errorMessage}>{error}</Text>
        <TouchableOpacity onPress={refetch} style={styles.retryButton}>
          <Text style={styles.retryButtonText}>Retry</Text>
        </TouchableOpacity>
      </View>
    );
  }

  if (!gameData) return null;

  const currentStep = getCurrentStep();
  const steps = getCurrentSteps();

  return (
    <GestureHandlerRootView style={styles.container}>
      <GestureDetector gesture={panGesture}>
        <SafeAreaView style={styles.safeArea}>
          {/* Navigation Buttons */}
          <NavigationButtons
            onPrevious={() => navigate(-1)}
            onNext={() => navigate(1)}
            hasPrevious={hasPreviousStep}
            hasNext={hasNextStep}
            theme={theme}
          />

          {/* Tab Navigator */}
          <TabNavigator
            tabs={gameData.tabs}
            currentTab={currentTab}
            onTabChange={setCurrentTab}
            theme={theme}
          />

          {/* Main Content */}
          <View style={styles.content}>
            {/* Steps List */}
            <View style={styles.stepsContainer}>
              <StepsList
                steps={steps}
                selectedIndex={selectedIndex}
                onStepSelect={(index) => {
                  setSelectedIndices(prev => ({
                    ...prev,
                    [currentTab]: index
                  }));
                }}
                theme={theme}
              />
            </View>

            {/* Detail Panel */}
            <View style={styles.detailContainer}>
              <DetailPanel
                step={currentStep}
                formatting={gameData.formatting}
                theme={theme}
              />
            </View>
          </View>

          {/* Progress Indicator */}
          <View style={styles.progressContainer}>
            <Text style={styles.progressText}>
              {selectedIndex + 1} of {steps.length}
            </Text>
            <View style={styles.progressBar}>
              <View 
                style={[
                  styles.progressFill, 
                  { width: `${((selectedIndex + 1) / steps.length) * 100}%` }
                ]} 
              />
            </View>
          </View>
        </SafeAreaView>
      </GestureDetector>
    </GestureHandlerRootView>
  );
};

const getStyles = (theme: Theme) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  safeArea: {
    flex: 1,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 20,
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: theme.colors.onBackground,
  },
  errorText: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.error,
    marginBottom: 8,
  },
  errorMessage: {
    fontSize: 14,
    color: theme.colors.onBackground,
    textAlign: 'center',
    marginBottom: 20,
  },
  retryButton: {
    backgroundColor: theme.colors.primary,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
  },
  retryButtonText: {
    color: theme.colors.onPrimary,
    fontSize: 16,
    fontWeight: '600',
  },
  headerButtons: {
    flexDirection: 'row',
  },
  headerButton: {
    padding: 8,
    marginLeft: 8,
  },
  content: {
    flex: 1,
    flexDirection: 'row',
  },
  stepsContainer: {
    flex: 1,
    borderRightWidth: 1,
    borderRightColor: theme.colors.border,
  },
  detailContainer: {
    flex: 1,
  },
  progressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 16,
    borderTopWidth: 1,
    borderTopColor: theme.colors.border,
  },
  progressText: {
    fontSize: 14,
    color: theme.colors.onBackground,
    marginRight: 12,
    minWidth: 80,
  },
  progressBar: {
    flex: 1,
    height: 4,
    backgroundColor: theme.colors.surfaceVariant,
    borderRadius: 2,
  },
  progressFill: {
    height: '100%',
    backgroundColor: theme.colors.primary,
    borderRadius: 2,
  },
});
```

### **GameLibraryScreen.tsx**
```typescript
interface GameFilter {
  category?: string[];
  difficulty?: 'Beginner' | 'Intermediate' | 'Advanced';
  playerCount?: string;
  onlyDownloaded?: boolean;
  onlyFavorites?: boolean;
}

export const GameLibraryScreen: React.FC = () => {
  const navigation = useNavigation();
  const { theme } = useTheme();
  const styles = getStyles(theme);
  
  const [games, setGames] = useState<GameMetadata[]>([]);
  const [filteredGames, setFilteredGames] = useState<GameMetadata[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filter, setFilter] = useState<GameFilter>({});
  const [showFilters, setShowFilters] = useState(false);
  const [refreshing, setRefreshing] = useState(false);

  // Load games on mount
  useEffect(() => {
    loadGames();
  }, []);

  // Filter games when search or filter changes
  useEffect(() => {
    filterGames();
  }, [games, searchQuery, filter]);

  const loadGames = async () => {
    try {
      setLoading(true);
      const gameData = await GameDataService.getInstance().getAllGames();
      setGames(gameData);
    } catch (error) {
      console.error('Failed to load games:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterGames = async () => {
    let filtered = games.filter(game => {
      // Search query filter
      const matchesSearch = searchQuery === '' || 
        game.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        game.description.toLowerCase().includes(searchQuery.toLowerCase());

      return matchesSearch;
    });

    // Apply additional filters
    if (filter.category && filter.category.length > 0) {
      filtered = filtered.filter(game => 
        filter.category!.some(cat => game.category.includes(cat))
      );
    }

    if (filter.difficulty) {
      filtered = filtered.filter(game => game.difficulty === filter.difficulty);
    }

    if (filter.onlyDownloaded) {
      const downloaded = await StorageService.getDownloadedGames();
      filtered = filtered.filter(game => 
        game.bundled || downloaded.includes(game.id)
      );
    }

    if (filter.onlyFavorites) {
      const favorites = await StorageService.getFavorites();
      filtered = filtered.filter(game => favorites.includes(game.id));
    }

    setFilteredGames(filtered);
  };

  const handleRefresh = async () => {
    setRefreshing(true);
    await loadGames();
    // Check for updates
    try {
      await GameDataService.getInstance().checkForUpdates();
    } catch (error) {
      console.log('Update check failed:', error);
    }
    setRefreshing(false);
  };

  const handleGamePress = async (game: GameMetadata) => {
    try {
      // Check if game is available locally
      if (!game.bundled && !game.downloaded) {
        // Navigate to download screen
        navigation.navigate('GameDownload', { gameId: game.id });
        return;
      }

      // Track recent access and navigate to game
      await StorageService.addRecentGame(game.id);
      navigation.navigate('Game', { gameId: game.id });
    } catch (error) {
      console.error('Failed to open game:', error);
    }
  };

  const renderGameCard = ({ item }: { item: GameMetadata }) => (
    <GameCard
      game={item}
      onPress={() => handleGamePress(item)}
      onFavoriteToggle={async () => {
        const isFav = await StorageService.isFavorite(item.id);
        if (isFav) {
          await StorageService.removeFavorite(item.id);
        } else {
          await StorageService.addFavorite(item.id);
        }
        // Refresh if showing only favorites
        if (filter.onlyFavorites) {
          filterGames();
        }
      }}
      theme={theme}
    />
  );

  if (loading) {
    return (
      <View style={styles.centered}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={styles.loadingText}>Loading games...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Track0r Games</Text>
        <TouchableOpacity 
          onPress={() => setShowFilters(!showFilters)}
          style={styles.filterButton}
        >
          <Icon name="filter-list" size={24} color={theme.colors.onBackground} />
        </TouchableOpacity>
      </View>

      {/* Search Bar */}
      <View style={styles.searchContainer}>
        <SearchBar
          value={searchQuery}
          onChangeText={setSearchQuery}
          placeholder="Search games..."
          theme={theme}
        />
      </View>

      {/* Filters */}
      {showFilters && (
        <FilterPanel
          filter={filter}
          onFilterChange={setFilter}
          theme={theme}
        />
      )}

      {/* Games List */}
      <FlatList
        data={filteredGames}
        renderItem={renderGameCard}
        keyExtractor={(item) => item.id}
        contentContainerStyle={styles.gamesList}
        refreshControl={
          <RefreshControl
            refreshing={refreshing}
            onRefresh={handleRefresh}
            colors={[theme.colors.primary]}
          />
        }
        showsVerticalScrollIndicator={false}
        ListEmptyComponent={
          <View style={styles.emptyContainer}>
            <Text style={styles.emptyText}>
              {searchQuery || Object.keys(filter).length > 0 
                ? 'No games match your criteria' 
                : 'No games available'}
            </Text>
          </View>
        }
      />
    </SafeAreaView>
  );
};

const getStyles = (theme: Theme) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  centered: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: theme.colors.onBackground,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: theme.colors.border,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.onBackground,
  },
  filterButton: {
    padding: 8,
  },
  searchContainer: {
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  gamesList: {
    padding: 20,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingVertical: 60,
  },
  emptyText: {
    fontSize: 16,
    color: theme.colors.onSurfaceVariant,
    textAlign: 'center',
  },
});
```

## UI Components

### **GameCard.tsx**
```typescript
interface GameCardProps {
  game: GameMetadata;
  onPress: () => void;
  onFavoriteToggle: () => void;
  theme: Theme;
}

export const GameCard: React.FC<GameCardProps> = ({ 
  game, 
  onPress, 
  onFavoriteToggle,
  theme 
}) => {
  const [isFavorite, setIsFavorite] = useState(false);
  const [isDownloaded, setIsDownloaded] = useState(false);
  const styles = getStyles(theme);

  useEffect(() => {
    checkFavoriteStatus();
    checkDownloadStatus();
  }, [game.id]);

  const checkFavoriteStatus = async () => {
    const favorite = await StorageService.isFavorite(game.id);
    setIsFavorite(favorite);
  };

  const checkDownloadStatus = async () => {
    if (game.bundled) {
      setIsDownloaded(true);
      return;
    }
    
    const downloaded = await StorageService.getDownloadedGames();
    setIsDownloaded(downloaded.includes(game.id));
  };

  const handleFavoritePress = async () => {
    await onFavoriteToggle();
    setIsFavorite(!isFavorite);
    
    // Haptic feedback
    Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
  };

  const getStatusBadge = () => {
    if (game.bundled) {
      return (
        <View style={[styles.badge, styles.bundledBadge]}>
          <Text style={styles.badgeText}>Built-in</Text>
        </View>
      );
    } else if (isDownloaded) {
      return (
        <View style={[styles.badge, styles.downloadedBadge]}>
          <Text style={styles.badgeText}>Downloaded</Text>
        </View>
      );
    } else {
      return (
        <View style={[styles.badge, styles.cloudBadge]}>
          <Icon name="cloud-download" size={12} color={theme.colors.onSurfaceVariant} />
          <Text style={styles.badgeText}>Download</Text>
        </View>
      );
    }
  };

  return (
    <TouchableOpacity 
      style={styles.card} 
      onPress={onPress}
      activeOpacity={0.7}
    >
      <View style={styles.cardContent}>
        {/* Game Icon */}
        <View style={styles.iconContainer}>
          {game.iconUrl ? (
            <Image source={{ uri: game.iconUrl }} style={styles.icon} />
          ) : (
            <View style={styles.defaultIcon}>
              <Text style={styles.iconText}>{game.title.charAt(0)}</Text>
            </View>
          )}
        </View>

        {/* Game Info */}
        <View style={styles.infoContainer}>
          <View style={styles.titleRow}>
            <Text style={styles.title} numberOfLines={1}>{game.title}</Text>
            <TouchableOpacity onPress={handleFavoritePress} style={styles.favoriteButton}>
              <Icon 
                name={isFavorite ? "favorite" : "favorite-border"} 
                size={20} 
                color={isFavorite ? theme.colors.primary : theme.colors.onSurfaceVariant} 
              />
            </TouchableOpacity>
          </View>
          
          {game.subtitle && (
            <Text style={styles.subtitle} numberOfLines={1}>{game.subtitle}</Text>
          )}
          
          <Text style={styles.description} numberOfLines={2}>{game.description}</Text>
          
          {/* Game Details */}
          <View style={styles.detailsRow}>
            <View style={styles.detail}>
              <Icon name="people" size={14} color={theme.colors.onSurfaceVariant} />
              <Text style={styles.detailText}>{game.playerCount}</Text>
            </View>
            <View style={styles.detail}>
              <Icon name="schedule" size={14} color={theme.colors.onSurfaceVariant} />
              <Text style={styles.detailText}>{game.playTime}</Text>
            </View>
            <View style={styles.detail}>
              <Icon name="star" size={14} color={theme.colors.onSurfaceVariant} />
              <Text style={styles.detailText}>{game.difficulty}</Text>
            </View>
          </View>
        </View>
      </View>

      {/* Status Badge */}
      <View style={styles.badgeContainer}>
        {getStatusBadge()}
      </View>
    </TouchableOpacity>
  );
};

const getStyles = (theme: Theme) => StyleSheet.create({
  card: {
    backgroundColor: theme.colors.surface,
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardContent: {
    flexDirection: 'row',
  },
  iconContainer: {
    marginRight: 16,
  },
  icon: {
    width: 60,
    height: 60,
    borderRadius: 8,
  },
  defaultIcon: {
    width: 60,
    height: 60,
    borderRadius: 8,
    backgroundColor: theme.colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: theme.colors.onPrimary,
  },
  infoContainer: {
    flex: 1,
  },
  titleRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 4,
  },
  title: {
    fontSize: 18,
    fontWeight: 'bold',
    color: theme.colors.onSurface,
    flex: 1,
    marginRight: 8,
  },
  favoriteButton: {
    padding: 4,
  },
  subtitle: {
    fontSize: 14,
    color: theme.colors.onSurfaceVariant,
    marginBottom: 8,
  },
  description: {
    fontSize: 14,
    color: theme.colors.onSurfaceVariant,
    lineHeight: 20,
    marginBottom: 12,
  },
  detailsRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  detail: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  detailText: {
    fontSize: 12,
    color: theme.colors.onSurfaceVariant,
    marginLeft: 4,
  },
  badgeContainer: {
    position: 'absolute',
    top: 12,
    right: 12,
  },
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 12,
  },
  bundledBadge: {
    backgroundColor: theme.colors.primaryContainer,
  },
  downloadedBadge: {
    backgroundColor: theme.colors.tertiaryContainer,
  },
  cloudBadge: {
    backgroundColor: theme.colors.surfaceVariant,
  },
  badgeText: {
    fontSize: 10,
    fontWeight: '600',
    color: theme.colors.onSurfaceVariant,
    marginLeft: 4,
  },
});
```

### **DetailPanel.tsx**
```typescript
interface DetailPanelProps {
  step: GameStep | GameSubstep | null;
  formatting: FormattingRules;
  theme: Theme;
}

export const DetailPanel: React.FC<DetailPanelProps> = ({ 
  step, 
  formatting, 
  theme 
}) => {
  const styles = getStyles(theme);
  const { fontSize } = useSettings();

  const formattedContent = useMemo(() => {
    if (!step) return '';
    return FormattingService.formatDetailText(step.detail, formatting);
  }, [step, formatting]);

  if (!step) {
    return (
      <View style={styles.container}>
        <Text style={styles.placeholder}>Select a step to view details</Text>
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <View style={styles.header}>
        <Text style={[styles.title, { fontSize: getFontSize(fontSize, 'title') }]}>
          Details
        </Text>
        <Text style={[styles.stepTitle, { fontSize: getFontSize(fontSize, 'subtitle') }]}>
          {step.title}
        </Text>
      </View>

      <View style={styles.divider} />

      <HTMLRenderer
        html={formattedContent}
        baseStyle={[styles.htmlContent, { fontSize: getFontSize(fontSize, 'body') }]}
        theme={theme}
      />
    </ScrollView>
  );
};

const HTMLRenderer: React.FC<{
  html: string;
  baseStyle: any;
  theme: Theme;
}> = ({ html, baseStyle, theme }) => {
  // Convert HTML to React Native Text components
  const renderHTML = (htmlString: string) => {
    // Simple HTML parser for our specific formatting
    const parts = htmlString
      .replace(/<p>/g, '\n')
      .replace(/<\/p>/g, '\n')
      .replace(/<ul>/g, '\n')
      .replace(/<\/ul>/g, '\n')
      .replace(/<li>/g, '• ')
      .replace(/<\/li>/g, '\n')
      .replace(/<strong>/g, '')
      .replace(/<\/strong>/g, '')
      .replace(/<em>/g, '')
      .replace(/<\/em>/g, '')
      .replace(/<span class="page-ref">([^<]+)<\/span>/g, '\n\n$1')
      .split('\n')
      .filter(line => line.trim());

    return parts.map((line, index) => {
      const isPageRef = line.includes('Rulebook') || line.includes('Rules');
      const isBulletPoint = line.startsWith('• ');
      const isEmphasis = htmlString.includes(`<em>${line}</em>`);
      const isStrong = htmlString.includes(`<strong>${line}</strong>`);

      let style = baseStyle;
      if (isPageRef) {
        style = [baseStyle, styles.pageRef];
      } else if (isBulletPoint) {
        style = [baseStyle, styles.bulletPoint];
      } else if (isEmphasis) {
        style = [baseStyle, styles.emphasis];
      } else if (isStrong) {
        style = [baseStyle, styles.strong];
      }

      return (
        <Text key={index} style={style}>
          {line}
          {index < parts.length - 1 ? '\n' : ''}
        </Text>
      );
    });
  };

  return <View>{renderHTML(html)}</View>;
};

const getFontSize = (setting: 'small' | 'medium' | 'large', type: 'title' | 'subtitle' | 'body') => {
  const sizes = {
    small: { title: 18, subtitle: 14, body: 12 },
    medium: { title: 20, subtitle: 16, body: 14 },
    large: { title: 22, subtitle: 18, body: 16 },
  };
  return sizes[setting][type];
};

const getStyles = (theme: Theme) => StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.surface,
  },
  content: {
    padding: 20,
  },
  placeholder: {
    fontSize: 16,
    color: theme.colors.onSurfaceVariant,
    textAlign: 'center',
    marginTop: 40,
    fontStyle: 'italic',
  },
  header: {
    marginBottom: 16,
  },
  title: {
    fontWeight: 'bold',
    color: theme.colors.primary,
    marginBottom: 8,
  },
  stepTitle: {
    color: theme.colors.onSurface,
    fontWeight: '600',
  },
  divider: {
    height: 2,
    backgroundColor: theme.colors.primary,
    marginBottom: 20,
  },
  htmlContent: {
    color: theme.colors.onSurface,
    lineHeight: 22,
  },
  pageRef: {
    color: theme.colors.onSurfaceVariant,
    fontSize: 12,
    fontWeight: '600',
    backgroundColor: theme.colors.surfaceVariant,
    padding: 4,
    borderRadius: 4,
    marginTop: 8,
  },
  bulletPoint: {
    marginLeft: 16,
    marginVertical: 2,
  },
  emphasis: {
    fontStyle: 'italic',
    backgroundColor: theme.colors.primaryContainer,
    paddingHorizontal: 4,
    paddingVertical: 2,
    borderRadius: 4,
  },
  strong: {
    fontWeight: 'bold',
    color: theme.colors.primary,
  },
});
```

## Mobile-Specific Features

### **Gesture Navigation**
```typescript
export const useGestureNavigation = (navigation: any, onNavigate: (direction: number) => void) => {
  const { hapticFeedback } = useSettings();

  const panGesture = Gesture.Pan()
    .onUpdate((event) => {
      const { translationX, translationY, velocityX, velocityY } = event;
      
      // Horizontal swipe for tab switching
      if (Math.abs(translationX) > 100 && Math.abs(translationY) < 50) {
        if (Math.abs(velocityX) > 500) {
          if (hapticFeedback) {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
          }
          
          // Trigger tab switch
          const direction = translationX > 0 ? -1 : 1;
          // Implementation for tab switching
        }
      }
      
      // Vertical swipe for step navigation
      if (Math.abs(translationY) > 50 && Math.abs(translationX) < 50) {
        if (Math.abs(velocityY) > 300) {
          if (hapticFeedback) {
            Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
          }
          
          const direction = translationY > 0 ? -1 : 1;
          onNavigate(direction);
        }
      }
    });

  return panGesture;
};
```

### **Offline Storage and Sync**
```typescript
class OfflineManager {
  private static syncQueue: SyncOperation[] = [];

  static async enableOfflineMode(): Promise<void> {
    // Cache essential data for offline use
    const games = await GameDataService.getInstance().getAllGames();
    
    for (const game of games) {
      if (game.bundled || game.downloaded) {
        await this.cacheGameData(game.id);
      }
    }
  }

  static async syncWhenOnline(): Promise<void> {
    if (!NetInfo.isConnected) return;

    // Process sync queue
    for (const operation of this.syncQueue) {
      try {
        await this.executeSync(operation);
        this.removeSyncOperation(operation);
      } catch (error) {
        console.error('Sync failed:', error);
      }
    }
  }

  private static async cacheGameData(gameId: string): Promise<void> {
    const gameData = await GameDataService.getInstance().loadGame(gameId);
    await StorageService.saveGame(gameId, gameData);
  }

  private static async executeSync(operation: SyncOperation): Promise<void> {
    switch (operation.type) {
      case 'progress_sync':
        await this.syncGameProgress(operation);
        break;
      case 'settings_sync':
        await this.syncSettings(operation);
        break;
      case 'favorites_sync':
        await this.syncFavorites(operation);
        break;
    }
  }
}
```

### **Push Notifications**
```typescript
class NotificationService {
  static async initialize(): Promise<void> {
    const { status } = await Notifications.requestPermissionsAsync();
    if (status !== 'granted') {
      console.warn('Notification permissions not granted');
      return;
    }

    // Configure notification categories
    await Notifications.setNotificationCategoryAsync('timer', [
      {
        identifier: 'pause',
        buttonTitle: 'Pause',
        options: { opensAppToForeground: false },
      },
      {
        identifier: 'stop',
        buttonTitle: 'Stop',
        options: { opensAppToForeground: false },
      },
    ]);
  }

  static async scheduleTimerNotification(duration: number): Promise<void> {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Turn Timer',
        body: 'Your turn time is up!',
        categoryIdentifier: 'timer',
        sound: true,
      },
      trigger: { seconds: duration },
    });
  }

  static async scheduleGameReminder(gameId: string, title: string, delay: number): Promise<void> {
    await Notifications.scheduleNotificationAsync({
      content: {
        title: 'Game Reminder',
        body: `Continue your ${title} game`,
        data: { gameId },
      },
      trigger: { seconds: delay },
    });
  }

  static async cancelTimerNotifications(): Promise<void> {
    const scheduled = await Notifications.getAllScheduledNotificationsAsync();
    const timerNotifications = scheduled.filter(n => 
      n.content.categoryIdentifier === 'timer'
    );
    
    for (const notification of timerNotifications) {
      await Notifications.cancelScheduledNotificationAsync(notification.identifier);
    }
  }
}
```

## Development Workflow

### **Expo Setup**
```bash
# Create new Expo project
npx create-expo-app track0r-mobile --template typescript

# Navigate to project
cd track0r-mobile

# Install dependencies
npx expo install react-native-gesture-handler react-native-reanimated
npx expo install @react-native-async-storage/async-storage
npx expo install expo-notifications expo-haptics
npx expo install @react-navigation/native @react-navigation/stack @react-navigation/bottom-tabs
npx expo install react-native-screens react-native-safe-area-context
npx expo install expo-linear-gradient expo-blur

# Development dependencies
npm install --save-dev @types/react @types/react-native
npm install --save-dev jest @testing-library/react-native
npm install --save-dev eslint @typescript-eslint/eslint-plugin
```

### **Project Configuration**

#### **app.json**
```json
{
  "expo": {
    "name": "Track0r",
    "slug": "track0r",
    "version": "1.0.0",
    "orientation": "default",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "updates": {
      "fallbackToCacheTimeout": 0
    },
    "assetBundlePatterns": [
      "**/*"
    ],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.gam0r.track0r"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#FFFFFF"
      },
      "package": "com.gam0r.track0r"
    },
    "web": {
      "favicon": "./assets/favicon.png"
    },
    "plugins": [
      "expo-notifications",
      [
        "expo-build-properties",
        {
          "android": {
            "enableProguardInReleaseBuilds": true
          }
        }
      ]
    ]
  }
}
```

#### **package.json Scripts**
```json
{
  "scripts": {
    "start": "expo start",
    "android": "expo start --android",
    "ios": "expo start --ios",
    "web": "expo start --web",
    "test": "jest",
    "test:watch": "jest --watch",
    "lint": "eslint . --ext .ts,.tsx",
    "lint:fix": "eslint . --ext .ts,.tsx --fix",
    "validate-data": "node scripts/validate-game-data.js",
    "bundle-games": "node scripts/bundle-game-data.js",
    "build:android": "eas build --platform android",
    "build:ios": "eas build --platform ios",
    "submit:android": "eas submit --platform android",
    "submit:ios": "eas submit --platform ios"
  }
}
```

### **Build and Deployment Scripts**

#### **scripts/validate-game-data.js**
```javascript
const fs = require('fs');
const path = require('path');
const Ajv = require('ajv');

const schema = require('../assets/data/schema.json');
const ajv = new Ajv();
const validate = ajv.compile(schema);

function validateGameData() {
  const dataDir = path.join(__dirname, '../assets/data');
  const files = fs.readdirSync(dataDir)
    .filter(file => file.endsWith('.json') && file !== 'schema.json' && file !== 'game_index.json');

  const errors = [];

  for (const file of files) {
    const filePath = path.join(dataDir, file);
    const gameData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    
    const valid = validate(gameData);
    if (!valid) {
      errors.push({
        file,
        errors: validate.errors
      });
    }
  }

  if (errors.length > 0) {
    console.error('Validation errors found:');
    errors.forEach(({ file, errors }) => {
      console.error(`\n${file}:`);
      errors.forEach(error => {
        console.error(`  ${error.instancePath}: ${error.message}`);
      });
    });
    process.exit(1);
  } else {
    console.log('All game data files are valid!');
  }
}

validateGameData();
```

#### **scripts/bundle-game-data.js**
```javascript
const fs = require('fs');
const path = require('path');

function bundleGameData() {
  const dataDir = path.join(__dirname, '../assets/data');
  const files = fs.readdirSync(dataDir)
    .filter(file => file.endsWith('.json') && file !== 'schema.json' && file !== 'game_index.json');

  const gameIndex = {
    version: '1.0.0',
    lastUpdated: new Date().toISOString(),
    games: []
  };

  for (const file of files) {
    const filePath = path.join(dataDir, file);
    const gameData = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const stats = fs.statSync(filePath);
    
    const metadata = {
      id: path.basename(file, '.json'),
      title: gameData.gameInfo.title,
      subtitle: gameData.gameInfo.subtitle || '',
      description: gameData.gameInfo.description || '',
      version: gameData.gameInfo.version || '1.0.0',
      size: stats.size,
      lastUpdated: stats.mtime.toISOString(),
      bundled: true,
      downloaded: false,
      category: gameData.gameInfo.category || ['Board Game'],
      difficulty: gameData.gameInfo.difficulty || 'Intermediate',
      playerCount: gameData.gameInfo.playerCount || '1-4',
      playTime: gameData.gameInfo.playTime || '60-90 min'
    };

    gameIndex.games.push(metadata);
  }

  // Sort games alphabetically
  gameIndex.games.sort((a, b) => a.title.localeCompare(b.title));

  // Write game index
  const indexPath = path.join(dataDir, 'game_index.json');
  fs.writeFileSync(indexPath, JSON.stringify(gameIndex, null, 2));

  console.log(`Generated game index with ${gameIndex.games.length} games`);
}

bundleGameData();
```

## Testing Strategy

### **Unit Tests**
```typescript
// __tests__/services/GameDataService.test.ts
import { GameDataService } from '../../src/services/GameDataService';

describe('GameDataService', () => {
  let service: GameDataService;

  beforeEach(() => {
    service = GameDataService.getInstance();
  });

  test('should load bundled game data', async () => {
    const gameData = await service.loadGame('stalker');
    
    expect(gameData).toBeDefined();
    expect(gameData.gameInfo.title).toBe('STALKER');
    expect(gameData.tabs).toHaveLength(2);
    expect(gameData.formatting).toBeDefined();
  });

  test('should search games by title', async () => {
    const results = await service.searchGames('stalker');
    
    expect(results).toHaveLength(1);
    expect(results[0].title).toBe('STALKER');
  });

  test('should filter games by category', async () => {
    const results = await service.searchGames('', { 
      category: ['Cooperative'] 
    });
    
    expect(results.length).toBeGreaterThan(0);
    results.forEach(game => {
      expect(game.category).toContain('Cooperative');
    });
  });
});
```

### **Component Tests**
```typescript
// __tests__/components/GameCard.test.tsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import { GameCard } from '../../src/components/GameCard';

const mockGame = {
  id: 'test-game',
  title: 'Test Game',
  description: 'A test game',
  bundled: true,
  downloaded: false,
  // ... other properties
};

describe('GameCard', () => {
  test('renders game information correctly', () => {
    const { getByText } = render(
      <GameCard
        game={mockGame}
        onPress={jest.fn()}
        onFavoriteToggle={jest.fn()}
        theme={mockTheme}
      />
    );

    expect(getByText('Test Game')).toBeTruthy();
    expect(getByText('A test game')).toBeTruthy();
  });

  test('calls onPress when card is tapped', () => {
    const onPress = jest.fn();
    const { getByTestId } = render(
      <GameCard
        game={mockGame}
        onPress={onPress}
        onFavoriteToggle={jest.fn()}
        theme={mockTheme}
      />
    );

    fireEvent.press(getByTestId('game-card'));
    expect(onPress).toHaveBeenCalled();
  });
});
```

### **Integration Tests**
```typescript
// __tests__/integration/GameFlow.test.tsx
import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import { GameScreen } from '../../src/screens/GameScreen';

describe('Game Flow Integration', () => {
  test('complete game navigation flow', async () => {
    const { getByText, getByTestId } = render(
      <GameScreen route={{ params: { gameId: 'stalker' } }} />
    );

    // Wait for game to load
    await waitFor(() => {
      expect(getByText('STALKER')).toBeTruthy();
    });

    // Test tab switching
    fireEvent.press(getByText('Setup'));
    expect(getByText('Game Setup Overview')).toBeTruthy();

    // Test step navigation
    fireEvent.press(getByTestId('next-button'));
    // Verify step changed
  });
});
```

## Deployment Strategy

### **App Store Optimization**

#### **Core App Strategy**
- **Base Package**: Include 2-3 most popular games (STALKER, Wondrous Creatures)
- **Size Optimization**: Target under 50MB for initial download
- **Offline First**: Full functionality without internet connection
- **Progressive Enhancement**: Additional features when online

#### **Content Delivery**
```typescript
interface ContentStrategy {
  // Bundled content (always available)
  bundledGames: string[];
  
  // Downloadable content (on-demand)
  downloadableGames: string[];
  
  // Update mechanism
  updateStrategy: 'app-store' | 'over-the-air' | 'hybrid';
}

const CONTENT_STRATEGY: ContentStrategy = {
  bundledGames: ['stalker', 'wondrous_creatures'],
  downloadableGames: ['star_wars_unlimited', 'community_games'],
  updateStrategy: 'hybrid'
};
```

### **Monetization Models**

#### **Freemium Model**
```typescript
interface MonetizationTiers {
  free: {
    gamesIncluded: string[];
    features: string[];
    limitations: string[];
  };
  premium: {
    price: string;
    gamesIncluded: string[];
    features: string[];
    benefits: string[];
  };
}

const MONETIZATION: MonetizationTiers = {
  free: {
    gamesIncluded: ['stalker', 'wondrous_creatures'],
    features: ['Basic navigation', 'Offline mode', 'Progress tracking'],
    limitations: ['2 games only', 'No cloud sync', 'Basic themes']
  },
  premium: {
    price: '$4.99/month or $29.99/year',
    gamesIncluded: ['all_current', 'all_future'],
    features: ['All games', 'Cloud sync', 'Advanced themes', 'Turn timer', 'Notes'],
    benefits: ['No ads', 'Priority support', 'Early access']
  }
};
```

#### **One-Time Purchase Model**
```typescript
const PURCHASE_MODEL = {
  baseApp: {
    price: '$9.99',
    includes: ['Core functionality', '3 popular games', 'Offline mode']
  },
  gamePacks: {
    cooperativeGames: { price: '$2.99', games: 5 },
    strategyGames: { price: '$3.99', games: 7 },
    partyGames: { price: '$1.99', games: 4 }
  },
  premiumFeatures: {
    price: '$4.99',
    features: ['Cloud sync', 'Advanced themes', 'Turn timer', 'Analytics']
  }
};
```

### **Release Timeline**

#### **Phase 1: MVP Release (8-10 weeks)**
- Core React Native app with 2-3 games
- Basic navigation and offline functionality
- iOS and Android app store submission
- User feedback collection and analytics

#### **Phase 2: Feature Enhancement (4-6 weeks)**
- Additional games and content
- Advanced features (timer, themes, sync)
- Performance optimization
- User-requested features

#### **Phase 3: Platform Expansion (6-8 weeks)**
- Web version via React Native Web
- Desktop version consideration
- API for third-party integrations
- Community features

#### **Phase 4: Ecosystem Development (Ongoing)**
- Game creation tools for community
- Publisher partnerships
- Advanced analytics and insights
- AI-powered features

### **Success Metrics**

#### **Technical KPIs**
- App startup time: < 2 seconds
- Game load time: < 500ms
- Crash rate: < 0.1%
- App store rating: > 4.5 stars

#### **User Experience KPIs**
- Daily active users: Target 1000+ within 3 months
- Session duration: Target 15+ minutes average
- User retention: 70% after 7 days, 40% after 30 days
- Feature adoption: 80% of users try premium features

#### **Business KPIs**
- Conversion rate: 10% free to premium within 30 days
- Average revenue per user: $15/year
- Customer acquisition cost: < $5
- Lifetime value: > $25

## Migration from Web Version

### **Data Compatibility**
The existing JSON data format from the web refactor is 100% compatible with React Native:

```typescript
// Web data works directly in React Native
const webGameData = require('./stalker.json');
const mobileGameData: GameData = webGameData; // No conversion needed

// Same formatting rules apply
const formattedText = FormattingService.formatDetailText(
  step.detail, 
  gameData.formatting
);
```

### **Feature Parity**
All web features will be preserved and enhanced:

- ✅ **Tab-based navigation** → Enhanced with gestures
- ✅ **Step-by-step progression** → Added haptic feedback
- ✅ **Detailed rule references** → Improved typography
- ✅ **Mobile responsiveness** → Native mobile optimization
- ✅ **Offline functionality** → Enhanced with local storage
- ✅ **Keyboard navigation** → Added touch gestures

### **Progressive Enhancement**
```typescript
interface FeatureComparison {
  web: string[];
  reactNative: string[];
  enhanced: string[];
}

const FEATURES: FeatureComparison = {
  web: [
    'Basic navigation',
    'Tab switching', 
    'Mobile responsive',
    'Offline capable'
  ],
  reactNative: [
    'All web features',
    'Native performance',
    'Gesture navigation',
    'Haptic feedback'
  ],
  enhanced: [
    'Push notifications',
    'Background sync',
    'Camera integration',
    'Native sharing'
  ]
};
```

## Conclusion

The React Native implementation builds perfectly on the data-driven architecture proposed for the web refactor. Key advantages include:

### **Technical Benefits**
- **Shared Data Format**: Existing JSON structure works unchanged
- **Code Reuse**: Business logic shared across platforms
- **Native Performance**: 60fps animations and smooth interactions
- **Offline First**: Enhanced local storage and sync capabilities

### **User Experience Benefits**
- **Familiar Interface**: Consistent with web version
- **Mobile Optimized**: Touch gestures and native patterns
- **Enhanced Features**: Notifications, haptics, camera integration
- **Accessibility**: Native accessibility features

### **Development Benefits**
- **Single Codebase**: iOS, Android, and Web from one source
- **Rapid Development**: Proven patterns and shared components
- **Easy Maintenance**: Centralized data and business logic
- **Scalable Architecture**: Ready for future enhancements

### **Business Benefits**
- **Market Reach**: Native mobile apps in app stores
- **Monetization**: Multiple revenue models supported
- **User Engagement**: Enhanced with mobile-specific features
- **Growth Potential**: Platform for community and partnerships

The React Native version represents a natural evolution that preserves all existing functionality while unlocking the full potential of mobile platforms. The shared data architecture ensures consistency across platforms while enabling platform-specific enhancements.

**Recommendation**: Proceed with React Native implementation using Expo for rapid development, targeting MVP release within 8-10 weeks with core functionality and 2-3 bundled games. 
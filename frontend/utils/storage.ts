/**
 * Safe storage utilities for handling session/local storage
 */

export const safeStorage = {
  /**
   * Safely set item in storage with JSON stringify
   */
  setItem: (key: string, value: any, storage: Storage = sessionStorage): boolean => {
    try {
      const serialized = JSON.stringify(value);
      storage.setItem(key, serialized);
      return true;
    } catch (error) {
      console.error(`Error saving to storage (${key}):`, error);
      return false;
    }
  },

  /**
   * Safely get item from storage with JSON parse
   */
  getItem: <T = any>(key: string, storage: Storage = sessionStorage): T | null => {
    try {
      const item = storage.getItem(key);
      if (!item) return null;
      
      return JSON.parse(item) as T;
    } catch (error) {
      console.error(`Error parsing from storage (${key}):`, error);
      // Clear corrupted data
      storage.removeItem(key);
      return null;
    }
  },

  /**
   * Remove item from storage
   */
  removeItem: (key: string, storage: Storage = sessionStorage): void => {
    try {
      storage.removeItem(key);
    } catch (error) {
      console.error(`Error removing from storage (${key}):`, error);
    }
  },

  /**
   * Clear all storage
   */
  clear: (storage: Storage = sessionStorage): void => {
    try {
      storage.clear();
    } catch (error) {
      console.error('Error clearing storage:', error);
    }
  }
};

export default safeStorage;
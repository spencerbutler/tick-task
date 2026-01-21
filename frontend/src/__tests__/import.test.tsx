/**
 * Import test to ensure all component imports resolve correctly.
 * This test helps catch import path issues early.
 */

import { describe, test, expect } from 'vitest';

// Test that all view components can be imported
describe('Component Imports', () => {
  test('should import all view components', async () => {
    // Test TodayView import
    const { TodayView } = await import('../views/TodayView');
    expect(TodayView).toBeDefined();
    expect(typeof TodayView).toBe('function');

    // Test InboxView import
    const { InboxView } = await import('../views/InboxView');
    expect(InboxView).toBeDefined();
    expect(typeof InboxView).toBe('function');

    // Test ContextsView import
    const { ContextsView } = await import('../views/ContextsView');
    expect(ContextsView).toBeDefined();
    expect(typeof ContextsView).toBe('function');

    // Test TagsView import
    const { TagsView } = await import('../views/TagsView');
    expect(TagsView).toBeDefined();
    expect(typeof TagsView).toBe('function');
  });

  test('should import all component modules', async () => {
    // Test Navigation component import
    const { Navigation } = await import('../components/Navigation');
    expect(Navigation).toBeDefined();
    expect(typeof Navigation).toBe('function');

    // Test TaskModal component import
    const { TaskModal } = await import('../components/TaskModal');
    expect(TaskModal).toBeDefined();
    expect(typeof TaskModal).toBe('function');
  });

  test('should import hooks', async () => {
    // Test useTasks hook import
    const { useTasks } = await import('../hooks/useTasks');
    expect(useTasks).toBeDefined();
    expect(typeof useTasks).toBe('function');
  });

  test('should import types', async () => {
    // Test API types import - just verify the module can be imported
    const apiTypes = await import('../types/api');
    expect(apiTypes).toBeDefined();
    expect(typeof apiTypes).toBe('object');
  });
});

describe('App Import', () => {
  test('should import App component with all dependencies', async () => {
    // This test ensures that App.tsx can import all its dependencies
    // If any import path is broken, this will fail
    const appModule = await import('../App');
    expect(appModule.default).toBeDefined();
    expect(typeof appModule.default).toBe('function');
  });
});

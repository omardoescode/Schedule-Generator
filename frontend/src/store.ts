// This file is deprecated. Use stores/courses.ts instead.
import { writable, type Writable } from 'svelte/store';
import type { Course } from './types';

export const courses: Writable<Course[]> = writable([]);

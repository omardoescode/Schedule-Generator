import { writable, type Writable } from 'svelte/store';
import type { Course } from '../types';
import { browser } from '$app/environment';

export const courses: Writable<Course[]> = writable([]);

if (browser) {
	const saved = localStorage.getItem('courses');
	if (saved) {
		try {
			courses.set(JSON.parse(saved));
		} catch {}
	}
	courses.subscribe((value) => {
		localStorage.setItem('courses', JSON.stringify(value));
	});
}
